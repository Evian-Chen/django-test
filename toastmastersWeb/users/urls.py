from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import RegisterView, CustomTokenObtainPairView, LogoutView, MeView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 登入
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # simplejwt 的登入 View
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # simplejwt 的刷新 View
    # path('logout/', LogoutView.as_view(), name='logout'),
]