from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from .Managers.ManagerFactory import ManagerFactory

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
    campaign = ManagerFactory.get_campaign_manager().get_campaigns_by_id(slug)

    if not campaign:
        return render(request, 'DawajKase/404.html')
    
    creator = ManagerFactory.get_user_manager().get_user_by_id(campaign.organizerID)

    if not creator:
        return render(request, 'DawajKase/404.html')
    
    comments = ManagerFactory.get_comment_manager().get_comments_by_project_id(campaign.id)

    userData = request.session.get('userData', None)

    return render(request, 'DawajKase/project.html', {'userData': userData, 'campaign': campaign.to_json(), 'creator': creator.to_json(), 'comments': comments})

def search(request):
    query = request.GET.get('q', '').strip()
    reset = request.GET.get('reset', False)

    if query:
        campaigns = ManagerFactory.get_campaign_manager().search_campaigns(query)
    else:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(9)

    if reset:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_by_limit(9)
        return render(request, 'DawajKase/campaign_list.html', {'campaigns': campaigns, 'showDescription': True})

    return render(request, 'DawajKase/campaign_list.html', {'campaigns': campaigns, 'showDescription': True})


def campaign_create(request):
    return render(request, 'DawajKase/campaign_create.html')


