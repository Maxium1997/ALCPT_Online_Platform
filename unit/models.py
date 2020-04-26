from django.db import models

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=150, unique=True)
    address = models.TextField(unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    website = models.URLField(unique=True, null=True, blank=True)
    is_military_school = models.BooleanField(default=False)

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
    name = models.CharField(max_length=150)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s%s" % (self.school, self.name)

    def get_student_num(self):
        student_num = 0
        for department in self.department_set.all():
            student_num += department.student_set.count()
        return student_num


class Department(models.Model):
    name = models.CharField(max_length=150)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "%s%s%s" % (self.college.school.name, self.college.name, self.name)


class Squadron(models.Model):
    name = models.CharField(max_length=150)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    class Meta:
        ordering = ('college',)

    def __str__(self):
        return "%s%s%s" % (self.college.school.name, self.college.name, self.name)
