from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Answer, Tag, LikeDislike
from catalog.forms import QuestionForm, AnswerForm

from django.contrib.auth import get_user_model

User = get_user_model()

def post_list(request):
    if request.GET.get('answered') is not None:
        sort_key = '-total_answers'
    else:
        sort_key = '-create_date'

    questions = Question.objects.all().order_by(sort_key)
    if len(questions) == 0:
        return render(request, 'catalog/index.html', {'error': "Be the first to ask a question!"})
    posts = my_paginator(questions, request, 3)

    return render(request, 'catalog/index.html', {'questions': posts})


def add_new_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question.objects.create_question(author=request.user, header=form.cleaned_data['header'], body_quest=form.cleaned_data['body_quest'], tags=form.cleaned_data['tags'])
            if question is not None:
                return redirect('../question/{}'.format(question.id))
        return render(request, 'catalog/ask.html', {'form':form})
    if request.method == "GET":
        form = QuestionForm()
        if request.user.is_authenticated:
            return render(request, 'catalog/ask.html', {'form': form})
    return redirect('ask_margot')


def tag_page(request, tag_id):
    try:
        tag_name = Tag.objects.get(pk=tag_id)
    except:
        return HttpResponse(status=404)
    questions = Question.objects.filter(tags=tag_name)
    posts = my_paginator(questions,request, 3)
    return render (request, 'catalog/tag.html', {'questions':posts, 'tag':tag_name})


def question_page(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except:
        return HttpResponse(status=404)
    context = {}

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create_answer(author=request.user, question=question, body_answer=form.cleaned_data['body_answer'])
            answer.save()
            return redirect('question', question.id)
        else:
            context.update({'form' : form})

    answers = Answer.objects.filter(question=question_id).order_by('-total_likes')
    form = AnswerForm()
    posts = my_paginator(answers, request, 3)
    context.update({'form': form, 'question': question, 'answers': posts})

    return render(request, 'catalog/question.html', context=context)

def my_paginator(objects_list, request, per_page):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)

    return posts

@login_required()
def vote_view(request):
    post = request.POST
    user = request.user

    vote_object, action, object_id = post['object'], post['action'], post['object_id']
    if vote_object == 'question':
        vote_object = Question.objects.get(pk=object_id)
    else:
        vote_object = Answer.objects.get(pk=object_id)
    LikeDislike.objects.create_like(user, instance=vote_object, object_id=object_id, action=action)

    return HttpResponse(vote_object.total_likes, status=200)
