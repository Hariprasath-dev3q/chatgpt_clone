from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('chat/', views.new_chat, name='new_chat'),
    path('chat/<int:thread_id>/', views.chat_interface, name='chat_interface'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/delete-thread/<int:thread_id>/', views.delete_thread, name='delete_thread'),
]