from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage
import json
import requests
from geopy.geocoders import Nominatim
from io import BytesIO
import PyPDF2
from transformers import BartTokenizer, BartForConditionalGeneration
from .models import AIUseCase
from .summarizer import summarize_pdf  
from django.core.exceptions import ValidationError

# Custom JSON Encoder for datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timezone.datetime):
            return obj.isoformat()
        return super().default(obj)

# Utility functions
def geocode_address(address):
    geolocator = Nominatim(user_agent="HospitalFinder")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None

def find_nearest_hospitals(lat, lng):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node
      ["amenity"="hospital"]
      (around:5000,{lat},{lng});
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    hospitals = [{'name': element['tags'].get('name', 'Unnamed Hospital'),
                  'lat': element['lat'],
                  'lng': element['lon']} for element in data['elements'][:12]]
    return hospitals

@login_required
def user_setting(request):
    return render(request, 'User/setting.html')

# Views
def home(request):
    return render(request, 'index.html')

def team(request):
    return render(request, 'Team.html')

def service(request):
    return render(request, 'service.html')

def question(request):
    return render(request, 'question.html')

def redirect_team(request):
    return HttpResponseRedirect('/team/')

def redirect_signup(request):
    return HttpResponseRedirect('/signup/')

def redirect_service(request):
    return HttpResponseRedirect('/service/')

def redirect_question(request):
    return HttpResponseRedirect('/question/')

def some_view(request):
    current_time = timezone.now().isoformat()
    response_data = {'current_time': current_time}
    return JsonResponse(response_data)

@login_required
def user_home(request):
    context = {
        'username': request.user.get_full_name(),
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'profile_image': getattr(request.user, 'profile_image', None),
    }
    return render(request, 'User/UserHome.html', context)

@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        # Getting form data
        username = request.POST.get('name')
        email = request.POST.get('email')
        bio = request.POST.get('bio', '')

        # Updating user object with first and last name (if full name provided)
        if username:
            user.first_name, user.last_name = username.split(' ', 1) if ' ' in username else (username, '')

        user.email = email

        # Handling profile image upload
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            user.profile_image = profile_image  # Assuming the User model has a profile_image field

        # Updating profile bio if it exists
        if hasattr(user, 'profile'):
            user.profile.bio = bio
            user.profile.save()

        # Save the user object
        user.save()

        # Success message and redirect
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')

    else:
        # On GET request, render the profile page with user details
        context = {
            'username': user.get_full_name(),
            'email': user.email,
            'bio': getattr(user.profile, 'bio', '') if hasattr(user, 'profile') else '',
            'date_joined': user.date_joined,
            'profile_image': getattr(user, 'profile_image', None),
        }
        return render(request, 'User/UserProfile.html', context)

@login_required
def user_dashboard(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pdf_file = request.FILES['pdf_file']
                fs = FileSystemStorage()
                filename = fs.save(pdf_file.name, pdf_file)
                file_path = fs.path(filename)
                
                summary = summarize_pdf(file_path)
                key_points = extract_key_points(summary)
                
                fs.delete(filename)
                
                context = {
                    'form': form,
                    'summary': summary,
                    'key_points': key_points,
                    'username': request.user.get_full_name(),
                    'email': request.user.email,
                    'date_joined': request.user.date_joined,
                    'profile_image': getattr(request.user, 'profile_image', None),
                }
                return render(request, 'User/dashboard.html', context)
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = UploadFileForm()
    
    context = {
        'form': form,
        'username': request.user.get_full_name(),
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'profile_image': getattr(request.user, 'profile_image', None),
    }
    return render(request, 'User/dashboard.html', context)

@login_required
def text_summarization(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pdf_file = request.FILES['pdf_file']
                fs = FileSystemStorage()
                filename = fs.save(pdf_file.name, pdf_file)
                file_path = fs.path(filename)
                
                summary = summarize_pdf(file_path)
                key_points = extract_key_points(summary)
                
                fs.delete(filename)
                
                context = {
                    'form': form,
                    'summary': summary,
                    'key_points': key_points,
                }
                return render(request, 'User/text_sum.html', context)
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = UploadFileForm()
    
    context = {
        'form': form,
    }
    return render(request, 'User/text_sum.html', context)

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')

@login_required
def ai_usecase_detail(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    usecase = get_object_or_404(AIUseCase, id=id)
    return render(request, 'ai_usecase_detail.html', {'usecase': usecase})

@login_required
def ai_usecase_create(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        # Process form data here
        pass

    return render(request, 'ai_usecase_form.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup.html')

        user = User.objects.create_user(
            username=username, 
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return redirect('user_home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')

@csrf_exempt
def find_hospital(request):
    if request.method == 'GET':
        return render(request, 'hosp.html')
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            address = data.get('address')
            lat_lng = geocode_address(address)
            if lat_lng:
                lat, lng = lat_lng
                hospitals = find_nearest_hospitals(lat, lng)
                if hospitals:
                    return JsonResponse({'success': True, 'hospitals': hospitals})
                else:
                    return JsonResponse({'success': False, 'message': 'No hospitals found nearby.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid address.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
