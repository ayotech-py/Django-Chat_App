from urllib.parse import urlparse
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatapp, name='chatapp'),
    path('chatroom/<str:name>/', views.chatroom, name='chatroom'),
]
