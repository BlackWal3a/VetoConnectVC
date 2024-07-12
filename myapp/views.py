from django.shortcuts import render,redirect,HttpResponse
from django.db import IntegrityError
from .models import Account,AnimalForm,Blacklist
from django.db.models import Count
from .forms import AnimalFormForm
import pandas as pd
from datetime import datetime
from django.http import JsonResponse,HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import urllib.parse
from decimal import Decimal
#import auth
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login,logout
# Register your custom user model with Django admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone  # Import timezone for today's date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

#Save_Incoming Data
@csrf_exempt
@login_required
def save_date_view(request):
    if request.method == 'POST':
        # Handle tint data
        tint_value = request.POST.get('tint')
        print("Received tint value:", tint_value)
        if tint_value is not None:
            request.user.account.geography_global_selection = tint_value

        #Handle Dark Mode
        darkmode_value = request.POST.get('mode')
        print("Received mode value:", darkmode_value)
        if darkmode_value is not None:
            request.user.account.dark_mode = darkmode_value


        # Handle Geography filters
        geo_filter_id = request.POST.get('geo_id')
        print("Received id value:", geo_filter_id)
        if geo_filter_id is not None:
            request.user.account.geography_filter_id = geo_filter_id

        # Save the data to the database
        request.user.account.save(update_fields=['geography_global_selection'])

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def signup_view(request):
    if request.method == 'POST':
        uname = request.POST.get('name1')
        email = request.POST.get('email1')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if uname == "" or email == "" or password1 == "" or password2 == "":
            error_msg = 'Please fill all fields'
            return render(request, 'sign-up.html', {'error': error_msg})

        if password1 != password2:
            error_msg = 'Passwords do not match.'
            return render(request, 'sign-up.html', {'error': error_msg})

        if User.objects.filter(email=email).exists():
            error_msg = 'Email is already in use.'
            return render(request, 'sign-up.html', {'error': error_msg})

        if User.objects.filter(username=uname).exists():
            error_msg = 'Username is already in use.'
            return render(request, 'sign-up.html', {'error': error_msg})
        
        # Create User object
        my_user = User.objects.create_user(uname, email, password1, last_name="LT")
        
        # Create associated Account object
        account = Account.objects.create(user=my_user)
        
        # Set the unit to "LT" for the newly created account
        account.units = "LT"
        account.dark_mode = 1
        account.save()
        
        return redirect('sign-in')

    return render(request, 'sign-up.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')  # Get the value of Remember Me checkbox

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set session expiry based on Remember Me checkbox
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days expiry
            else:
                request.session.set_expiry(0)  # Browser session expiry
            return redirect('dashboard')  # Redirect to the profile page
        else:
            # Display an error message on the sign-in page
            return render(request, 'sign-in.html', {'error': True})

    return render(request, 'sign-in.html')


@login_required
def dashboard_view(request: HttpRequest):
    # Check if the authenticated user is staff
    if not request.user.is_staff:
        return redirect('profile')  # Redirect non-staff members to the welcome page
    
    if request.user.is_authenticated:
        account = request.user.account

    # Count total submitted forms
    total_submitted_forms = AnimalForm.objects.all().count()
    # Count forms submitted today (adjusted for timezone)
    today_start = timezone.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)
    forms_submitted_today = AnimalForm.objects.filter(date__range=(today_start, today_end)).count()

    # Blacklist
    blacklist = Blacklist.objects.all()
    blacklist_count = blacklist.count()

    # Count non-staff users
    non_staff_users = User.objects.filter(is_staff=False)
    non_staff_user_count = non_staff_users.count()
    # Count non-staff users created today (adjusted for timezone)
    today_start = timezone.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)
    users_created_today = User.objects.filter(is_staff=False, date_joined__range=(today_start, today_end)).count()

    non_staff_accounts = Account.objects.filter(user__is_staff=False)

        # Aggregate the count of each animal name
    animal_name_counts = AnimalForm.objects.values('animal_name').annotate(count=Count('animal_name')).order_by('-count')

    # Prepare data for Chart.js
    animal_names = [item['animal_name'] for item in animal_name_counts]
    name_counts = [item['count'] for item in animal_name_counts]
    
    print(non_staff_user_count)
    current_path = request.path
    data = {
        'submitted_forms' : total_submitted_forms,
        'forms_submitted_today' : forms_submitted_today,
        'non_staff_users': non_staff_user_count,
        'todays_non_staff_users': users_created_today,
        'non_staff_user_info': non_staff_accounts,
        'blacklist' : blacklist,
        'blacklist_count' : blacklist_count,
        'animal_names': animal_names,
        'name_counts': name_counts,        
    }
    return render(request, 'dashboard.html', {'current_path': current_path , 'data':data})

@login_required
def delete_account(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        email = user.email
        user.delete()
        Blacklist.objects.create(email=email)
        return redirect('dashboard')  # Redirect to the dashboard after deletion

    return render(request, 'confirm_delete.html', {'user': user})

@login_required
def remove_from_blacklist(request, email):
    if request.method == 'POST':
        # Find the corresponding blacklist entry
        blacklist_entry = get_object_or_404(Blacklist, email=email)
        # Delete the blacklist entry
        blacklist_entry.delete()
        # Redirect back to the profile page or another appropriate page
        return redirect('dashboard')  # Adjust the redirect target as needed

    return redirect('dashboard')  # Adjust the redirect target as needed

@login_required
def reception_list(request: HttpRequest):
    # Check if the authenticated user is staff
    if not request.user.is_staff:
        return redirect('profile')  # Redirect non-staff members to the welcome page
    
    if request.user.is_authenticated:
        account = request.user.account
    
    data = AnimalForm.objects.all().order_by('-date')  # Sort by date descending using Django ORM
    
    print(data)
    
    current_path = request.path
    print(current_path)
    return render(request, 'reception.html', {'current_path': current_path,'data':data})

@login_required
def admin_profile_view(request : HttpRequest):
    # Check if the authenticated user is staff
    if not request.user.is_staff:
        return redirect('profile')  # Redirect non-staff members to the welcome page
    
    help = Help.objects.all()
    if request.user.is_authenticated:
        email = request.user.email  # Accessing the email attribute of the authenticated user
        account = request.user.account
        surname = account.surname
        name = account.name

    data = {
        'surname': surname,
        'name': name,
        'email': email,
        'help' : help,
    }
    current_path = request.path
    return render(request, 'admin_profile.html', {'current_path': current_path, 'data': data})

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AnimalForm
from .forms import AnimalFormForm

@login_required
def profile_view(request):
    # Check if the authenticated user is staff
    if request.user.is_staff:
        return redirect('reception')  # Redirect staff members to the reception page
    
    if request.user.is_authenticated:
        email = request.user.email  # Accessing the email attribute of the authenticated user
        account = request.user.account
        surname = account.surname
        name = account.name
        num_ordre = account.num_ordre
        specialty = account.specialty
        nom_clinique = account.nom_clinique
        profile_pic_url = account.profile_pic.url if account.profile_pic else None

    # Check for any AnimalForm entries that need feedback
    pending_feedback = AnimalForm.objects.filter(email=email, status='A répondu', status_feedback='No', viewed='Yes').first()
    if pending_feedback:
        request.session['feedback_message'] = 'Veuillez remplir le Feedback avant de continuer.'
        return redirect('client_form_detail', submission_id=pending_feedback.id)
        
    
    # Fetch user submissions
    data = AnimalForm.objects.filter(email=email)
    user_submissions = data.all().order_by('-date')
    
    error = None
    
    if request.method == 'POST':
        form = AnimalFormForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            instance = form.save(commit=False)  # Get the unsaved instance of the form
            instance.client_name = surname  # Set the client_name field to the user's surname
            instance.email = email  # Set the email field to the user's email
            instance.clinic = nom_clinique
            instance.form_picture = profile_pic_url
            instance.save()  # Save the modified instance
            error = False       
        else:
            # Form is not valid, set error flag
            error = True
    
    else:
        form = AnimalFormForm(initial={'client_name': surname, 'email': email, 'clinic': nom_clinique, 'form_pic': profile_pic_url})  # Prepopulate the form with the surname and email as initial values
    
    data = {
        'surname': surname,
        'name': name,
        'email': email,
        'age': specialty,
        'num_ordre': num_ordre,
        'nom_clinique': nom_clinique,
        'profile_pic_url': profile_pic_url,
        'user_submissions': user_submissions,  # Pass the submissions to the template
    }
    
    context = {
        'form': form,
        'data': data,
        'error': error
    }

    return render(request, 'profile.html', context)


from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']
        
        # Assuming you are working with the logged-in user's profile
        user_profile = Account.objects.get(user=request.user)
        user_profile.profile_pic = profile_picture
        user_profile.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure'}, status=400)

def handle_ajax_request(request):
    # Handle the AJAX request here
    if request.method == 'POST':
        # Process the AJAX request
        # For demonstration, let's just return a JsonResponse
        return JsonResponse({'success': True})

def logout_view(request):
    logout(request)
    return redirect('landingpage')

def landingpage_view(request):
    name = ''  # Initialize name variable

    if request.method == 'POST':
        uname = request.POST.get('name1')
        email = request.POST.get('email1')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if uname == "" or email == "" or password1 == "" or password2 == "":
            error_msg = 'Merci de compléter tous les champs'
            return render(request, 'landingpage.html', {'error': error_msg})

        if password1 != password2:
            error_msg = 'Les mots de passe ne correspondent pas.'
            return render(request, 'landingpage.html', {'error': error_msg})

        if User.objects.filter(email=email).exists():
            error_msg = 'Cet email est déjà utilisé.'
            return render(request, 'landingpage.html', {'error': error_msg})

        if Blacklist.objects.filter(email=email).exists():
            error_msg = 'Cet email est est bloqué.'
            return render(request, 'landingpage.html', {'error': error_msg})
            
        if User.objects.filter(username=uname).exists():
            error_msg = 'Nom utilisateur est déjà utilisé'
            return render(request, 'landingpage.html', {'error': error_msg})
        
        # Create User object
        my_user = User.objects.create_user(uname, email, password1, last_name="LT")
        
        # Create associated Account object
        account = Account.objects.create(user=my_user)
        
        # Set the unit to "LT" for the newly created account
        account.units = "LT"
        account.save()
        
        return redirect('success')
    
    if request.user.is_authenticated:
        account = request.user.account
        name = account.surname
    
    data = {
        'name' : name,
    }
    return render(request, 'landingpage.html' , {'data': data})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')  # Access username from form data using 'name' attribute
        password = request.POST.get('password')  # Access password from form data using 'password' attribute
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the authenticated user is staff
            if user.is_staff:
                return redirect('reception')  # Redirect to dashboard if user is staff
            else:
                account = request.user.account
                if not account.surname and not account.name:  # Use `not` for clarity
                    return redirect('welcome')
                else:
                    return redirect('profile')

        else:
            context = {'error': True}  # Set error flag for invalid credentials
    else:
        context = {}  # Empty context for GET requests

    return render(request, 'login.html', context)

from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Help

def help_view(request: HttpRequest):
    error_message = None
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        response = request.POST.get('response')

        # Save the data to the Help model
        help_entry = Help(nom=nom, email=email, response=response)
        help_entry.save()
        return redirect('help_view')  # Redirect to the same page or any other page

    current_path = request.path
    return render(request, 'help.html', {
        'current_path': current_path,
        'error_message': error_message
    })


def success_page(request: HttpRequest):
    
    current_path = request.path
    return render(request, 'success_sign_up.html', {'current_path': current_path})

@login_required
def welcome_page(request: HttpRequest):
    
    current_path = request.path
    return render(request, 'welcome.html', {'current_path': current_path})

@login_required
def details_page(request: HttpRequest):
    
    # Check if the authenticated user is staff
    if request.user.is_staff:
        return redirect('reception')  # Redirect staff members to the reception page
     
    account = request.user.account

    if request.method == 'POST':
        username = request.POST.get('prenom')
        password = request.POST.get('nom')
        clinic = request.POST.get('clinic')
        num_ordre = request.POST.get('ordreInput')
        specialty = request.POST.get('ageInput')
        animal = request.POST.get('animall')

        # Check for missing fields
        if not username:
            messages.error(request, "Le prénom est obligatoire.")
        if not password:
            messages.error(request, "Le nom est obligatoire.")
        if not clinic:
            messages.error(request, "La clinique est obligatoire.")
        if not num_ordre:
            messages.error(request, "Le numéro d'ordre est obligatoire.")
        if not specialty:
            messages.error(request, "La spécialité est obligatoire.")
        if not animal:
            messages.error(request, "L'animal examiné est obligatoire.")

        if username and password and clinic and num_ordre and specialty and animal:
            account.surname = username
            account.name = password
            account.nom_clinique = clinic
            account.num_ordre = num_ordre
            account.specialty = specialty
            account.animall_examined = animal
            account.save()
            messages.success(request, "Les détails ont été mis à jour avec succès.")
            return redirect('profile')

    current_path = request.path
    return render(request, 'details1.html', {'current_path': current_path})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AnimalForm

@login_required
def client_form_detail(request: HttpRequest, submission_id):
    # Check if the authenticated user is staff
    if request.user.is_staff:
        return redirect('reception')  # Redirect staff members to the reception page
    
    animal = get_object_or_404(AnimalForm, id=submission_id)
    account = request.user.account

    feedback_message = request.session.pop('feedback_message', None)  # Get the message and remove it from the session

    if animal.status == 'A répondu' :
        animal.viewed = 'Yes'
        animal.save()  
          
    if request.method == 'POST':
        rating = request.POST.get('rating')
        message = request.POST.get('message')

        if not rating or not message:
            messages.error(request, 'Please provide both a rating and a message.')
        else:
            # Save the feedback directly to the animal instance
            animal.stars = rating
            animal.feedback_text = message
            animal.status_feedback = 'Yes'
            animal.save()
            messages.success(request, 'Your feedback has been submitted successfully.')
            return redirect('profile')  # Redirect to the appropriate page after submission

    context = {
        'animal': animal,
        'id': submission_id,
        'feedback_message': feedback_message,
    }
    current_path = request.path
    return render(request, 'client_form_detail.html', {'current_path': current_path, 'context': context})

@login_required
def delete_animal(request, animal_id):
    if request.method == 'POST':
        animal = get_object_or_404(AnimalForm, id=animal_id)
        animal.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def animal_detail(request, id):
    
    # Check if the authenticated user is staff
    if not request.user.is_staff:
        return redirect('profile')  # Redirect staff members to the reception page
    
    animal = get_object_or_404(AnimalForm, id=id)
    if request.method == 'POST':
        response = request.POST.get('response')
        # Check if the response is to reject
        if response == 'reject':
            animal.status = 'Rejeté'
            animal.save()
            return redirect('reception')

        # Continue handling other responses if needed
        else:
            # Handle other responses
            animal.response = response
            animal.status = 'A répondu'
            animal.save()
            return redirect('reception')
        

    context = {
        'animal': animal,
        'id': id,
    }
    return render(request, 'animal_detail.html', context)

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import AnimalForm
import base64
from django.core.files.base import ContentFile

@login_required
def save_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        animal = get_object_or_404(AnimalForm, id=data['id'])
        figure = data['figure']
        format, imgstr = data['image'].split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name='modified_image.' + ext)
        
        if figure == 'Figure 1':
            animal.picture1 = image_data  # Or picture2, picture3 based on the context
            animal.save()
        elif figure == 'Figure 2':
            animal.picture2 = image_data  # Or picture2, picture3 based on the context
            animal.save()
        elif figure == 'Figure 3':
            animal.picture3 = image_data  # Or picture2, picture3 based on the context
            animal.save()
            
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)
