import json
from django.core import serializers
from django.http import JsonResponse
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


def get_messages(request):
    all_messages = list(Messages.objects.values())
    return JsonResponse(all_messages, safe=False)


def chatroom(request, name):
    username = request.user.id
    chatname = ChatRoom.objects.get(chatname=name)
    all_messages = Messages.objects.filter(chatroom=chatname)
    user = Users.objects.get(username=username)

    if request.method == 'POST':
        messages = request.POST.get('messages')
        user = Users.objects.get(username=username)
        delivered_message = Messages.objects.create(
            message=messages, user=user, chatroom=chatname)
        delivered_message.save()
        all_messages = Messages.objects.filter(chatroom=chatname)
    else:
        all_messages = Messages.objects.filter(chatroom=chatname)

    all_usernames = list(Users.objects.all().values('username_id'))
    all_users_list = ['start']
    for us in all_usernames:
        all_users_list.append(str(Users.objects.get(id=us['username_id'])))
    all_users_list = json.dumps(all_users_list)
    filtered_messages = serializers.serialize('json', all_messages)
    return render(request, 'chatroom.html', {'names': all_usernames, 'all_usernames': all_users_list, 'chatroom': chatname.id, 'userid': username, 'chatname': name, 'username': user, 'all_message': filtered_messages})
