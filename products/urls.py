from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .views import SignupView, ProductViewSet, ProductSearchView, ProductSelectViewSet

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('product/create/', ProductViewSet.as_view({'post': 'create'}), name='product-create'),
    path('product/search/', ProductSearchView.as_view(), name='product-search'),
    path('product/<int:pk>/select/', ProductSelectViewSet.as_view({'post': 'select'}), name='product-select'),
]
