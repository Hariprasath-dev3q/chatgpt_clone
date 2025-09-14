from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ChatThread, Message

@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'user__username']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['thread', 'is_user', 'content_preview', 'timestamp']
    list_filter = ['is_user', 'timestamp']
    search_fields = ['content']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'