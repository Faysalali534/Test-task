from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SignupView

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
]
