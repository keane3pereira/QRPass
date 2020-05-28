from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import main.views as main_views

# Create your views here.

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect(main_views.home)
    form = CustomUserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        print('user', user)
        login(request, user)
        return redirect(main_views.home)
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

def sign_out(request):
    try: del request.session[request.user.email]
    except: pass
    logout(request)
    return redirect(sign_in)

def base(request):
    return redirect(sign_out)
