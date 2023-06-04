from django.contrib import admin
from django.urls import path
from core.person_tags_views import PersonTagListView, AddPersonTagView, DeletePersonTagView
from core.crypto_views import Crypto, AddCrypto, DeleteCrypto
from core.views import PersonListView, TableUploadView, TableUpdateView, TableSaveView, TableListView, StartTaskView, \
    CustomLoginView, EmailSend
from django.contrib.auth.views import LogoutView

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PersonListView.as_view(), name='person_list'),
    path('table/upload/', TableUploadView.as_view(), name='table_upload'),
    path('table/<int:pk>/preview/', TableUpdateView.as_view(), name='table_preview'),
    path('table/<int:pk>/save/', TableSaveView.as_view(), name='table_save'),
    path('tables/', TableListView.as_view(), name='table_list'),
    path('start_task/', StartTaskView.as_view(), name='start_task'),
    path('email_send/',  EmailSend.as_view(), name='email_send'),
    path('crypto/', Crypto.as_view(), name='crypto'),
    path('crypto/add/', AddCrypto.as_view(), name='crypto_add'),
    path('crypto/<int:pk>/delete/', DeleteCrypto.as_view(), name='crypto_delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('person_tags/', PersonTagListView.as_view(), name='person_tags'),
    path('person_tags/add/', AddPersonTagView.as_view(), name='person_tags_add'),
    path('person_tags/<int:pk>/delete/', DeletePersonTagView.as_view(), name='person_tags_delete'),
    path('sentry-debug/', trigger_error),

]
