from django.db import models
from django.utils import timezone

class QuizResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    quiz_type = models.IntegerField(blank=True, null=True)  # optional
    quiz_id = models.IntegerField(blank=True, null=True, default=0)  # null 허용 + 기본값 0
    selected = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(blank=True, null=True)
    duration_seconds = models.FloatField(blank=True, null=True)
    emotion = models.CharField(max_length=255, blank=True, null=True)
    situation = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'quiz_result'
