from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('me/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
]
