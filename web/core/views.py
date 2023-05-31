import csv

from django.shortcuts import get_object_or_404
from django.views.generic import View, ListView, FormView, UpdateView, TemplateView
from django.contrib import messages

from core.decorators import timing_decorator
from core.models import Person, PersonTable, TaskStatus, PersonTag
from core.services import TableService, PersonService
from core.forms import PersonTableForm, PersonFilterForm
from core.constants import PREVIEW_ROWS_LIMIT, PersonTableStatus
from core.tasks import save_table_task, update_person_status_and_usage_by_phone_number
from mycelery import app
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = '/'


class StartTaskView(LoginRequiredMixin, TemplateView):
    template_name = 'start_task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tasks'] = TaskStatus.objects.filter(is_active=True)
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'start':
            num_of_processes = int(request.POST.get('num_of_processes', 1))

            for _ in range(num_of_processes):
                task = update_person_status_and_usage_by_phone_number.delay()
                TaskStatus.objects.create(task_id=task.id)
            messages.success(self.request, 'Задачи успешно запущены.')

        elif action == 'stop':
            for task_status in TaskStatus.objects.filter(is_active=True):
                app.control.revoke(task_status.task_id, terminate=True)
                task_status.is_active = False
                task_status.save()
            messages.success(self.request, 'Задачи успешно остановлены.')

        return HttpResponseRedirect(reverse('start_task'))


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 50
    form_class = PersonFilterForm

    def get_queryset(self):
        return PersonService.filtered_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_qs = PersonService.filtered_queryset(self.request)
        context['total_count'] = filtered_qs.count()
        context['form'] = self.form_class(self.request.GET)
        context['has_data'] = PersonService.has_data_for_columns(filtered_qs)
        return context

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if request.GET.get('export') == 'excel':
            selected_columns = request.GET.getlist('columns')
            merge_fio = self.request.GET.get('merge_fio', '') == '1'
            response = PersonService.export_to_excel(qs, selected_columns, merge_fio)
            return response
        elif request.GET.get('export') == 'csv':
            selected_columns = request.GET.getlist('columns')
            merge_fio = self.request.GET.get('merge_fio', '') == '1'
            response = PersonService.export_to_csv(qs, selected_columns, merge_fio)
            return response

        return super().get(request, *args, **kwargs)
    @timing_decorator
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TableUploadView(LoginRequiredMixin, FormView):
    template_name = 'table_upload.html'
    form_class = PersonTableForm

    def form_valid(self, form):
        filename = self.request.FILES['file']
        self.loaded_table = TableService.upload_table(filename)
        messages.success(self.request, 'Таблица была успешно загружена.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('table_preview', args=[self.loaded_table.pk])


class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = PersonTable
    template_name = 'table_preview.html'
    fields = ['columns', 'status']

    def get_context_data(self, **kwargs):
        rows_limit = PREVIEW_ROWS_LIMIT
        context = super().get_context_data(**kwargs)
        excel_data = TableService.read_table(self.object.file)
        if len(excel_data) > rows_limit:
            excel_data = excel_data[:rows_limit]
        context['columns'] = self.object.columns
        context['rows'] = excel_data.values.tolist()
        context['tags'] = PersonTag.objects.all()
        return context

    def form_valid(self, form):
        if self.object.status == PersonTableStatus.STATUS_NEW:
            mappings = self.request.POST.getlist('mapping')
            columns = self.object.columns
            self.object.columns = [f"{mappings}:{columns}" for mappings, columns in zip(mappings, columns)]
            self.object.status = PersonTableStatus.STATUS_MATCHING
            self.object.save()
            selected_tags = self.request.POST.getlist('tags')
            tags = PersonTag.objects.filter(id__in=selected_tags)
            self.object.tags.set(tags)
        else:
            messages.error(self.request, 'Уже апдейтнуто.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('table_save', args=[self.object.pk])


class TableSaveView(LoginRequiredMixin, View):
    template_name = 'table_save.html'

    def get(self, request, pk):
        loaded_table = get_object_or_404(PersonTable, id=pk)
        return render(request, self.template_name,
                      {'loaded_table': loaded_table, 'status': loaded_table.get_status_display()})

    def post(self, request, pk):
        loaded_table = get_object_or_404(PersonTable, id=pk)
        save_table_task.delay(loaded_table.id)
        messages.success(self.request, 'Данные файла были успешно загружены.')
        return redirect('table_upload')


class TableListView(LoginRequiredMixin, ListView):
    template_name = 'table_list.html'
    model = PersonTable

    def get_queryset(self):
        return PersonTable.objects.order_by('status', '-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context