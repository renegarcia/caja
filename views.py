from .models import Caja, Movement
from .tables import MovementTable
from .forms import MovementForm
from .filters import MovementFilter
from django_filters.views import FilterView
from django.shortcuts import reverse, get_object_or_404
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db import transaction
from django_tables2 import SingleTableMixin


class UserOwnsObjectMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class CajaListView(LoginRequiredMixin, ListView):
    model = Caja

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = modelform_factory(self.model, fields=("name",))
        return context

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CajaCreateView(LoginRequiredMixin, CreateView):
    model = Caja
    fields = ("name",)
    http_method_names = ("post",)

    def form_valid(self, form):
        caja = form.save(commit=False)
        caja.user = self.request.user
        caja.save()
        self.object = caja
        return HttpResponseRedirect(self.get_success_url())


class CajaUpdateView(LoginRequiredMixin, UserOwnsObjectMixin, UpdateView):
    model = Caja
    fields = ("name",)
    http_method_names = ("post",)


class CajaDeleteView(LoginRequiredMixin, UserOwnsObjectMixin, DeleteView):
    model = Caja
    success_url = reverse_lazy("caja:caja_list")

    def form_valid(self, form):
        messages.success(self.request, "La caja fue eliminada")
        return super(CajaDeleteView, self).form_valid(form)


class CajaDetailView(
    LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView
):
    model = Movement
    table_class = MovementTable
    filterset_class = MovementFilter

    def test_func(self):
        caja = self.get_caja()
        return caja.user == self.request.user

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(caja_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        caja = self.get_caja()
        context["caja"] = caja
        context["form"] = MovementForm(initial={"caja": pk})
        CajaForm = modelform_factory(Caja, fields=("name",))
        context["caja_update_form"] = CajaForm(initial={"name": caja.name})
        return context

    def get_caja(self):
        try:
            return self.caja
        except AttributeError:
            self.caja = get_object_or_404(Caja, pk=self.kwargs["pk"])
        return self.caja


class MovementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Movement
    fields = "__all__"
    http_method_names = ("post",)

    def test_func(self):
        caja = self.get_caja()
        return caja.user == self.request.user

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

    def get_caja(self):
        try:
            return self.caja
        except AttributeError:
            self.caja = get_object_or_404(Caja, pk=self.kwargs["pk"])
        return self.caja


class MovementCancelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movement
    template_name = "caja/movement_confirm_cancel.html"

    def test_func(self):
        movement = self.get_object()
        return movement.caja.user == self.request.user

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
