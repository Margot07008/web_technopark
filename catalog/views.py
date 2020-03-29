from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import json

from django.views import View
from django.contrib.contenttypes.models import ContentType

from .models import Question, Tag, Answer, LikeDislike

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
        header = request.POST.get("header")
        body_quest = request.POST.get("body_quest")
        question = Question.objects.create_question(author=request.user, header=header, body_quest=body_quest)
        if question is not None:
            question.save()
            print('kek')
            return redirect('../question/{}'.format(question.id))
        return render(request, 'catalog/ask.html', {'error': 'Something went wrong. Try again.'})
    return render(request, 'catalog/ask.html')


class AnswerForm(forms.Form):
    body_answer = forms.CharField(label='Your anwer', widget=forms.Textarea(attrs={'rows':'3'}))



def question_page(request, question_id):
    print(request.user)
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