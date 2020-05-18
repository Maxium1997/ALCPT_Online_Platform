from django.db import models

from registration.models import User
# Create your models here.


# Used to notify something important or need to know to the users
class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    announcer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title
