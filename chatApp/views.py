from django.shortcuts import render, redirect
from .models import ChatRoom, Messages, Users
from django.contrib import messages
from django.contrib.auth.models import User, auth


def chatapp(request):
    if request.method == 'POST':
        chatroom = request.POST['roomname']
        username = request.user.id
        realname = request.user
        if ChatRoom.objects.filter(chatname=chatroom).exists():
            chatname = ChatRoom.objects.filter(chatname=chatroom)
            if Users.objects.filter(username=username).exists():
                user = Users.objects.get(username=username)
                user.chatroom.set(chatname)
            else:
                user = Users.objects.create(username=realname)
                user.chatroom.set(chatname)
            return redirect('chatroom/'+chatroom)
        else:
            chatname = ChatRoom.objects.create(chatname=chatroom)
            chatname.save()
            chatname = ChatRoom.objects.filter(chatname=chatroom)
            user = Users.objects.create(username=username)
            user.chatroom.set(chatname)
            return redirect('chatroom/'+chatroom)
    else:
        return render(request, 'chatapp.html')


def chatroom(request, name):
    username = request.user.id
    chatname = ChatRoom.objects.get(chatname=name)
    all_messages = Messages.objects.filter(chatroom=chatname)
    user = Users.objects.get(username=username)

    if request.method == 'POST':
        messages = request.POST['messages']
        user = Users.objects.get(username=username)
        delivered_message = Messages.objects.create(
            message=messages, user=user, chatroom=chatname)
        delivered_message.save()
        all_messages = Messages.objects.filter(chatroom=chatname)
        return render(request, 'chatroom.html', {'chatname': name, 'username': user, 'all_message': list(all_messages)})
    else:
        all_messages = Messages.objects.filter(chatroom=chatname)
    return render(request, 'chatroom.html', {'chatname': name, 'username': user, 'all_message': list(all_messages)})
