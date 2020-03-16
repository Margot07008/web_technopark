from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Question, UserProfile, Tag, Answer


# Create your views here.
def ask_margot(request):
    questions = Question.objects.all().order_by('-create_date')
    user = UserProfile.objects.all()
    tag = Tag.objects.all()
    return render(request, 'catalog/index.html', {'questions': questions})


# Create your views here.
def ask_margot_not_log(request):
    question = Question.objects.all()
    user = UserProfile.objects.all()
    # tag = Tag.objects.all()
    return render(request, 'catalog/base.html', {'questions': question})


def profile_settings(request):
    user = UserProfile.objects.all()
    return render(request, 'catalog/settings.html', {'user': user})


def add_new_question(request):
    if request.method == 'GET':
        tag = Tag.objects.all()
        question = Question.objects.all()
        user = UserProfile.objects.all()
        return render(request, 'catalog/ask.html',
                      {'tags': tag, 'questions': question, 'users': user})
    elif request.method == "POST":
        q = Question.objects.create(
            author=request.user,
            header=request.POST.get("title"),
            body_quest=request.POST.get("text")
        )
        # q.tag = request.POST.set("tags")
        q.save()

    return redirect('ask_margot')


def editiing_profile(request):
    if request.method == 'GET':
        tag = Tag.objects.all()
        users = UserProfile.objects.all()
        return render(request, 'catalog/settings.html',
                      {'tags': tag, 'users': users})
    elif request.method == "POST":
        u = request.user
        u.nickname = request.POST.get('nickname')
        u.email = request.POST.get('email')
        u.profile_image = request.POST.get('img')
        u.login = request.POST.get('login')

        u.save()

    return redirect('/settings')


def question_page(request, question_id):
    user = UserProfile.objects.all()
    question = Question.objects.get(id=question_id)
    tags = question.tag.all()
    answer = Answer.objects.filter(question_id=question_id)

    return render(request, 'catalog/question.html',
                  {'questions': question, 'answers': answer})


def login_view(request):
    class LoginForm(forms.Form):
        login = forms.CharField()
        password = forms.CharField()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])
            if user is None:
                return render(request, 'catalog/login.html',
                              {'error': 'Неверный логин и/или пароль'})
            login(request, user)
            return redirect('ask_margot')
        return render(request, 'catalog/login.html',
                      {'error': 'Заполните формы корректно'})
    else:
        if request.user.is_authenticated:
            return redirect('ask_margot')
        return render(request, 'catalog/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('ask_margot')


def registration_view(request):
    class RegistrationForm(forms.Form):
        login = forms.CharField()
        email = forms.EmailField()
        nickname = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput())
        repeat_password = forms.CharField(widget=forms.PasswordInput())
        avatar = forms.ImageField()

    if request.method == 'GET':
        return render(request, 'catalog/registration.html',
                      {'form': RegistrationForm})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'catalog/registration.html', {'form': form})

        username = form.cleaned_data['nickname']
        password = form.cleaned_data['password']
        repeat_password = form.cleaned_data['repeat_password']
        if password != repeat_password:
            return render(request, 'catalog/registration.html',
                          {'form': form, 'error': 'Пароли не совпадают'})

        user = User.objects.create(email=form.cleaned_data['email'],
                                   password=password,
                                   username=username)
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('ask_margot')
    else:
        return HttpResponse(status=405)
