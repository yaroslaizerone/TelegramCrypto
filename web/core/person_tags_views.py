from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from core.models import PersonTag
from core.forms import PersonTagForm

class PersonTagListView(LoginRequiredMixin, ListView):
    model = PersonTag
    template_name = 'person_tag_list.html'

class AddPersonTagView(LoginRequiredMixin, CreateView):
    model = PersonTag
    form_class = PersonTagForm
    template_name = 'person_tag_add.html'
    success_url = reverse_lazy('person_tags')

class DeletePersonTagView(LoginRequiredMixin, DeleteView):
    model = PersonTag
    success_url = reverse_lazy('person_tags')
    template_name = 'person_tag_delete.html'