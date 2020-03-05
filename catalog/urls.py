from django.urls import path
from . import views

urlpatterns = [
    path('', views.ask_margot, name='ask_margot'),
   # path('', views.ask_margot_not_log, name='ask_margot'),
    path('ask/', views.ask_margot_ask, name='ask')
]