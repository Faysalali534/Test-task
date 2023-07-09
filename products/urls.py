from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from products.views import SignupView, TokenObtainPairView, TokenRefreshView, ProductViewSet, ProductSearchView, \
    ProductSelectViewSet, UserProductListView

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('product/create/', ProductViewSet.as_view({'post': 'create'}), name='product-create'),
    path('product/search/', ProductSearchView.as_view(), name='product-search'),
    path('product/<int:pk>/select/', ProductSelectViewSet.as_view({'post': 'select', "put": "deselect"}),
         name='product-select'),
    path('user/products/', UserProductListView.as_view(), name='user-products'),
]
