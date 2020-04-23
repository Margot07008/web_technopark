from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from core.forms import LoginForm, RegistrationForm, EditForm


User = get_user_model()


def registration_view(request):

    if request.method == 'GET':
        return render(request, 'core/registration.html',
                      {'form': RegistrationForm})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'core/registration.html', {'form': form})

        print(form.cleaned_data)
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user = User.objects.create_user(email=email,
                                   password=password,
                                   username=username,
                                   first_name=first_name,
                                   last_name=last_name
                                   )
        if user is not None:
            # user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('ask_margot')
        else:
            return render(request, 'core/registration.html',
                          {'form': form, 'error': 'Server error'})
    else:
        return HttpResponse(status=405)


def login_view(request):

    if request.user.is_authenticated:
        return redirect('ask_margot')
    if request.method == 'GET':
        return render(request, 'core/login.html',
                      {'form': LoginForm})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,
                                password=password)
            if user is None:
                return render(request, 'core/login.html',
                              {'error': 'Wrong login or/and password', 'form': form})

            login(request, user)
            return redirect('ask_margot')
        return render(request, 'core/login.html',
                      {'form': form})
    else:
        return render(request, 'core/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def settings_view(request):

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'core/settings.html', {'form': form})

        user = request.user
        User.objects.update_user(user, form.cleaned_data)
        return redirect('settings')

    if request.method == "GET":
        form = EditForm()
        if request.user.is_authenticated:
            return render(request, 'core/settings.html', {'form': form})
    return redirect('ask_margot')


