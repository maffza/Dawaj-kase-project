from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from .Managers.ManagerFactory import ManagerFactory
from .Campaign import Campaign
from main.models import Campaign, Donation
from django.db.models import Count, Max, Sum, F, FloatField, ExpressionWrapper
from .Util import generate_random_string
import json
import plotly.graph_objs as go
import plotly.offline as opy
from datetime import date

# Create your views here.
def index(request):
    category_id = request.GET.get('category', None)
    sort_by = request.GET.get('sort', None)
    favorites = request.GET.get('favorites', None)
    page = int(request.GET.get('page', 1))
    userData = request.session.get('userData', None)
    
    page_size = 20
    offset = (page - 1) * page_size
    
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
            sort_by=sort_by,
            limit=page_size,
            offset=offset
        )
        total_campaigns = ManagerFactory.get_campaign_manager().count_campaigns()
        total_pages = (total_campaigns + page_size - 1) // page_size
        
    userData = request.session.get('userData', None)
    query = request.session.get('query', None)
    return render(request, 'DawajKase/index.html', {
        'userData': userData,
        'campaigns': campaigns,
        'query': query,
        'selected_category': category_id,
        'sort_by': sort_by,
        'favorites': favorites,
        'current_page': page,
        'total_pages': total_pages if not (favorites or category_id) else 1
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
    
    if campaign.has_finished():
        ManagerFactory.get_campaign_manager().end_campaign(campaign.id)
    
    creator = ManagerFactory.get_user_manager().get_user_by_id(campaign.organizerID)
    if not creator:
        return render(request, 'DawajKase/404.html')
    
    comments = ManagerFactory.get_comment_manager().get_comments_by_project_id(campaign.id)
    userData = request.session.get('userData', None)
    isFavourited = ManagerFactory.get_favourite_manager().is_favourited_by_user_with_id(slug, userData['id']) if userData else None
    donations = ManagerFactory.get_campaign_manager().get_donations(campaign.id)
    donors_count = ManagerFactory.get_campaign_manager().count_unique_donors(campaign.id)
    posts = ManagerFactory.get_post_manager().get_campaign_posts(campaign.id)
    tiers = ManagerFactory.get_reward_manager().get_campaign_tiers(campaign.id)
    
    if donations:
        for donation in donations:
            donation['tier'] = 1
            for i, tier in enumerate(reversed(tiers)):
                if donation['amount'] >= tier.amount:
                    donation['tier'] = int(float(len(tiers) - i - 1) / (len(tiers) - 1) * 9 + 1)
                    break

    return render(request, 'DawajKase/project.html', {
        'userData': userData,
        'isFavourited': isFavourited,
        'campaign': campaign.to_json(),
        'creator': creator.to_json(),
        'comments': comments,
        'donations': donations,
        'donors_count': donors_count,
        'posts': posts,
        'tiers': tiers
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
        # documentPhoto = request.FILES.get('image') # Disabled to not enter a file each time the during development

        ManagerFactory().get_user_manager().send_verification_request(userData['id'], phoneNumber, bankNumber, '')

        messages.success(request, 'Your request has been sent')
        return redirect('become_creator')

    return render(request, 'DawajKase/becomecreator.html', {'userData': userData, 'query': query})

def search(request):
    query = request.GET.get('q', '').strip()
    reset = request.GET.get('reset', False)
    sort_by = request.GET.get('sort', None)
    page = int(request.GET.get('page', 1))
    
    page_size = 19
    offset = (page - 1) * page_size

    if query:
        campaigns = ManagerFactory.get_campaign_manager().search_campaigns(query)
    else:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_sorted(
            sort_by=sort_by,
            limit=page_size,
            offset=offset
        )
        total_campaigns = ManagerFactory.get_campaign_manager().count_campaigns()
        total_pages = (total_campaigns + page_size - 1) // page_size

    if reset:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_sorted(sort_by=sort_by)
        return render(request, 'DawajKase/campaign_list.html', {
            'campaigns': campaigns, 
            'showDescription': True,
            'sort_by': sort_by,
            'current_page': page,
            'total_pages': total_pages if not query else 1
        })

    return render(request, 'DawajKase/campaign_list.html', {
        'campaigns': campaigns, 
        'showDescription': True,
        'sort_by': sort_by,
        'current_page': page,
        'total_pages': total_pages if not query else 1
    })

def search_bar(request):
    query = request.GET.get('q', '').strip()
    reset = request.GET.get('reset', False)
    sort_by = request.GET.get('sort', None)
    page = int(request.GET.get('page', 1))
    request.session['query'] = query
    
    page_size = 20
    offset = (page - 1) * page_size

    if query:
        campaigns = ManagerFactory.get_campaign_manager().search_campaigns(query)
    else:
        campaigns = ManagerFactory.get_campaign_manager().get_campaigns_sorted(
            sort_by=sort_by,
            limit=page_size,
            offset=offset
        )
        total_campaigns = ManagerFactory.get_campaign_manager().count_campaigns()
        total_pages = (total_campaigns + page_size - 1) // page_size
    
    return render(request, 'DawajKase/search.html', {
        'campaigns': campaigns, 
        'showDescription': True, 
        'query': query,
        'sort_by': sort_by,
        'current_page': page,
        'total_pages': total_pages if not query else 1
    })
    
def campaign_create(request):
    from datetime import date, timedelta
    userData = request.session.get('userData', None)
    query = request.session.get('query', None)
    tomorrow = date.today() + timedelta(days=1)
    categories = ManagerFactory.get_category_manager().get_all_categories()

    return render(request, 'DawajKase/campaign_create.html', {
        'userData': userData,
        'query': query,
        'tomorrow': tomorrow.isoformat(),
        'categories': categories
    })

def insert_campaign(request):
    # Check if POST request
    if request.method != 'POST':
        return redirect('campaign_create')

    # Check if user is logged in
    userData = request.session.get('userData', None)
    if not userData:
        return redirect('campaign_create')

    # Insert the campaign
    title = request.POST.get('title')
    shortDescription = request.POST.get('shortDescription')
    description = request.POST.get('description')
    targetMoneyAmount = request.POST.get('targetMoneyAmount')
    endDate = request.POST.get('endDate')
    image = request.FILES.get('image')
    tierAmounts = request.POST.getlist('tierAmount[]')
    tierDescriptions = request.POST.getlist('tierDescription[]')

    if image:
        imagePath = f'media/campaign_thumbnails/' + generate_random_string(16)
        with open(f'static/{imagePath}', 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
    
        campaignManager = ManagerFactory.get_campaign_manager()
        category_name = request.POST.get('category')
        category_id = ManagerFactory.get_category_manager().get_category_id_by_name(category_name)

        campaignID = campaignManager.insert_campaign(title, shortDescription, description, targetMoneyAmount, endDate, imagePath, userData['id'], category_id)

        if tierAmounts and len(tierAmounts) > 0:
            ManagerFactory.get_reward_manager().insert_tiers(tierAmounts, tierDescriptions, campaignID)

    else:
        # no pic
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


def insert_post(request):
    campaignID = request.POST.get('campaign_id')

    # Check if POST request
    if request.method != 'POST':
        return redirect(f'project/{campaignID}')

    # Check if the campaign exists
    campaign = ManagerFactory.get_campaign_manager().get_campaign_by_id(campaignID)

    if not campaign:
        return redirect(f'project/{campaignID}')

    # Check if user is logged in
    userData = request.session.get('userData', None)
    if not userData:
        return redirect(f'project/{campaignID}')
    
    # Check if the user is allowed to insert a post
    userID = userData['id']

    if campaign.organizerID != userID:
        return redirect(f'project/{campaignID}')

    # Insert the post
    title = request.POST.get('postTitle')
    description = request.POST.get('postContent')
    image = request.FILES.get('postImage')

    if image:
        imagePath = f'media/post_images/' + generate_random_string(16)
        with open(f'static/{imagePath}', 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
    else:
        imagePath = None

    ManagerFactory.get_post_manager().add_post(title, description, imagePath, userID, campaignID)

    return redirect(f'project/{campaignID}')


def add_comment(request):
    campaignID = request.POST.get('campaign_id')

    # Check if POST request
    if request.method != 'POST':
        return redirect(f'project/{campaignID}')

    # Check if the campaign exists
    campaign = ManagerFactory.get_campaign_manager().get_campaign_by_id(campaignID)

    if not campaign:
        return redirect(f'project/{campaignID}')

    # Check if user is logged in
    userData = request.session.get('userData', None)
    if not userData:
        return redirect(f'project/{campaignID}')

    # Add the comment
    text = request.POST.get('text')
    
    if text:
        ManagerFactory.get_comment_manager().insert_comment(text, campaignID, userData['id'])

    return redirect(f'project/{campaignID}')






def chart_button_view(request):
    return render(request, 'campaigns/button.html')

def donation_stats_table(request):
    campaigns = Campaign.objects.annotate(
        num_donations=Count('donation'),
        max_donation=Max('donation__amount'),
        percent_funded=ExpressionWrapper(
            100 * F('current_money_amount') / F('target_money_amount'),
            output_field=FloatField()
        )
    )

    titles = [c.title for c in campaigns]
    num_donations = [c.num_donations for c in campaigns]
    max_donations = [f"${c.max_donation:.2f}" if c.max_donation else "$0.00" for c in campaigns]
    percent_funded = [f"{c.percent_funded:.1f}%" if c.percent_funded else "0%" for c in campaigns]

    table = go.Figure(data=[
        go.Table(
            header=dict(values=["Campaign", "Number of Donations", "Highest Donation", "Percent Funded"]),
            cells=dict(values=[titles, num_donations, max_donations, percent_funded])
        )
    ])

    chart_div = opy.plot(table, auto_open=False, output_type='div')
    return render(request, 'DawajKase/chart.html', {'chart_div': chart_div})


def fetch_successful_campaigns(start_date, end_date):
    django_cursor = connection.cursor()
    raw_conn = django_cursor.connection
    raw_cursor = raw_conn.cursor() 
    output_cursor = raw_conn.cursor()

    raw_cursor.execute("""
        BEGIN
            :1 := CROWDFUNDING_PKG.get_successful_campaigns(:2, :3);
        END;
    """, [output_cursor, start_date, end_date])

    results = output_cursor.fetchall()
    columns = [col[0].lower() for col in output_cursor.description]

    return results, columns


def successful_campaigns_chart(request):
    userData = request.session.get('userData', None)
    rows, columns = fetch_successful_campaigns(
        date(2020, 1, 1),
        date(2030, 1, 1)
    )

    if not rows:
        return render(request, 'DawajKase/chart.html', {
            'userData': userData,
            'message': 'No successful campaigns found in the given time range.'
        })

    data_by_column = list(zip(*rows))

    fig = go.Figure(data=[
        go.Table(
            header=dict(values=[col.replace('_', ' ').title() for col in columns]),
            cells=dict(values=data_by_column)
        )
    ])

    chart_div = opy.plot(fig, auto_open=False, output_type='div')




    campaign_count = len(rows)

    column_indices = {col: idx for idx, col in enumerate(columns)}
    donation_values = [row[column_indices['average_donation']] for row in rows if row[column_indices['average_donation']] is not None]
    total_collected_values = [row[column_indices['total_collected']] for row in rows if row[column_indices['total_collected']] is not None]


    avg_donation = round(sum(donation_values) / len(donation_values), 2) if donation_values else 0
    total_collected = round(sum(total_collected_values), 2) if total_collected_values else 0
    highest_donation = max([row[column_indices['highest_donation']] for row in rows if row[column_indices['highest_donation']] is not None])

    aggregation_text = (
        f"Liczba wyświetlonych kampanii: {campaign_count} | "
        f"Suma wpłat: {total_collected} $ | "
        f"Średnia kwota wpłaty: {avg_donation} $ | "
        f"Najwyższa wpłata: {highest_donation} $"
    )

    return render(request, 'DawajKase/chart.html', {
        'userData': userData,
        'chart_div': chart_div,
        'aggregation_text': aggregation_text
    })


def fetch_verified_user_campaigns():
    django_cursor = connection.cursor()
    raw_conn = django_cursor.connection
    raw_cursor = raw_conn.cursor()
    output_cursor = raw_conn.cursor()

    raw_cursor.execute("""
        BEGIN
            :1 := CROWDFUNDING_PKG.get_verified_user_campaigns;
        END;
    """, [output_cursor])

    results = output_cursor.fetchall()
    columns = [col[0].lower() for col in output_cursor.description]

    return results, columns

def verified_user_campaigns_view(request):
    userData = request.session.get('userData', None)
    rows, columns = fetch_verified_user_campaigns()

    print("COLUMNS:", columns)
    print("ROWS:", rows)
    
    if not rows:
        return render(request, 'DawajKase/chart.html', {
            'userData': userData,
            'message': 'No campaigns found for verified users.'
        })

    data_by_column = list(zip(*rows))

    fig = go.Figure(data=[
        go.Table(
            header=dict(values=[col.replace('_', ' ').title() for col in columns]),
            cells=dict(values=data_by_column)
        )
    ])

    chart_div = opy.plot(fig, auto_open=False, output_type='div')

    campaign_count = len(rows)

    column_indices = {col: idx for idx, col in enumerate(columns)}
    donation_values = [row[column_indices['average_donation']] for row in rows if row[column_indices['average_donation']] is not None]
    total_collected_values = [row[column_indices['total_collected']] for row in rows if row[column_indices['total_collected']] is not None]


    avg_donation = round(sum(donation_values) / len(donation_values), 2) if donation_values else 0
    total_collected = round(sum(total_collected_values), 2) if total_collected_values else 0
    highest_donation = max(row[column_indices['highest_donation']] for row in rows if row[column_indices['highest_donation']] is not None)

    aggregation_text = (
        f"Liczba wyświetlonych kampanii: {campaign_count} | "
        f"Suma wpłat: {total_collected} $ | "
        f"Średnia kwota wpłaty: {avg_donation} $ | "
        f"Najwyższa wpłata: {highest_donation} $"
    )

    return render(request, 'DawajKase/chart.html', {
        'userData': userData,
        'chart_div': chart_div,
        'aggregation_text': aggregation_text
    })
