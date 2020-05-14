from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from registration.models import User, Student
from registration.definition import Privilege, Identity, Gender
from unit.models import School, College, Department, Squadron


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               error_messages={'required': "username field is required."})

    first_name = forms.CharField(required=True, max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'First name'}),
                                 error_messages={'required': "First name field is required."})
    last_name = forms.CharField(required=True, max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Last name'}),
                                error_messages={'required': "Last name field is required."})
    CHOICES = [(_.value[0], _.value[1]) for _ in Gender.__members__.values()]
    gender = forms.ChoiceField(required=True,
                               choices=CHOICES,
                               widget=forms.Select(attrs={'id': 'gender',
                                                          'class': 'form-control'}),
                               error_messages={'required': "Please select your gender."})
    IDENTITIES = [(_.value[0], _.value[1]) for _ in Identity.__members__.values()]
    identity = forms.ChoiceField(required=True,
                                 choices=IDENTITIES,
                                 widget=forms.Select(attrs={'id': 'identity',
                                                            'class': 'form-control'}),
                                 error_messages={'required': "Please select your identity."})
    introduction = forms.CharField(required=False,
                                   widget=forms.Textarea(attrs={'class': 'form-control',
                                                                'rows': 4,
                                                                'placeholder': 'Say something to introduce yourself'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'identity', 'introduction']


class SchoolForm(forms.ModelForm):
    school = forms.ModelChoiceField(queryset=School.objects.all())

    class Meta:
        model = School
        fields = ['school']


class CollegeForm(forms.ModelForm):
    def __init__(self, school, *args, **kwargs):
        super(CollegeForm, self).__init__(*args, **kwargs)
        self.fields['college'] = forms.ModelChoiceField(queryset=College.objects.filter(school=school))

    class Meta:
        model = College
        fields = '__all__'


class StudentProfileUpdateForm(forms.ModelForm):
    stu_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    squadron = forms.ModelChoiceField(required=False,
                                      queryset=Squadron.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    year_grade = forms.CharField(required=False,
                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['stu_id', 'department', 'squadron', 'year_grade']
