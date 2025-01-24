from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from .Managers.ManagerFactory import ManagerFactory
from .Campaign import Campaign
from .Util import generate_random_string

# Create your views here.
def index(request):
    campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(9)
    userData = request.session.get('userData', None)
    query = request.session.get('query', None)
    return render(request, 'DawajKase/index.html', {'userData': userData, 'campaigns': campaigns, 'query': query})

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
    isFavourited = ManagerFactory.get_campaign_manager().is_favourited_by_user_with_id(slug, userData['id']) if userData else None
    donations = ManagerFactory.get_campaign_manager().get_donations(campaign.id)

    return render(request, 'DawajKase/project.html', {'userData': userData, 'isFavourited': isFavourited, 'campaign': campaign.to_json(), 'creator': creator.to_json(), 'comments': comments, 'donations': donations})

#MESJASZA BZDETY, TE CHYBA PRAWIDLOWE
def project_adm(request, slug):
    campaign = ManagerFactory.get_campaign_manager().get_campaign_by_id(slug)

    if not campaign:
        return render(request, 'DawajKase/404.html')
    
    creator = ManagerFactory.get_user_manager().get_user_by_id(campaign.organizerID)

    if not creator:
        return render(request, 'DawajKase/404.html')
    
    comments = ManagerFactory.get_comment_manager().get_comments_by_project_id(campaign.id)
    userData = request.session.get('userData', None)
    isFavourited = ManagerFactory.get_campaign_manager().is_favourited_by_user_with_id(slug, userData['id']) if userData else None
    donations = ManagerFactory.get_campaign_manager().get_donations(campaign.id)

    return render(request, 'DawajKase/project_adm.html', {'userData': userData, 'isFavourited': isFavourited, 'campaign': campaign.to_json(), 'creator': creator.to_json(), 'comments': comments, 'donations': donations})


#MESJASZA BZDETY, DO NAPRAWY BY POBIERALO PRAWIDLOWE

def confirmationtab(request):
    campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(9)
    userData = request.session.get('userData', None)
    query = request.session.get('query', None)
    return render(request, 'DawajKase/confirmationtab.html', {'userData': userData, 'campaigns': campaigns, 'query': query})

#MESJASZA BZDETY, DO NAPRAWY BY POBIERALO PRAWIDLOWE

def becomecreator(request):
    campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(9)
    userData = request.session.get('userData', None)
    query = request.session.get('query', None)
    return render(request, 'DawajKase/becomecreator.html', {'userData': userData, 'campaigns': campaigns, 'query': query})


def search(request):
    query = request.GET.get('q', '').strip()
    reset = request.GET.get('reset', False)

    if query:
        campaigns = ManagerFactory.get_campaign_manager().search_campaigns(query)
    else:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(9)

    if reset:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(150)
        return render(request, 'DawajKase/campaign_list.html', {'campaigns': campaigns, 'showDescription': True})

    return render(request, 'DawajKase/campaign_list.html', {'campaigns': campaigns, 'showDescription': True})

def search_bar(request):
    query = request.GET.get('q', '').strip()
    reset = request.GET.get('reset', False)
    if query:
        campaigns = ManagerFactory.get_campaign_manager().search_campaigns(query)
    else:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(150)
    return render(request, 'DawajKase/search.html', {'campaigns': campaigns, 'showDescription': True})



    
def campaign_create(request):
    campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(9)
    userData = request.session.get('userData', None)
    query = request.session.get('query', None)
    return render(request, 'DawajKase/campaign_create.html', {'userData': userData, 'campaigns': campaigns, 'query': query})

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

            if campaignManager.insert_campaign(title, shortDescription, description, targetMoneyAmount, endDate, imagePath, userData['id'], 0):
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
        isFavourited = ManagerFactory.get_campaign_manager().is_favourited_by_user_with_id(id, userData['id'])
        if isFavourited:
            ManagerFactory.get_campaign_manager().remove_campaign_from_favourites(id, userData['id'])
        else:
            ManagerFactory.get_campaign_manager().add_campaign_to_favourites(id, userData['id'])
    
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





    