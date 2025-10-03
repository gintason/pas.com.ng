from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.views import View
from django.contrib.auth.forms import PasswordResetForm


# Create your views here.

def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error=True
            messages.error(request, 'A User with this username already exists')
        
        if User.objects.filter(email=email).exists():
            user_data_has_error=True
            messages.error(request, "This email is already taken by another user")
        
        if len(password) < 5:
            user_data_has_error=True
            messages.error(request, 'Password is too short')
        
        if confirm_password != password:
            user_data_has_error = True
            messages.error(request, 'Passwords do not match!')
        
        if len(username) > 7:
            user_data_has_error=True
            messages.error(request, 'Please username should not be more than 7 characters')
        
        if not user_data_has_error:
            new_user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
            password = password
            )
            messages.success(request, 'Account created. Login now')
            return redirect('users:login')
        else:
            return render(request, 'users/register.html')
        
    return render(request, 'users/register.html')

def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            # login user if login credentials are correct
            login(request, user)

            # ewdirect to home page
            return redirect('pasApp:home')
        else:
            # redirect back to the login page if credentials are wrong
            messages.error(request, 'Invalid email or password')
            return redirect('users:login')

    return render(request, 'users/login.html')



def LogoutView(request):

        logout(request)

        # redirect to login page after logout
        return redirect('users:login')


# 🔹 Password Reset Views 

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('users:reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            #to get the full password reset url
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'


            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'


            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] ) # email receiver

            email_message.fail_silently = True
            email_message.send()

            return redirect('users:password-reset-sent', reset_id = new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('users:forgot-password')
        

    return render(request, 'users/forgot_password.html')

def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
           return render(request, 'users/password_reset_sent.html')
    else:
          # redirect to forgot password page if code does not exist
          messages.error(request, 'Invalid reset id')
          return redirect('users:forgot-password')
        

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

        # check to make sure link has not expired
            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')
                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                # delete reset id after use
                reset_id.delete()

                # redirect to login
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('users:login')
            else:
                # redirect back to password reset page and display errors
                return redirect('users:reset-password', reset_id=reset_id)

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    return render(request, 'users/reset_password.html', {'reset_id': reset_id})


