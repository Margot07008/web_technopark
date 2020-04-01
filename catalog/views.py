from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Answer
from catalog.forms import QuestionForm, AnswerForm

from django.contrib.auth import get_user_model

User = get_user_model()

def post_list(request):
    if request.GET.get('answered') is not None:
        sort_key = '-total_answers'
    else:
        sort_key = '-create_date'

    object_list = Question.objects.all().order_by(sort_key)
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


def add_new_question(request):
    if request.method == "POST":

        form = QuestionForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags'].split()
            question = Question.objects.create_question(author=request.user, header=form.cleaned_data['header'], body_quest=form.cleaned_data['body_quest'], tags=tags)
            if question is not None:
                question.save()
                return redirect('../question/{}'.format(question.id))
            return render(request, 'catalog/ask.html', {'error': 'Something went wrong. Try again.'})

    form = QuestionForm()
    return render(request, 'catalog/ask.html', {'form': form})




def question_page(request, question_id):
    question = Question.objects.get(pk=question_id)
    context = {}

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create_answer(author=request.user, question=question, body_answer=form.cleaned_data['body_answer'])
            answer.save()
            return redirect('question', question.id)
        else:
            context.update({'error' : 'Invalid answer`s data'})

    answers = Answer.objects.filter(question=question_id).order_by('-create_date')
    form = AnswerForm()


    paginator = Paginator(answers, 3)  # 3 поста на каждой странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)

    context.update({'form': form, 'question': question, 'answers': posts})
    # return render(request,
    #               'catalog/question.html', {'page': page, 'questions': question, 'answers': posts})

    # my_paginator(request, answers,context, 3, 'catalog/question.html')

    return render(request, 'catalog/question.html', context=context)


# def my_paginator(request, object_list, context, count, src):
#
#     paginator = Paginator(object_list, count)  # count постов на каждой странице
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # Если страница не является целым числом, поставим первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Если страница больше максимальной, доставить последнюю страницу результатов
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   src, {'page': page, 'iteration_list': posts}, context)

