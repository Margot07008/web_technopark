from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='ask_margot'),
    path('ask/', views.add_new_question, name='ask'),
    path('question/<int:question_id>', views.question_page, name='question'),
]

