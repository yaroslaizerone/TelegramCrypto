from django import forms
from core.models import PersonTable, Region
from django_select2.forms import Select2Widget



class PersonTableForm(forms.ModelForm):
    class Meta:
        model = PersonTable
        fields = ['file']

class PersonFilterForm(forms.Form):
    region = forms.ModelMultipleChoiceField(
        queryset=Region.objects.all(),
        label='Регион',
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'id_region', 'data-placeholder': 'Выберите регион'}),
    )
    utc_choices = [('', 'Выберите часовой пояс')] + sorted(
        [(utc, 'UTC+' + utc) for utc in Region.objects.values_list('utc', flat=True).distinct()])
    utc = forms.MultipleChoiceField(
        choices=utc_choices,
        label='Часовой пояс UTC',
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'id_utc', 'data-placeholder': 'Выберите UTC'}),
    )
    max_rows = forms.IntegerField(
        required=False,
        min_value=1,
        label='Максимальное количество строк',
        widget=forms.NumberInput(attrs={'id': 'id_max_rows', 'placeholder': 'Кол-во строк'})
    )

