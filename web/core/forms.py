from django import forms
from core.models import PersonTable


class PersonTableForm(forms.ModelForm):
    class Meta:
        model = PersonTable
        fields = ['file']
