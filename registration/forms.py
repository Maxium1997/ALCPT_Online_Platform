from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from registration.models import User
from registration.definition import Privilege, Identity, Gender
from unit.models import Department, Squadron


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


# class UserCreateForm(forms.ModelForm):
#     username = forms.CharField(required=True, max_length=150,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}),
#                                error_messages={'required': "username field is required."})
#     first_name = forms.CharField(required=True, max_length=30,
#                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
#                                  error_messages={'required': "First name field is required."})
#     last_name = forms.CharField(required=True, max_length=150,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}),
#                                 error_messages={'required': "Last name field is required."})
#     CHOICES = [(_.value[0], _.value[1]) for _ in Gender.__members__.values()]
#     gender = forms.ChoiceField(required=True,
#                                choices=CHOICES,
#                                error_messages={'required': "Please select your gender."})
#     IDENTITIES = [(_.value[0], _.value[1]) for _ in Identity.__members__.values()]
#     identity = forms.ChoiceField(required=True,
#                                  choices=IDENTITIES,
#                                  widget=forms.Select(attrs={'id': 'identity',
#                                                             'onchange': 'is_student();'}),
#                                  error_messages={'required': "Please select your identity."})
#     PRIVILEGES = [(_.value[0], _.value[1]) for _ in Privilege.__members__.values()]
#     privilege = forms.IntegerField(required=True,
#                                    widget=forms.CheckboxSelectMultiple(choices=PRIVILEGES,
#                                                                        attrs={'class': 'list-inline pl-2'}),
#                                    error_messages={'required': "Select one privilege at least."})
#     stu_id = forms.CharField(disabled=True,
#                              max_length=20,
#                              widget=forms.TextInput(attrs={'id': 'stu_id',
#                                                            'class': 'form-control'}))
#     department = forms.ModelChoiceField(disabled=True,
#                                         queryset=Department.objects.all(),
#                                         widget=forms.Select(attrs={'id': 'department',
#                                                                    'class': 'form-control'}))
#     squadron = forms.ModelChoiceField(disabled=True,
#                                       queryset=Squadron.objects.filter(college__school__is_military_school=True),
#                                       widget=forms.Select(attrs={'id': 'squadron',
#                                                                  'class': 'form-control'}),
#                                       help_text="If you are not a military student, please ignore this field.")
#     year_grade = forms.IntegerField(disabled=True,
#                                     widget=forms.TextInput(attrs={'id': 'year_grade',
#                                                                   'class': 'form-control'}),
#                                     help_text="If you are not a military student, please ignore this field.")
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name',
#                   'gender', 'identity', 'privilege',
#                   'stu_id', 'department', 'squadron', 'year_grade']


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
