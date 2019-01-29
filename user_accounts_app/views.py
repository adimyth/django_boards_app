from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login
from user_accounts_app.forms import SignUpForm, LoginForm
from board_app.models import User, Topic


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # user is created with the filled form data
            form.save(commit=True)
            # authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request=request, username=username, password=password)
            # redirecting to login page
            login(request, user)
            redirect(reverse('board_app:home'))
    else:
        form = SignUpForm()
    return render(request, 'user_accounts_app/signup.html', {'form': form})


def login_form(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            # redirecting to login page
            login(request, user)
            return redirect(reverse('board_app:home'))
        else:
            # generating appropriate response for the user while trying to login with invalid creds
            try:
                User.objects.get(username=username)
                User.objects.get(password=password)
            except Exception:
                error_stmt = 'Invalid credentials'
            return render(request, 'user_accounts_app/login.html', {'form': form, 'error': error_stmt})
    return render(request, 'user_accounts_app/login.html', {'form': form})
