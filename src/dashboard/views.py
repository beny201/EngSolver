from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, TemplateView

from dashboard.forms import SearchedValues
from distance_checker.models import Corner, Ridge


class CalculationsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        qty_corners = Corner.objects.filter(author=user).count()
        qty_ridges = Ridge.objects.filter(author=user).count()
        context['qty_corners'] = qty_corners
        context['qty_ridges'] = qty_ridges
        return context


class CornerCalculationView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/corner.html'
    model = Corner
    context_object_name = "Corners"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(author=user).order_by("-created_date")
        return queryset


class CornerDetailedView(LoginRequiredMixin, DetailView):
    model = Corner
    context_object_name = "corner"
    template_name = 'dashboard/corner_detail.html'


class CornerDeleteView(LoginRequiredMixin, DeleteView):
    model = Corner
    context_object_name = "corner"
    template_name = 'dashboard/delete_confirm.html'
    success_url = reverse_lazy('dashboard')


class RidgeCalculationView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/ridge.html'
    model = Ridge
    context_object_name = "Ridges"
    paginate_by = 5
    form_class = SearchedValues

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["form"] = self.form_class()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset_main = queryset.filter(author=user).order_by("-created_date")
        form = self.form_class(self.request.get)
        if form.is_valid():
            if form.cleaned_data.get("case"):
                if (
                    queryset_main.filter(
                        case__icontains=form.cleaned_data["case"]
                    ).count()
                    == 0
                ):
                    messages.error(self.request, "Case not found !")
                else:
                    return queryset_main.filter(
                        case__icontains=form.cleaned_data["case"]
                    )
        return queryset_main


class RidgeDetailedView(LoginRequiredMixin, DetailView):
    model = Ridge
    context_object_name = "ridge"
    template_name = 'dashboard/ridge_detail.html'


class RidgeDeleteView(LoginRequiredMixin, DeleteView):
    model = Ridge
    context_object_name = "ridge"
    template_name = 'dashboard/delete_confirm.html'
    success_url = reverse_lazy('dashboard')
