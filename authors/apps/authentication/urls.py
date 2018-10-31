from django.urls import path, re_path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, AccountVerificationAPIView
)

urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users', RegistrationAPIView.as_view(), name='signup'),
    path('users/login', LoginAPIView.as_view(), name='login' ),
    path('activate/<uidb64>/<token>', AccountVerificationAPIView.as_view(), name='activate_account'),
]
