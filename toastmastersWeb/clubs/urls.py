from django.urls import path
from .views import ClubListView, ClubCreateView, ClubUpdateView, ClubDeleteView, ClubDetailView

urlpatterns = [
    path('list/', ClubListView.as_view(), name='club-list'),
    path('create/', ClubCreateView.as_view(), name='club-create'),
    path('update/<int:pk>/', ClubUpdateView.as_view(), name='club-update'),
    path('delete/<int:pk>/', ClubDeleteView.as_view(), name='club-delete'),
    path('detail/<str:name>/', ClubDetailView.as_view(), name='club-detail')
]