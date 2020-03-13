from django.urls import path
from . import views

urlpatterns = [
    path('', views.ask_margot, name='ask_margot'),
    path('ask/', views.add_new_question, name='ask'),
    path('questions/<int:question_id>', views.question_page, name='question'),
    path('settings/', views.profile_settings, name='settings'),
    path('settings/', views.editiing_profile, name='edit'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration')
]