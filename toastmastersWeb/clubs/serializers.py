from rest_framework import serializers
from .models import Clubs

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clubs
        fields = '__all__'

