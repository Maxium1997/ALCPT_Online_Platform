from django.db import models
from django.contrib.auth.models import AbstractUser

from registration.definition import Gender, Identity, Privilege

# Create your models here.


class User(AbstractUser):
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    email_is_verified = models.BooleanField(default=False)
    gender = models.SmallIntegerField(default=Gender.Unset.value[0])
    identity = models.PositiveIntegerField(default=Identity.Visitor.value[0])
    privilege = models.PositiveIntegerField(default=Privilege.Testee.value[0])
    update_time = models.DateTimeField(auto_now=True)

    def has_permission(self, require_privilege):
        return (self.privilege & require_privilege.value[0]) > 0

    def is_student(self):
        return True if self.identity == Identity.Student.value[0] else False
