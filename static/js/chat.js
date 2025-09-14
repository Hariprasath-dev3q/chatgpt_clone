function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Clear input and show typing indicator
    input.value = '';
    showTypingIndicator();
    
    // Add user message to UI immediately
    addMessageToUI(message, true);
    
    // Send to backend
    fetch('/api/send-message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            message: message,
            thread_id: currentThreadId
        })
    })
    .then(response => response.json())
    .then(data => {
        hideTypingIndicator();
        
        if (data.success) {
            // Update thread ID if this was a new chat
            if (!currentThreadId && data.thread_id) {
                window.history.replaceState({}, '', `/chat/${data.thread_id}/`);
                currentThreadId = data.thread_id;
            }
            
            // Add AI response
            addMessageToUI(data.ai_message.content, false);
            
            // Refresh sidebar to show updated chat
            setTimeout(() => window.location.reload(), 1000);
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        hideTypingIndicator();
        console.error('Error:', error);
        alert('Error sending message');
    });
}

function addMessageToUI(content, isUser) {
    const container = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `mb-4 chat-message ${isUser ? 'text-right' : 'text-left'}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = `inline-block max-w-3xl p-3 rounded-lg message-bubble ${
        isUser ? 'bg-blue-500 text-white' : 'bg-white text-gray-800 shadow'
    }`;
    
    const contentP = document.createElement('p');
    contentP.className = 'whitespace-pre-wrap';
    contentP.textContent = content;
    
    const timeP = document.createElement('p');
    timeP.className = `text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500'}`;
    timeP.textContent = new Date().toLocaleString();
    
    bubbleDiv.appendChild(contentP);
    bubbleDiv.appendChild(timeP);
    messageDiv.appendChild(bubbleDiv);
    
    // Insert before typing indicator
    const typingIndicator = document.getElementById('typing-indicator');
    container.insertBefore(messageDiv, typingIndicator);
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    indicator.classList.remove('hidden');
    
    const container = document.getElementById('chat-container');
    container.scrollTop = container.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    indicator.classList.add('hidden');
}

function newChat() {
    window.location.href = '/chat/';
}

function deleteThread(threadId, event) {
    event.stopPropagation();
    
    if (confirm('Are you sure you want to delete this chat?')) {
        fetch(`/api/delete-thread/${threadId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/';
            } else {
                alert('Error deleting chat');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting chat');
        });
    }
}

// Auto-focus message input
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('message-input');
    if (input) {
        input.focus();
    }
});