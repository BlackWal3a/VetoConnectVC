from django import forms
from django.contrib.auth.models import User
from .models import AnimalForm

from django import forms
from myapp.models import Account

class AnimalFormForm(forms.ModelForm):
    class Meta:
        model = AnimalForm
        fields = ['animal_name', 'animal_type', 'problem','probleme', 'description','picture1', 'picture2', 'picture3']

