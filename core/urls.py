from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from django.urls import path
from . import views
from .models import User

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view, name='registration'),

]