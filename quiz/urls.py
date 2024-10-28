from django.urls import path
from .views import QuestionCreateView, QuestionListView, QuizCreateView, QuizListView, QuestionUpdateView
from .consumer import QuizConsumer

urlpatterns = [
    path('questions/<int:quiz_id>', QuestionListView.as_view(), name='question-list'),
    path('questions/update/<int:question_id>', QuestionUpdateView.as_view(), name='update-question'),
    path('questions/create/<int:quiz_id>', QuestionCreateView.as_view(), name='create-question'),
    path('quiz', QuizListView.as_view(), name='list-user-quiz'),
    path('quiz/create', QuizCreateView.as_view(), name='create-quiz'),



]

websockets_urlpatterns = [
    path('ws/quiz/', QuizConsumer.as_asgi(), name='quiz-websocket')
]
