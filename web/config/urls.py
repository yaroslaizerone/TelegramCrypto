from django.contrib import admin
from django.urls import path
from core.views import PersonListView, TableUploadView, TableUpdateView, TableSaveView, TableListView, StartTaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PersonListView.as_view(), name='person_list'),
    path('table/upload/', TableUploadView.as_view(), name='table_upload'),
    path('table/<int:pk>/preview/', TableUpdateView.as_view(), name='table_preview'),
    path('table/<int:pk>/save/', TableSaveView.as_view(), name='table_save'),
    path('tables/', TableListView.as_view(), name='table_list'),
    path('start_task/', StartTaskView.as_view(), name='start_task'),
]