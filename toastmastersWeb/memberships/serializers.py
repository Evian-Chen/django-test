from rest_framework import serializers
from .models import Memberships

class MembershipsSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = Memberships
        fields = ['id', 'user', 'club', 'role', 'joined_at', 'user_username', 'club_name', 'role_display']