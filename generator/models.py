from django.db import models

class GenerationLog(models.Model):
    prompt = models.TextField()
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
