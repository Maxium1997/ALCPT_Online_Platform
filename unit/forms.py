from django import forms

from unit.models import School


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

    class Meta:
        model = School
        fields = ['name', 'address', 'slug', 'phone', 'website']
