from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import json

from django.views import View
from django.contrib.contenttypes.models import ContentType

from .models import Question, UserProfile, Tag, Answer, LikeDislike


# Create your views here.

def post_list(request):
    object_list = Question.objects.all().order_by('-create_date')
    paginator = Paginator(object_list, 3)  # 3 поста на каждой странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request,
	          'catalog/index.html', {'page': page, 'questions': posts})


# def ask_margot(request):
#     questions = Question.objects.all().order_by('-create_date')
#     return render(request, 'catalog/index.html', {'questions': questions})


# Create your views here.
def ask_margot_not_log(request):
    question = Question.objects.all()
    user = UserProfile.objects.all()
    # tag = Tag.objects.all()
    return render(request, 'catalog/base.html', {'questions': question})



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



def question_page(request, question_id):
    if request.method == 'GET':
        question = Question.objects.get(id=question_id)
        object_list = Answer.objects.filter(question_id=question_id).order_by('-create_date')
        paginator = Paginator(object_list, 3)  # 3 поста на каждой странице
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом, поставим первую страницу
            posts = paginator.page(1)
        except EmptyPage:
            # Если страница больше максимальной, доставить последнюю страницу результатов
            posts = paginator.page(paginator.num_pages)
        return render(request,
                      'catalog/question.html', {'page': page, 'questions': question, 'answers': posts})

    elif request.method == "POST":
        a = Answer.objects.create(
            author=request.user,
            question_id=question_id,
            body_answer=request.POST.get("text")
        )
        a.save()

    return redirect('question', question_id)





def login_view(request):
    class LoginForm(forms.Form):
        login = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput())

    if request.method == 'GET':
        return render(request, 'catalog/login.html',
                      {'form': LoginForm})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
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


@login_required(login_url='/login')
def settings_view(request):
    class EditProfileForm(forms.Form):
        login = forms.CharField(label='Username',required=False)
        email = forms.EmailField(label='Email', required=False)
        nickname = forms.CharField(label='nickname', required=False)
        avatar = forms.ImageField(required=False)

    context={}

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if not form.is_valid():
            context.update({'error' : 'Something wrong with data', 'form' : EditProfileForm()})
            return render(request,'catalog/settings.html',context=context)

        user = request.user
        temp_user =  UserProfile.objects.get(user=request.user)
        temp_user.login = request.POST['login']
        temp_user.email = request.POST['email']
        temp_user.nickname = request.POST['nickname']
        temp_user.save()
        return redirect('ask_margot')
    form = EditProfileForm()
    context.update({'form':form})
    return render(request, 'catalog/settings.html', context=context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('ask_margot')


def registration_view(request):
    class RegistrationForm(forms.Form):
        login = forms.CharField()
        email = forms.EmailField()
        nickname = forms.CharField()
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


class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )