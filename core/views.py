from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


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
        return render(request, 'catalog/registration.html',
                      {'form': RegistrationForm})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'catalog/registration.html', {'form': form})

        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        password = form.cleaned_data['password']
        repeat_password = form.cleaned_data['repeat_password']
        if password != repeat_password:
            return render(request, 'catalog/registration.html',
                          {'form': form, 'error': 'Пароли не совпадают'})

        if User.objects.filter(username=username).exists():
            return render (request, 'catalog/registration.html',
                          {'form': form, 'error': 'Пользователь уже существует'})
        user = User.objects.create(email=form.cleaned_data['email'],
                                   password=password,
                                   username=username,
                                   first_name=first_name,
                                   last_name=last_name
                                   )
        login(request, user)
        return redirect('ask_margot')
    else:
        return HttpResponse(status=405)


def login_view(request):
    class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput())

    if request.method == 'GET':
        return render(request, 'catalog/login.html',
                      {'form': LoginForm})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is None:
                return render(request, 'catalog/login.html',
                              {'error': 'Неверный логин и/или пароль', 'form': form})
            login(request, user)
            return redirect('ask_margot')
        return render(request, 'catalog/login.html',
                      {'error': 'Заполните формы корректно', 'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('ask_margot')
        return render(request, 'catalog/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('ask_margot')

