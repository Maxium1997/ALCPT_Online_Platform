from django import forms

from unit.models import School, College, Department, Squadron


class SchoolCreateForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           max_length=150,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=True,
                              max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.CharField(required=True,
                           max_length=150,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=True,
                            max_length=15,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    website = forms.URLField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_military_school = forms.BooleanField(required=False)

    class Meta:
        model = School
        fields = ['name', 'address', 'slug', 'phone', 'website']


class CollegeCreateForm(forms.ModelForm):
    school = forms.ModelChoiceField(required=True,
                                    queryset=School.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True,
                           max_length=150,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = College
        fields = ['school', 'name']


class DepartmentCreateForm(forms.ModelForm):
    college = forms.ModelChoiceField(required=True,
                                     queryset=College.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True,
                           max_length=150,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Department
        fields = ['college', 'name']


class SquadronCreateForm(forms.ModelForm):
    college = forms.ModelChoiceField(required=True,
                                     queryset=College.objects.filter(school__is_military_school=True),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True,
                           max_length=150,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Squadron
        fields = ['college', 'name']

