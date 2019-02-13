from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from users.forms import UserRegistrationForm
from users.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
from django.conf import settings
import requests
from django.contrib import messages

# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Create an Account"
        form = UserRegistrationForm(
            request.POST or None,
            request.FILES or None
            )

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)

            return HttpResponseRedirect(reverse('home_page'))

        context = {"title": title, "form": form}

        return render(request, "users/form.html", context)



def user_login(request):
    context = {}
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']


        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''

        if result['success']:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('user_success'))
            else:
                context["error"] = "Provide valid credentials !!"
                return render(request, "users/login.html", context)
        else:
            context["error"] = "Please fill the captcha"
            return render(request, "users/login.html", context)

    else:
        return render(request, "users/login.html", context)

# def user_login(request):
#     context = {}
#     if request.method == "POST":
#
#         username_get = request.POST['username']
#         password_get = request.POST['password']
#
#
#         ''' Begin reCAPTCHA validation '''
#         recaptcha_response = request.POST.get('g-recaptcha-response')
#         data = {
#             'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#             'response': recaptcha_response
#         }
#         r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
#         result = r.json()
#         ''' End reCAPTCHA validation '''
#
#         if result['success']:
#
#             username = request.user.username
#             password = request.user.password
#
#             if username_get==username and password_get==password:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('user_success'))
#             else:
#                 context["error"] = "Provide valid credentials !!"
#                 return render(request, "users/login.html", context)
#         else:
#             context["error"] = "Please fill the captcha"
#             return render(request, "users/login.html", context)
#
#     else:
#         return render(request, "users/login.html", context)

@login_required(login_url="/login/")
def success(request):
    context = {}
    context['user'] = request.user
    return render(request, "users/success.html", context)



def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))