from django.shortcuts import render, redirect

from .models import Question, UserProfile, Tag, Answer


# Create your views here.
def ask_margot(request):
    question = Question.objects.all().order_by('-create_date')
    user = UserProfile.objects.all()
    tag = Tag.objects.all()
    return render(request, 'catalog/index.html', {'questions': question, 'users': user, 'tags': tag})


# Create your views here.
def ask_margot_not_log(request):
    question = Question.objects.all()
    user = UserProfile.objects.all()
    tag = Tag.objects.all()
    return render(request, 'catalog/base.html', {'questions': question, 'users': user, 'tags': tag})


def ask_question(request):
    tag = Tag.objects.all()
    question = Question.objects.all()
    user = UserProfile.objects.all()
    return render(request, 'catalog/ask.html', {'tags': tag, 'questions': question, 'users': user})

def add_new_question(request):
    if request.method =="POST":
        q = Question()
        q.author = "user_name"
        q.header = request.POST.get("title")
        q.body_quest = request.POST.get("text")
        # q.tag = request.POST.set("tags")
        q.save()
    return redirect('catalog/index.html')

def question_page(request):

    tag = Tag.objects.all()
    user = UserProfile.objects.all()
    new_id = request.GET.get("question_page", "")
    question = Question.objects.get(id = new_id)
    answer = Answer.objects.get(question = question.id)

    return render(request, 'catalog/question.html', {'questions': question, 'tags': tag, 'users': user, 'answers':answer})



