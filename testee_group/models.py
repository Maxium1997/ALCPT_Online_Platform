from django.db import models

# Create your models here.


class TesteeGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    member = models.ManyToManyField('User', blank=True)
    creator = models.ForeignKey('User', null=True, on_delete=models.SET_NULL, related_name='created_by')
    created_time = models.DateTimeField(auto_now_add=True)
    updater = models.ForeignKey('User', null=True, on_delete=models.SET_NULL, related_name='updated_by')
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
