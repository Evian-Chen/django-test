from django.urls import path
from .views import MeView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'), # 用於獲取和更新當前用戶資料
]