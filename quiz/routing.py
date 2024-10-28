from django.urls import path
from .consumer import QuizConsumer

websocket_urlpatterns = [
    path('ws/quiz/<str:session_id>/', QuizConsumer.as_asgi()),
]
