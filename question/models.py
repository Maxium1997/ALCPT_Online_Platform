from django.db import models

from registration.models import User
from question.definition import Difficulty, State

# Create your models here.


class Question(models.Model):
    q_type = models.PositiveSmallIntegerField(blank=False, null=False)
    q_file = models.FileField(upload_to='Listening Question Audio File', null=True)
    q_content = models.TextField(blank=True, null=True)
    difficulty = models.PositiveSmallIntegerField(default=Difficulty.Simple.value[0])
    issued_freq = models.PositiveIntegerField(default=0)
    # issued_freq: used to record the issued frequency of the question

    correct_freq = models.PositiveIntegerField(default=0)
    # correct_freq: used to record the correct frequency of the question

    faulty_reason = models.TextField(null=True, blank=True)
    # faulty_reason: used to record the faulty reason when the question was rejected

    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='producer')
    updated_time = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    state = models.PositiveSmallIntegerField(default=State.Saved)

    @property   # read only
    def correct_rate(self):
        return self.correct_freq / self.issued_freq * 100


class Choice(models.Model):
    source = models.ForeignKey(Question, on_delete=models.CASCADE)
    c_content = models.TextField(null=False, blank=False)
    is_answer = models.BooleanField(default=False)

    def __set__(self):
        return self.c_content
