from django.db import models

# Create your models here.

class Clubs(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

        # 新的結構化時間字段
    WEEKDAY_CHOICES = [
        (0, '星期一'),
        (1, '星期二'),
        (2, '星期三'),
        (3, '星期四'),
        (4, '星期五'),
        (5, '星期六'),
        (6, '星期日'),
    ]
    
    meeting_weekday = models.IntegerField(choices=WEEKDAY_CHOICES, null=True, blank=True)
    meeting_start_time = models.TimeField(null=True, blank=True)
    meeting_end_time = models.TimeField(null=True, blank=True)
    
    # 保留原有字段作為備用或顯示用
    meeting_time_display = models.CharField(max_length=50, blank=True, null=True, help_text="顯示用的時間描述")

    def __str__(self):
        return self.name

    @property
    def meeting_time_formatted(self):
        """格式化顯示開會時間"""
        if self.meeting_weekday is not None and self.meeting_start_time and self.meeting_end_time:
            weekday_name = dict(self.WEEKDAY_CHOICES)[self.meeting_weekday]
            return f"{weekday_name} {self.meeting_start_time.strftime('%H:%M')}-{self.meeting_end_time.strftime('%H:%M')}"
        return self.meeting_time_display or "未設定"

class ClubRole(models.TextChoices):
    PRESIDENT = 'president', '社長'
    VICE_PRESIDENT = 'vice_president', '副社長'
    VICE_PRESIDENT_EDUCATION = 'vpe', '教育副社長 (VPE)'
    VICE_PRESIDENT_MEMBERSHIP = 'vpm', '會員副社長 (VPM)'
    VICE_PRESIDENT_PUBLIC_RELATIONS = 'vpp', '公關副社長 (VPP)'
    SECRETARY = 'secretary', '書記'
    MEMBER = 'member', '會員'
