from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from django.urls import path, re_path
from . import views
from .models import LikeDislike, Question, Answer, Tag

urlpatterns = [
    path('', views.post_list, name='ask_margot'),

    path('ask/', views.add_new_question, name='ask'),
    path('question/<int:question_id>', views.question_page, name='question'),
]

