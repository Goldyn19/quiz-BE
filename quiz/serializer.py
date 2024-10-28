from rest_framework import serializers
from .models import Question, Quiz, Player, GameSession, Answer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'image': {'required': False}
        }


class QuizSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'created_by', 'created_by_username', 'question_count']
        read_only_fields = ['id', 'created_by', 'created_by_username', 'question_count']

    def get_question_count(self, obj):

        return obj.questions.count()


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
