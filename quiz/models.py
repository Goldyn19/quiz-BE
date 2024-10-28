from django.db import models
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()


class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField()
    correct_answer = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
    pin = models.CharField(max_length=6, unique=True, editable=False)
    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pin:  # Generate pin only if it doesn't already exist
            self.pin = self.generate_unique_pin()
        super().save(*args, **kwargs)

    def start_quiz(self):
        self.is_started = True
        self.save()

    def stop_quiz(self):
        self.is_ended = True
        self.save()

    def generate_unique_pin(self):
        length = 6
        while True:
            pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not GameSession.objects.filter(pin=pin).exists():
                return pin


class Answer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
