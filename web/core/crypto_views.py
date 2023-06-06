from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from core.models import CryptoObject
from core.forms import CryptoForm
from core.tasks import check_price_crypto


class Crypto(LoginRequiredMixin, ListView):
    model = CryptoObject
    template_name = 'crypto_list.html'


class AddCrypto(LoginRequiredMixin, CreateView):
    model = CryptoObject
    form_class = CryptoForm
    template_name = 'crypto_add.html'
    success_url = reverse_lazy('crypto')

    def form_valid(self, form):
        self.model = form.save(commit=False)
        CryptoObject.objects.filter(name=self.model.name).delete()
        self.model.save()
        return redirect('/crypto')

# TODO
# сделать асинхронный мотод для проверки падения стоимости монеты
# Делать проверку по БД
class DeleteCrypto(LoginRequiredMixin, DeleteView):
    model = CryptoObject
    template_name = 'crypto_delete.html'
    success_url = reverse_lazy('crypto')
