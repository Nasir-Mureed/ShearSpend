from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
import re
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import logging

from Partners.models import Partner

def register_view(request):
    if request.method == 'POST':
        # Extract form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')  # Fixed typo
        confirm_password = request.POST.get('confirm_password', '')
        
        # Initialize errors dictionary
        errors = {}
        
        # Validate username
        if not username:
            errors['username'] = 'Username is required.'
        elif len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters long.'
        elif len(username) > 150:
            errors['username'] = 'Username must be less than 150 characters.'
        elif not re.match(r'^[\w.@+-]+$', username):
            errors['username'] = 'Username contains invalid characters.'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'This username is already taken.'
        
        # Validate email
        if not email:
            errors['email'] = 'Email address is required.'
        else:
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    errors['email'] = 'This email is already registered.'
            except ValidationError:
                errors['email'] = 'Please enter a valid email address.'
        
        # Validate password
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'
        elif not any(char.isdigit() for char in password):
            errors['password'] = 'Password must contain at least one number.'
        elif not any(char.isupper() for char in password):
            errors['password'] = 'Password must contain at least one uppercase letter.'
        elif not any(char.islower() for char in password):
            errors['password'] = 'Password must contain at least one lowercase letter.'
        
        # Validate password confirmation
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'
        
        # If there are errors, return to form with error messages
        if errors:
            # Store error messages in Django's messages framework
            for field, error_message in errors.items():
                messages.error(request, f"{field.capitalize()}: {error_message}")
            
            # Return to registration page with previously entered data
            return render(request, 'Authentication/register.html', {
                'username': username,
                'email': email,
                'errors': errors
            })        
        # Create user (everything is valid)
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            Partner.objects.create(name=username, user_id=user.id)  # Create a Partner object for the new user

            # Optional: Automatically log in the user
            # from django.contrib.auth import login
            login(request, user)
            
            messages.success(
                request, 
                'Registration successful! You can now log in.',
                extra_tags='success'
            )            
            return redirect('Dashboard:dashboard')            
        except IntegrityError:
            # Handle database integrity errors
            messages.error(
                request,
                'An error occurred during registration. Please try again.'
            )
            return render(request, 'Authentication/register.html', {
                'username': username,
                'email': email
            })        
        except Exception as e:
            # Log the actual error for debugging (don't show to user)
            # logger.error(f"Registration error: {str(e)}")            
            messages.error(
                request,
                'An unexpected error occurred. Please try again later.'
            )
            return render(request, 'Authentication/register.html')
    
    # GET request - show empty registration form
    return render(request, 'Authentication/register.html')



# Set up logging
logger = logging.getLogger(__name__)

@sensitive_post_parameters('password')
@never_cache
def login_view(request):
    # Redirect if user is already authenticated
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('Dashboard:dashboard')
    
    if request.method == 'POST':
        # Extract and sanitize input
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me', False)
        
        # Initialize validation errors
        errors = {}
        
        # Validate input
        if not username:
            errors['username'] = 'Username is required.'
        
        if not password:
            errors['password'] = 'Password is required.'
        
        # If validation fails, return with errors
        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            return render(request, 'Authentication/login.html', {
                'username': username,
                'remember_me': remember_me,
                'errors': errors
            })
        
        # Attempt authentication
        try:
            # Check if user exists (optional - gives different error message)
            user_exists = User.objects.filter(username=username).exists()
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Successful authentication
                login(request, user)
                
                # Handle "Remember Me" functionality
                if not remember_me:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                else:
                    # Session lasts for 2 weeks (1209600 seconds)
                    request.session.set_expiry(1209600)
                
                # Log successful login
                logger.info(f"Successful login for user: {username} from IP: {get_client_ip(request)}")
                
                # Check for next parameter (redirect to requested page after login)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                # Success message
                messages.success(request, f'Welcome back, {user.username}!')
                
                return redirect('Dashboard:dashboard')
            else:
                # Failed authentication
                if user_exists:
                    # User exists but wrong password
                    error_msg = 'Incorrect password. Please try again.'
                    logger.warning(f"Failed login attempt for existing user: {username} from IP: {get_client_ip(request)}")
                else:
                    # User doesn't exist
                    error_msg = 'Username does not exist. Please check your username or register.'
                    logger.warning(f"Failed login attempt for non-existent user: {username} from IP: {get_client_ip(request)}")
                
                # Add delay to prevent brute force attacks (optional)
                import time
                time.sleep(1)  # 1 second delay
                
                messages.error(request, error_msg)
                
                return render(request, 'Authentication/login.html', {
                    'username': username,
                    'remember_me': remember_me
                })
                
        except Exception as e:
            # Log the actual error for debugging
            logger.error(f"Login error for user {username}: {str(e)}")
            
            # User-friendly error message
            messages.error(
                request, 
                'An unexpected error occurred. Please try again later.'
            )
            
            return render(request, 'Authentication/login.html', {
                'username': username
            })
    
    # GET request - show login form
    return render(request, 'Authentication/login.html', {
        'next': request.GET.get('next', '')
    })

# Helper function to get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def logout_view(request):
    logout(request)
    request.session.flush()  # Clear session data
    messages.info(request, 'You have been logged out.')
    return redirect('Dashboard:home')