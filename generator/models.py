from django.db import models
from django.contrib.auth.models import User

class GenerationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # NEW
    prompt = models.TextField()
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

