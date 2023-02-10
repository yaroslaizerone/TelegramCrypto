from django.contrib import admin
from django.urls import path
from core.views import PersonListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PersonListView.as_view(), name='person_list'),
]
