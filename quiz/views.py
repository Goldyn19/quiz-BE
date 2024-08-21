from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Question, Quiz
from .serializer import QuestionSerializer, QuizSerializer


class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        quiz_id = self.request.query_params.get('quiz_id')
        user = self.request.user
        try:
            quiz = Quiz.objects.get(id=quiz_id, created_by=user)
        except Quiz.DoesNotExist:
            return Question.objects.none()

        return quiz.questions.all()


class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the current user
        serializer.save(created_by=self.request.user)


class QuizAddQuestionsView(generics.UpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Fetch the specific Quiz object using the primary key from the URL
        quiz = self.get_object()

        # Ensure that the quiz was created by the current user
        if quiz.created_by != request.user:
            return Response({"detail": "Not allowed to add questions to this quiz."}, status=status.HTTP_403_FORBIDDEN)

        # Get the list of question IDs from the request data
        question_ids = request.data.get('questions', [])

        # Validate and add each question
        for question_id in question_ids:
            try:
                question = Question.objects.get(id=question_id)
                quiz.questions.add(question)
            except Question.DoesNotExist:
                return Response({"detail": f"Question with id {question_id} does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)

        quiz.save()
        return Response(QuizSerializer(quiz).data)


# Create your views here.
