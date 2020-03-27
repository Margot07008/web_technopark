from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import json

from django.views import View
from django.contrib.contenttypes.models import ContentType

from .models import Question, Tag, Answer, LikeDislike

from django.contrib.auth import get_user_model
User = get_user_model()


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



# Create your views here.
def ask_margot_not_log(request):
    question = Question.objects.all()
    user = User.objects.all()
    # tag = Tag.objects.all()
    return render(request, 'catalog/base.html', {'questions': question})



def add_new_question(request):
    if request.method == 'GET':
        tag = Tag.objects.all()
        question = Question.objects.all()
        user = User.objects.all()
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