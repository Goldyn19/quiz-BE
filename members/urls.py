
from django.urls import path
from .views import SignUpView, LoginView, UserUpdateView

urlpatterns = [
    path('register', SignUpView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('update-user', UserUpdateView.as_view(), name='update-user')

]