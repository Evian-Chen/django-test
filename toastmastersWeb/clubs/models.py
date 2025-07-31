from django.db import models

# Create your models here.

class Clubs(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    meeting_time = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ClubRole(models.TextChoices):
    PRESIDENT = 'president', '社長'
    VICE_PRESIDENT = 'vice_president', '副社長'
    VICE_PRESIDENT_EDUCATION = 'vpe', '教育副社長 (VPE)'
    VICE_PRESIDENT_MEMBERSHIP = 'vpm', '會員副社長 (VPM)'
    VICE_PRESIDENT_PUBLIC_RELATIONS = 'vpp', '公關副社長 (VPP)'
    SECRETARY = 'secretary', '書記'
    MEMBER = 'member', '會員'

class Memberships(models.Model):
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=50, choices=ClubRole.choices, default=ClubRole.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'user', 'role')

    def __str__(self):
        return f"{self.user.username} @ {self.club.name} ({self.role})"
