from django.contrib import admin

from .models import ChatRoom, Users, Messages


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'chatroom']


admin.site.register(Users)
admin.site.register(ChatRoom)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['messages', 'created_at', 'users']


admin.site.register(Messages)
