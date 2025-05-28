# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

from django.contrib.auth.signals import user_logged_in
from generator.models import TrialSessionLog
from generator.views import get_client_ip


@receiver(user_logged_in)
def link_trial_session_to_user(sender, user, request, **kwargs):
    ip_address = get_client_ip(request)
    try:
        session_log = TrialSessionLog.objects.get(ip_address=ip_address, linked_user__isnull=True)
        session_log.linked_user = user
        session_log.registered = True
        session_log.save()
    except TrialSessionLog.DoesNotExist:
        pass

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, credits=10)
      