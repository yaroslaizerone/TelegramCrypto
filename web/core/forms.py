from django import forms
from core.models import PersonTable, Region, PersonTag, PersonStatusLV
from core.constants import GENDER_CHOICES


class PersonTagForm(forms.ModelForm):
    class Meta:
        model = PersonTag
        fields = ['name']
        labels = {
            'name': 'Название тега',
        }


class PersonTableForm(forms.ModelForm):
    class Meta:
        model = PersonTable
        fields = ['file']


class PersonFilterForm(forms.Form):
    region = forms.ModelMultipleChoiceField(
        queryset=Region.objects.all(),
        label='Регион',
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'id_region', 'data-placeholder': 'Регион'}),
    )
    utc_choices = [('', 'Выберите часовой пояс')] + sorted(
        [(utc, 'UTC+' + utc) for utc in Region.objects.values_list('utc', flat=True).distinct()])
    utc = forms.MultipleChoiceField(
        choices=utc_choices,
        label='Часовой пояс UTC',
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'id_utc', 'data-placeholder': 'UTC'}),
    )
    max_rows = forms.IntegerField(
        required=False,
        min_value=1,
        label='Максимальное количество строк',
        widget=forms.NumberInput(attrs={'id': 'id_max_rows', 'placeholder': 'Кол-во строк'})
    )
    gender = forms.MultipleChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        label='Пол',
        widget=forms.SelectMultiple(attrs={'id': 'id_gender', 'data-placeholder': 'Пол'}),
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=PersonTag.objects.all(),
        required=False,
        label='Тег',
        widget=forms.SelectMultiple(attrs={'id': 'id_tag', 'data-placeholder': 'Тег'}),
    )
    status = forms.ModelMultipleChoiceField(
        queryset=PersonStatusLV.objects.all(),
        label='Статус',
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'id_status', 'data-placeholder': 'Статус'}),
    )
