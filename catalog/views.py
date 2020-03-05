from django.shortcuts import render

from .models import Question, UserProfile, Tag


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


def ask_margot_ask(request):
    tag = Tag.objects.all()
    return render(request, 'catalog/ask.html', {'tags': tag})
