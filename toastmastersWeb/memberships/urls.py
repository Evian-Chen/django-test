from django.urls import path
from .views import MembershipsUserView, MembershipsClubView, MembershipsDetailView, MembershipsListCreateView


urlpatterns = [
    path('', MembershipsListCreateView.as_view(), name='memberships-list-create'),
    path('<int:pk>/', MembershipsDetailView.as_view(), name='memberships-detail'),
    path('user/<int:user_id>/', MembershipsUserView.as_view(), name='memberships-by-user'),
    path('club/<str:club_name>/', MembershipsClubView.as_view(), name='memberships-by-club'),
]