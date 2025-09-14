from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="New Chat")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def get_preview(self):
        first_message = self.messages.filter(is_user=True).first()
        if first_message:
            return first_message.content[:50] + "..." if len(first_message.content) > 50 else first_message.content
        return "New Chat"

class Message(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_user = models.BooleanField()  # True for user messages, False for AI responses
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        sender = "User" if self.is_user else "AI"
        return f"{sender}: {self.content[:50]}..."