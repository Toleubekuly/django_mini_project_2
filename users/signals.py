from django.dispatch import receiver
from djoser.signals import user_registered, user_activated
from django.contrib.auth.signals import user_logged_in, user_logged_out
import logging

logger = logging.getLogger('app')


@receiver(user_registered)
def log_user_registered(sender, user, request, **kwargs):
    logger.info(f"User registered: {user.username}")


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    logger.info(f"User logged in: {user.username}")


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    logger.info(f"User logged out: {user.username}")
