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

        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        password = form.cleaned_data['password']
        repeat_password = form.cleaned_data['repeat_password']
        if password != repeat_password:
            return render(request, 'core/registration.html',
                          {'form': form, 'error': 'Passwords are not the same.'})

        if User.objects.filter(username=username).exists():
            return render (request, 'core/registration.html',
                          {'form': form, 'error': 'Nickname "{}" already exist.'.format(username)})

        user = User.objects.create_user(email=form.cleaned_data['email'],
                                   password=password,
                                   username=username,
                                   first_name=first_name,
                                   last_name=last_name
                                   )
        if user is not None:
            user.save()
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

    if request.method == 'GET':
        return render(request, 'core/login.html',
                      {'form': LoginForm})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST['username'],
                                password=request.POST['password'])
            if user is None:
                return render(request, 'core/login.html',
                              {'error': 'Wrong login or/and password', 'form': form})
            login(request, user)
            return redirect('ask_margot')
        return render(request, 'core/login.html',
                      {'error': 'Full out the forms correctly', 'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('ask_margot')
        return render(request, 'core/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def settings_view(request):

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'core/settings.html', {'form': form, 'error': 'Something wrong with data'})

        user = request.user
        user = User.objects.update_user(user, form.cleaned_data)
        if user is None:
            return render(request, 'core/settings.html', {'form': form, 'error': 'This user already exist'})
        return redirect('settings')

    form = EditForm()
    return render(request, 'core/settings.html', {'form': form})

