from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from .Managers.ManagerFactory import ManagerFactory
from .Campaign import Campaign
from .Util import generate_random_string
import json

# Create your views here.
def index(request):
    category_id = request.GET.get('category', None)
    sort_by = request.GET.get('sort', None)
    favorites = request.GET.get('favorites', None)
    userData = request.session.get('userData', None)
    
    if favorites and userData:
        if category_id:
            campaigns = ManagerFactory.get_campaign_manager().get_favourite_campaigns_by_category(
                userData['id'],
                int(category_id),
                sort_by=sort_by
            )
        else:
            # Dodajemy sprawdzenie czy użytkownik jest zalogowany
            if not userData:
                return redirect('auth')
            campaigns = ManagerFactory.get_campaign_manager().get_favourite_campaigns(
                userData['id'],
                sort_by=sort_by
            )
    elif category_id:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_category(
            int(category_id), 
            sort_by=sort_by
        )
    else:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_sorted(
            sort_by=sort_by
        )
        
    userData = request.session.get('userData', None)
    query = request.session.get('query', None)
    return render(request, 'DawajKase/index.html', {
        'userData': userData,
        'campaigns': campaigns,
        'query': query,
        'selected_category': category_id,
        'sort_by': sort_by,
        'favorites': favorites
    })

def auth(request):
    userData = request.session.get('userData', None)
    if userData:
        return redirect('index')
    
    register = request.GET.get('register', None)
    query = request.session.get('query', None)
    return render(request, 'DawajKase/auth.html', {'register': register, 'query': query})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        UserManager = ManagerFactory.get_user_manager()

        ret = UserManager.log_user_in(email, password)
        
        if ret[0] == "OK":
            user = ret[1]
            request.session['userData'] = user.to_json()
            return redirect('index')
        elif ret[0] == "InvalidPassword":
            messages.error(request, "Invalid password.")
        elif ret[0] == "InvalidEmail":
            messages.error(request, "Invalid email.")
        
    else:
        pass                  

    return redirect('auth')

def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstname')
        lastName = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        city = request.POST.get('city')
        address = request.POST.get('address')

        if password != confirmPassword:
            messages.error(request, "Passwords are not the same.")
            return redirect('/auth?register=1')

        UserManager = ManagerFactory.get_user_manager()

        if UserManager.check_if_user_exists(email):
            messages.error(request, "The email address is already in use.")
            return redirect('/auth?register=1')

        UserManager.register_user(firstName, lastName, email, password, city, address)

    else:
        pass

    return redirect('auth')

def logout(request):
    request.session.flush()
    return redirect('index')

def project(request, slug):
    campaign = ManagerFactory.get_campaign_manager().get_campaign_by_id(slug)

    if not campaign:
        return render(request, 'DawajKase/404.html')
    
    creator = ManagerFactory.get_user_manager().get_user_by_id(campaign.organizerID)

    if not creator:
        return render(request, 'DawajKase/404.html')
    
    comments = ManagerFactory.get_comment_manager().get_comments_by_project_id(campaign.id)
    userData = request.session.get('userData', None)
    isFavourited = ManagerFactory.get_favourite_manager().is_favourited_by_user_with_id(slug, userData['id']) if userData else None
    donations = ManagerFactory.get_campaign_manager().get_donations(campaign.id)
    donors_count = ManagerFactory.get_campaign_manager().count_unique_donors(campaign.id)

    return render(request, 'DawajKase/project.html', {
        'userData': userData,
        'isFavourited': isFavourited,
        'campaign': campaign.to_json(),
        'creator': creator.to_json(),
        'comments': comments,
        'donations': donations,
        'donors_count': donors_count
    })

def confirmation_tab(request):
    userData = request.session.get('userData', None)
    if not userData or userData['role'] != 'Admin':
        return redirect('index')
    campaigns = ManagerFactory.get_campaign_manager().get_campaigns_to_be_approved()
    query = request.session.get('query', None)
    users = ManagerFactory.get_user_manager().get_all_users()
    return render(request, 'DawajKase/confirmationtab.html', {'userData': userData, 'campaigns': campaigns, 'query': query, 'users': users})

def approve_campaign(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        campaignID = data.get('campaign_id')

        ManagerFactory.get_campaign_manager().approve_campaign(campaignID)

        return HttpResponse("OK", status=200)
    else:
        return render(request, 'DawajKase/404.html')

def change_role(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        userID = data.get('user_id')
        role = data.get('role')

        if role == '1' or role == '2':
            role = 'Organizer' if role == '2' else 'Supporter'
            ManagerFactory.get_user_manager().change_role(userID, role)
        elif role == '3':
            ManagerFactory.get_user_manager().delete_user(userID)

        return HttpResponse("OK", status=200)
    else:
        return render(request, 'DawajKase/404.html')

def become_creator(request):
    userData = request.session.get('userData', None)
    if not userData or userData['role'] == 'Organizer':
        return redirect('index')
    
    query = request.session.get('query', None)

    if request.method == 'POST':
        phoneNumber = request.POST.get('phone')
        bankNumber = request.POST.get('bank')
        # documentPhoto = request.FILES['image'] # Disabled to not enter a file each time the during development

        ManagerFactory().get_user_manager().send_verification_request(userData['id'], phoneNumber, bankNumber, '')

        messages.success(request, 'Your request has been sent')
        return redirect('become_creator')

    return render(request, 'DawajKase/becomecreator.html', {'userData': userData, 'query': query})

def search(request):
    query = request.GET.get('q', '').strip()
    reset = request.GET.get('reset', False)
    sort_by = request.GET.get('sort', None)

    if query:
        campaigns = ManagerFactory.get_campaign_manager().search_campaigns(query)
    else:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_sorted(sort_by=sort_by)

    if reset:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_sorted(sort_by=sort_by)
        return render(request, 'DawajKase/campaign_list.html', {
            'campaigns': campaigns, 
            'showDescription': True,
            'sort_by': sort_by
        })

    return render(request, 'DawajKase/campaign_list.html', {
        'campaigns': campaigns, 
        'showDescription': True,
        'sort_by': sort_by
    })

def search_bar(request):
    query = request.GET.get('q', '').strip()
    reset = request.GET.get('reset', False)
    sort_by = request.GET.get('sort', None)
    request.session['query'] = query

    if query:
        campaigns = ManagerFactory.get_campaign_manager().search_campaigns(query)
    else:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_sorted(sort_by=sort_by)
    
    return render(request, 'DawajKase/search.html', {
        'campaigns': campaigns, 
        'showDescription': True, 
        'query': query,
        'sort_by': sort_by
    })
    
def campaign_create(request):
    from datetime import date, timedelta
    userData = request.session.get('userData', None)
    query = request.session.get('query', None)
    tomorrow = date.today() + timedelta(days=1)
    return render(request, 'DawajKase/campaign_create.html', {
        'userData': userData,
        'query': query,
        'tomorrow': tomorrow.isoformat()
    })

def insert_campaign(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        shortDescription = request.POST.get('shortDescription')
        description = request.POST.get('description')
        targetMoneyAmount = request.POST.get('targetMoneyAmount')
        endDate = request.POST.get('endDate')
        image = request.FILES['image']

        if image:
            imagePath = f'media/campaign_thumbnails/' + generate_random_string(16)
            with open(f'static/{imagePath}', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
        
            userData = request.session.get('userData', None)
            campaignManager = ManagerFactory.get_campaign_manager()
            category_name = request.POST.get('category')
            category_id = ManagerFactory.get_category_manager().get_category_id_by_name(category_name)

            print(userData['id'], category_id)
            if campaignManager.insert_campaign(title, shortDescription, description, targetMoneyAmount, endDate, imagePath, userData['id'], category_id):
                pass
            else:
                pass

        else:
            pass

    else:
        pass

    return redirect('index')
    
def favourite_campaign(request, id):
    userData = request.session.get('userData', None)
    if userData:
        isFavourited = ManagerFactory.get_favourite_manager().is_favourited_by_user_with_id(id, userData['id'])
        if isFavourited:
            ManagerFactory.get_favourite_manager().remove_campaign_from_favourites(id, userData['id'])
        else:
            ManagerFactory.get_favourite_manager().add_campaign_to_favourites(id, userData['id'])
    
    return redirect('/project/' + id)







def donate(request, id):
    userData = request.session.get('userData', None)
    campaign = ManagerFactory.get_campaign_manager().get_campaign_by_id(id).to_json()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        message = request.POST.get('message')

        error = None
        if len(amount) == 0:
            error = "Enter a value!"

        if not error:
            amount = int(amount)
            if amount <= 0:
                error = "The amount must be greater than 0!"

        if not message:
            message = " "

        if error:
            return render(request, 'DawajKase/donate.html', {'userData': userData, 'campaign': campaign, 'error': error})
        else:
            if userData:
                ManagerFactory.get_payment_manager().donate(campaign['id'], userData['id'], amount, message)
            else:
                ManagerFactory.get_payment_manager().donate_anonymously(campaign['id'], amount, message)

        return redirect('/project/' + id)
    else:
        if not campaign:
            return render(request, 'DawajKase/404.html')
        
        return render(request, 'DawajKase/donate.html', {'userData': userData, 'campaign': campaign})

def delete_campaign(request, id):
    userData = request.session.get('userData', None)
    if not userData:
        return redirect('index')
    campaign = ManagerFactory.get_campaign_manager().get_campaign_by_id(id).to_json()
    
    if not campaign:
        return redirect('index')
    
    if campaign['organizerID'] != userData['id'] and userData['role'] != 'Admin':
        return redirect('index')
    
    ManagerFactory.get_campaign_manager().delete_campaign(id)
    return redirect('index')