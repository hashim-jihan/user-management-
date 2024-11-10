from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .forms import SignupPage, LoginPage



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userSignup(request):

    if request.user.is_authenticated:
          return redirect('userHome')

    if request.method == 'POST':
        form = SignupPage(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created Successfully!')
            return redirect('userLogin')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignupPage()

    return render(request, 'users/signup.html', {
        'forms': form
        })



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userLogin(request):
    if request.user.is_authenticated:
        return redirect('userHome')

    if request.method == 'POST':
        logform = LoginPage(request.POST)

        if logform.is_valid():
            username = logform.cleaned_data['username']
            password = logform.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    messages.error(request,'Admin can be logged in here!')
                    return redirect('adminLogin')
                else:

                    login(request, user)
                    return redirect('userHome')
            else:
                messages.error(request, 'Invalid username or password ')
    else:
        logform = LoginPage()

    return render(request, 'users/login.html', {
        'logform': logform
        })

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userHome(request):
    if request.user.is_superuser:
        return redirect ('adminHome')
    
    username = request.user.username
    return render(request, 'users/home.html', {
        'username': username  
    })


def userLogout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out ')
    return redirect('userLogin')
