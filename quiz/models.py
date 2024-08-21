from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField()  # Store options as a JSON object
    correct_answer = models.CharField(max_length=255)


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Player(models.Model):
    username = models.CharField(max_length=255)
    score = models.IntegerField(default=0)


class GameSession(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    is_active = models.BooleanField(default=True)
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)


class Answer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
