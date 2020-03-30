from django.conf.global_settings import AUTHENTICATION_BACKENDS
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()



# Create your views here.

def registration_view(request):
    class RegistrationForm(forms.Form):
        username = forms.CharField()
        first_name = forms.CharField()
        last_name = forms.CharField()
        email = forms.EmailField()

        password = forms.CharField(widget=forms.PasswordInput)
        repeat_password = forms.CharField(widget=forms.PasswordInput)
        # avatar = forms.ImageField()

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
    class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput())

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
                              {'error': 'Неверный логин и/или пароль', 'form': form})
            login(request, user)
            return redirect('ask_margot')
        return render(request, 'core/login.html',
                      {'error': 'Заполните формы корректно', 'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('ask_margot')
        return render(request, 'core/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def settings_view(request):
    class EditForm(forms.Form):
        username = forms.CharField(required=False)
        first_name = forms.CharField(required=False)
        last_name = forms.CharField(required=False)
        email = forms.EmailField(required=False)

        password = forms.CharField(widget=forms.PasswordInput, required=False)
        # avatar = forms.ImageField()

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'core/settings.html', {'form': form, 'error': 'Something wrong with data'})

        user = request.user
        User.objects.update_user(user, form.cleaned_data)
        return redirect('settings')

    form = EditForm()
    return render(request, 'core/settings.html', {'form': form})

