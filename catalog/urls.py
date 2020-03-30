from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from django.urls import path, re_path
from . import views
from .models import LikeDislike, Question, Answer, Tag

urlpatterns = [
    path('', views.post_list, name='ask_margot'),

    path('ask/', views.add_new_question, name='ask'),
    path('question/<int:question_id>', views.question_page, name='question'),


    url(r'^question/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.LIKE)),
        name='question_like'),
    url(r'^question/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.DISLIKE)),
        name='question_dislike'),
    url(r'^answer/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Answer, vote_type=LikeDislike.LIKE)),
        name='answer_like'),
    url(r'^answer/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Answer, vote_type=LikeDislike.DISLIKE)),
        name='answer_dislike'),
]

