from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as login_method, logout as logout_method
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from . models import PasswordReset

def login(req):

    if req.user.is_authenticated: 
        return HttpResponseRedirect(reverse('home:home'))

    context = {}
    if req.method == 'POST':
        username = req.POST['login-username']
        password = req.POST['login-password']

        user = authenticate(req, username=username, password=password)

        if user:
            login_method(req, user)
            return HttpResponseRedirect(reverse('home:home'))
        else:
            context = {
                'message': 'Username or password are incorrect.'
            }
            
    return render(req, 'login.html', context)

def logout(req):
    logout_method(req)
    return render(req, 'login.html')

def signup(req):

    if req.user.is_authenticated: 
        return HttpResponseRedirect(reverse('home:home'))

    context = {}
    if req.method == 'POST':

        firstname = req.POST['first_name']
        lastname = req.POST['last_name']
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        password_confirm = req.POST['password_confirm']

        is_staff = req.POST['is_staff']

        if password == password_confirm: 
            if User.objects.filter(username=username).exists(): 
                context = {
                    'message': 'User already exists'
                }
            else:
                if is_staff == 'staff': 
                        User.objects.create_superuser(
                            username, email, password, first_name=firstname, last_name=lastname
                        )
                        context = {
                            'message': 'Staff user has been created'
                        }
                else:
                    User.objects.create_user(
                        username, email, password, first_name=firstname, last_name=lastname
                    )
                    context = {
                        'message': 'User has been created'
                    }
        else:
            context = {
                'message': 'Passwords did not match.'
            }
    return render(req, 'signup.html', context)

def request_reset_password(req):
    context = {}
    if req.method == 'POST':
        email = req.POST['reset-email']
        is_email_valid = User.objects.filter(email=email).exists()

        if is_email_valid: 
            new_request = PasswordReset()
            new_request.email = email
            new_request.save()
            print(new_request) 
            return HttpResponseRedirect(reverse('password_reset'))

        else:
            context = {
                'message': 'The email does not exist'
            }


    return render(req, 'request_reset_password.html', context)

def password_reset(req):
    context = {}

    if req.method == 'POST':
        token = req.POST['pass-reset-token']
        email = req.POST['pass-reset-email']
        password = req.POST['pass-reset-password']
        password_confirm = req.POST['pass-reset-password-confirm']

        if password == password_confirm: 
            valid_token = PasswordReset.objects.filter(token=token, active=True).exists()
            valid_user = User.objects.filter(email=email).exists()

            if valid_token and valid_user: 
                db_token = PasswordReset.objects.get(token=token)
                db_token.active = False
                db_token.save()

                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()

                context = {
                    'success_message': f'Your password has been changed!',
                    'message': False
                }
            else:
                context = {
                    'message': 'Invalid token or email.'
                }
        else:
            context = {
                'message': 'Passwords do not match.'
            }

    return render(req, 'password_reset.html', context)

def change_password(req):
    context = {}

    if req.method == 'POST':
        username = req.user.get_username()
        current_password = req.POST['change-current-password']
        new_password = req.POST['change-new-password']
        new_password_confirm = req.POST['change-new-password-confirm']

        if new_password == new_password_confirm: 
            valid_user = authenticate(req, username=username, password=current_password)
            if valid_user: 
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                context = {
                    'message': 'Your password has been updated'
                }
            else:
                context = {
                    'message': 'Current password is wrong.'
                }
        else:
            context = {
                'message': 'Your new password do not match.'
            }

    return render(req, 'change_password.html', context)

def delete_account(req):
    context = {}
    if req.method == 'POST':
        username = req.user.get_username()
        password = req.POST['delete-password']
        text_delete = req.POST['delete-confirm']
        valid_user = authenticate(req, username=username, password=password)
        if valid_user: 
            if text_delete == 'delete':
                logout_method(req)
                user = User.objects.get(username=username)
                user.delete()
                return HttpResponseRedirect(reverse('login'))
            else:
                context = {
                    'message': '\'delete\' was not typed correctly.'
                }
        else:
            context = {
                'message': 'Wrong password.'
            }

    return render(req, 'delete_account.html', context)
    