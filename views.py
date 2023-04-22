from .models import Caja, Movement
from .tables import MovementTable
from .forms import MovementForm
from .filters import MovementFilter
from django_filters.views import FilterView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django_tables2 import SingleTableMixin


class CajaListView(LoginRequiredMixin, ListView):
    model = Caja


class CajaDetailView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Movement
    table_class = MovementTable
    filterset_class = MovementFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(caja_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context["caja"] = Caja.objects.get(pk=self.kwargs["pk"])
        context["form"] = MovementForm(initial={"caja": pk})
        return context


class MovementCreateView(LoginRequiredMixin, CreateView):
    model = Movement
    fields = "__all__"
    http_method_names = ("post",)

    def get_success_url(self, *args, **kwargs):
        return reverse("caja:caja_detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        movement = form.save(commit=False)
        with transaction.atomic():
            caja = movement.caja
            if movement.type == Movement.IN:
                caja.balance += movement.qty
            else:
                caja.balance -= movement.qty
            caja.save()
            movement.save()
        self.object = movement
        return HttpResponseRedirect(self.get_success_url())


class MovementCancelView(LoginRequiredMixin, DeleteView):
    model = Movement
    template_name = "caja/movement_confirm_cancel.html"

    def get_success_url(self):
        if not self.success_url:
            self.success_url = self.object.caja.get_absolute_url()
        return self.success_url

    def form_valid(self, form):
        success_url = self.get_success_url()
        movement = self.object
        with transaction.atomic():
            caja = movement.caja
            if movement.type == Movement.IN:
                caja.balance -= movement.qty
            else:
                caja.balance += movement.qty
            self.object.cancel()
            caja.save()
        return HttpResponseRedirect(success_url)
