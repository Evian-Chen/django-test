from rest_framework import serializers
from .models import Clubs

class ClubSerializer(serializers.ModelSerializer):
    meeting_time_formatted = serializers.ReadOnlyField()
    meeting_weekday_display = serializers.CharField(source='get_meeting_weekday_display', read_only=True)
    
    class Meta:
        model = Clubs
        fields = [
            'id', 'name', 'location', 'description',
            'meeting_weekday', 'meeting_weekday_display',
            'meeting_start_time', 'meeting_end_time',
            'meeting_time_display', 'meeting_time_formatted'
        ]