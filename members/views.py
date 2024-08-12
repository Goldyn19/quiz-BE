from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .token import create_jwt_pair_for_users
from .serializer import SignUpSerializer, UserUpdateSerializer, UserSerializer
from .models import User
from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema


class LoginView(APIView):
    @swagger_auto_schema(operation_summary='Login user', operation_description='To login users')
    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_users(user)
            user_data = UserSerializer(user).data
            response = {
                'message': 'Login successful',
                'tokens': tokens,
                'user': user_data

            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'invalid username or password'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary='Get Auth key', operation_description='To get the Authentication key')
    def get(self, request: Request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    @swagger_auto_schema(operation_summary='Create User', operation_description='sign up with an email address')
    def post(self, request: Request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                response = {
                    'message': 'User created successfully',
                    'data': serializer.data
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Log the exception here if needed
            return Response(
                data={'error': 'An unexpected error occurred. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        return self.request.user
# Create your views here.
