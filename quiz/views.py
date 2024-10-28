from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
import logging
from .models import Question, Quiz
from .serializer import QuestionSerializer, QuizSerializer

logger = logging.getLogger(__name__)


class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get quiz_id from query params
        quiz_id = self.kwargs.get('quiz_id')
        if not quiz_id:
            raise serializers.ValidationError({'message': 'Quiz id is required in the parameter'})

        try:
            # Attempt to retrieve the Quiz
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError({'message': 'Quiz does not exist'})

        # Ensure the current user is the creator of the quiz
        if quiz.created_by != self.request.user:
            raise permissions.PermissionDenied("Not allowed to add questions to this quiz.")

        # Save the question with the current user as the creator
        question = serializer.save(created_by=self.request.user)

        try:
            # Add the question to the quiz
            quiz.questions.add(question)
            quiz.save()
        except Exception as e:
            logger.error(f"Error adding question to quiz: {e}")
            raise serializers.ValidationError({'message': 'Failed to associate question with the quiz.'})

    def create(self, request, *args, **kwargs):
        # Call the default implementation of create
        response = super().create(request, *args, **kwargs)

        # Customize the response
        return Response({'message': 'Created successfully', 'data': response.data}, status=status.HTTP_201_CREATED)


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        user = self.request.user
        try:
            quiz = Quiz.objects.get(id=quiz_id, created_by=user)
        except Quiz.DoesNotExist:
            return Question.objects.none()
        questions = quiz.questions.all()
        return questions


class QuestionUpdateView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retrieve the question instance to update
        question_id = self.kwargs.get('question_id')
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise serializers.ValidationError({"message": "Question does not exist."})

    def perform_update(self, serializer):
        question = self.get_object()

        # Ensure that the user is the creator of the question
        if question.created_by != self.request.user:
            raise permissions.PermissionDenied('Not allowed to edit this question')

        # Save the updated question
        serializer.save()

    def update(self, request, *args, **kwargs):
        # Call the default implementation of update
        response = super().update(request, *args, **kwargs)

        # Customize the response
        return Response({"message": "Updated successfully", "data": response.data}, status=status.HTTP_200_OK)

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        user = self.request.user
        try:
            quiz = Quiz.objects.get(id=quiz_id, created_by=user)
        except Quiz.DoesNotExist:
            return Question.objects.none()
        questions = quiz.questions.all()
        return questions



class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Fetch all quizzes related to the user
        return Quiz.objects.filter(created_by=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response = {
            'message': 'Request Successful',
            'data': serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)


# Create your views here.
