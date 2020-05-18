from django.shortcuts import render

from registration.models import User
from notification.models import Notification

# Create your views here.


# If the notification to notify user some messages
def notify(self, title: str, content: str, is_public: bool, recipients: list, announcer: User):
    if is_public:
        Notification.objects.create(title=title, content=content, is_public=True, announcer=announcer)
    else:
        Notification.objects.bulk_create([Notification(title=title, content=content,
                                                       is_public=False, recipient=recipient,
                                                       announcer=announcer) for recipient in recipients])
