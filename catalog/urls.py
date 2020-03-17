from django.urls import path
from . import views

urlpatterns = [
    path('', views.ask_margot, name='ask_margot'),
    path('ask/', views.add_new_question, name='ask'),
    path('question/<int:question_id>', views.question_page, name='question'),
    # path('question/<int:question_id>', views.add_new_answer, name='new_answer'),
    # path('settings/', views.profile_settings, name='settings'),
    # path('settings/', views.editiing_profile, name='edit'),
    path('settings/', views.settings_view, name='settings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view, name='registration')
]
