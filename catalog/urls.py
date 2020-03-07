from django.urls import path
from . import views

urlpatterns = [
    path('', views.ask_margot, name='ask_margot'),
    path('ask/', views.ask_question, name='ask'),
    path('views.py', views.add_new_question, name='add_new_question'),
    path('question/', views.question_page, name='question'),
    path('settings/', views.profile_settings, name='settings'),
]