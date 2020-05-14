import time, datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from registration.definition import Gender, Identity, Privilege
from unit.models import Department, Squadron

# Create your models here.


class User(AbstractUser):
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    email_is_verified = models.BooleanField(default=False)
    gender = models.SmallIntegerField(default=Gender.Unset.value[0])
    identity = models.PositiveIntegerField(default=Identity.User.value[0])
    privilege = models.PositiveIntegerField(default=Privilege.Testee.value[0])
    update_time = models.DateTimeField(auto_now=True)

    def has_permission(self, require_privilege):
        return (self.privilege & require_privilege.value[0]) > 0

    def is_student(self):
        return True if self.identity == Identity.Student.value[0] and self.student is not None else False


class Student(models.Model):
    stu_id = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    squadron = models.ForeignKey(Squadron, null=True, on_delete=models.SET_NULL)
    year_grade = models.PositiveSmallIntegerField(default=time.localtime().tm_year - 1911)
    update_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()

    def get_stu_id(self):
        return self.stu_id

    def can_be_updated(self):
        return True if (datetime.date.today()-self.update_time) > datetime.timedelta(days=30) else False
