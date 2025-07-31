from django.db import models
from clubs.models import ClubRole

# Create your models here.

class Memberships(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='memberships')
    club = models.ForeignKey('clubs.Clubs', on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=50, choices=ClubRole.choices, default=ClubRole.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'club', 'role')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} @ {self.club.name} ({self.role})"