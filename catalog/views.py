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
    # tag = Tag.objects.all()
    return render(request, 'catalog/base.html', {'questions': question, 'users': user})


def profile_settings(request):
    user = UserProfile.objects.all()
    return render(request, 'catalog/settings.html', {'user': user})




def add_new_question(request):
    if request.method  == 'GET':
        tag = Tag.objects.all()
        question = Question.objects.all()
        user = UserProfile.objects.all()
        return render(request, 'catalog/ask.html', {'tags': tag, 'questions': question, 'users': user})
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
        return render(request, 'catalog/settings.html', {'tags': tag, 'users': users})
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
                  {'questions': question, 'tags': tags, 'users': user, 'answers': answer})


def login(request): #exit
    user = UserProfile.objects.all()
    return render(request, 'catalog/login.html', {'user' : user})

def registration(requset):
    return render(requset, 'catalog/registration.html')