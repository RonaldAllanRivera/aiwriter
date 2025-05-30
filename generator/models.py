# generator/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class GenerationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt = models.TextField()
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"



class TrialSessionLog(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    is_incognito = models.BooleanField(default=False)
    trial_uses = models.IntegerField(default=0)
    abuse_score = models.IntegerField(default=0)
    linked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    registered = models.BooleanField(default=False)  # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ip_address} ({self.trial_uses} used)"



class PurchaseLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    credits = models.IntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=50, default="completed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase by {self.user.email} - {self.credits} credits - ${self.amount}"
