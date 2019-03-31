from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import CustomUser, Ngo, Staff

@receiver(post_save, sender=CustomUser)
@receiver(post_save, sender=Ngo)
@receiver(post_save, sender=Staff)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)