from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import ChatThread, Message
from .forms import SignUpForm

# Configure OpenAI
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

class CustomLoginView(LoginView):
    template_name = 'chat/login.html'
    redirect_authenticated_user = True

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('chat_list')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('chat_list')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def chat_list(request):
    threads = ChatThread.objects.filter(user=request.user)
    return render(request, 'chat/chat_list.html', {'threads': threads})

@login_required
def chat_interface(request, thread_id=None):
    if thread_id:
        thread = get_object_or_404(ChatThread, id=thread_id, user=request.user)
        messages_list = thread.messages.all()
    else:
        thread = None
        messages_list = []
    
    threads = ChatThread.objects.filter(user=request.user)
    
    return render(request, 'chat/chat_interface.html', {
        'thread': thread,
        'messages': messages_list,
        'threads': threads
    })

@login_required
def new_chat(request):
    thread = ChatThread.objects.create(user=request.user)
    return redirect('chat_interface', thread_id=thread.id)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        thread_id = data.get('thread_id')
        
        if not message_content:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create thread
        if thread_id:
            thread = get_object_or_404(ChatThread, id=thread_id, user=request.user)
        else:
            thread = ChatThread.objects.create(
                user=request.user,
                title=message_content[:50] + "..." if len(message_content) > 50 else message_content
            )
        
        # Save user message
        user_message = Message.objects.create(
            thread=thread,
            content=message_content,
            is_user=True
        )
        
        # Generate AI response (mock response for demo)
        ai_response = generate_ai_response(message_content)
        
        # Save AI message
        ai_message = Message.objects.create(
            thread=thread,
            content=ai_response,
            is_user=False
        )
        
        return JsonResponse({
            'success': True,
            'thread_id': thread.id,
            'user_message': {
                'content': user_message.content,
                'timestamp': user_message.timestamp.isoformat()
            },
            'ai_message': {
                'content': ai_message.content,
                'timestamp': ai_message.timestamp.isoformat()
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["DELETE"])
def delete_thread(request, thread_id):
    thread = get_object_or_404(ChatThread, id=thread_id, user=request.user)
    thread.delete()
    return JsonResponse({'success': True})

def generate_ai_response(user_message): 
    try:
        response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": user_message}
        ]
    )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I'm having trouble generating a response right now. Error: {str(e)}"
    




