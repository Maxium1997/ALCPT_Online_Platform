from django.db import models
from django.contrib.auth.models import AbstractUser

from registration.definition import Gender, Identity, Privilege

# Create your models here.


class User(AbstractUser):
    reg_id = models.CharField(primary_key=True, unique=True, max_length=50)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    email_is_verified = models.BooleanField(default=False)
    gender = models.SmallIntegerField(default=Gender.Unset.value[0])
    identity = models.PositiveIntegerField(default=Identity.Visitor.value[0])
    privilege = models.PositiveIntegerField(default=Privilege.Testee.value[0])
    update_time = models.DateTimeField(auto_now=True)
