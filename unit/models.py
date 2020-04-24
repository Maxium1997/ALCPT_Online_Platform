from django.db import models

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=150, unique=True)
    address = models.TextField(unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    website = models.URLField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_student_num(self):
        student_num = 0
        for college in self.college_set.all():
            for department in college.department_set.all():
                student_num += department.student_set.count()
        return student_num


class College(models.Model):
    name = models.CharField(max_length=150, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_student_num(self):
        student_num = 0
        for department in self.department_set.all():
            student_num += department.student_set.count()
        return student_num


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Squadron(models.Model):
    name = models.CharField(max_length=150, unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name
