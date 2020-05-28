from django import template

from registration.models import User
from notification.models import Notification

register = template.Library()


@register.filter(name='notification_center_amount')
def notification_center_amount(user: User):
    return user.notification_set.all().count()


@register.filter(name='notification_unread_amount')
def notification_unread_amount(user: User):
    return user.notification_set.filter(is_read=False).count()
