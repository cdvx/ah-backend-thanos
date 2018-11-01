from django.urls import path, re_path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, AccountVerificationAPIView
)

urlpatterns = [
    # path('users/<pk>', UserRetrieveUpdateAPIView.as_view()), Story not yet worked on
    path('users', RegistrationAPIView.as_view(), name='signup'),
    path('users/login', LoginAPIView.as_view(), name='login' ),
    path('users/activate/<uidb64>/<activation_token>', AccountVerificationAPIView.as_view(), name='activate_account'),
]
