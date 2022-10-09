from email.policy import default
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    chatname = models.CharField(max_length=100)

    def __str__(self):
        return self.chatname


class Users(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp")
    chatroom = models.ManyToManyField(ChatRoom)

    def __str__(self):
        return self.username.username


class Messages(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
