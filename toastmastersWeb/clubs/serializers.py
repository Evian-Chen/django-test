from rest_framework import serializers
from .models import Clubs, Memberships

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clubs
        fields = '__all__'

