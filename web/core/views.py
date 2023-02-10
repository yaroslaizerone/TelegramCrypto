from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Person, PersonUsage, PersonTag


class PersonListView(ListView):
    model = Person

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('personusage_set')
        return qs
