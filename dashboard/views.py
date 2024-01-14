from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, TemplateView

from bars_calculation.models import CalculationRhs
from dashboard.filters import CalculationRhsFilter, CornerFilter, RidgeFilter
from distance_checker.models import Corner, Ridge


class UserNeedToBeAuthor(UserPassesTestMixin):
    login_url = "login"

    def test_func(self):
        checked_object = self.get_object()
        return checked_object.author == self.request.user

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('login')


class CalculationsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        qty_corners = Corner.objects.filter(author=user).count()
        qty_ridges = Ridge.objects.filter(author=user).count()
        qty_bars = CalculationRhs.objects.filter(author=user).count()
        context['qty_corners'] = qty_corners
        context['qty_ridges'] = qty_ridges
        context['qty_bars'] = qty_bars
        return context


class CornerCalculationView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/corner.html'
    model = Corner
    context_object_name = "Corners"
    paginate_by = 5
    form_class = CornerFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset_user = queryset.filter(author=user).order_by("-created_date")
        self.filterset = self.form_class(self.request.GET, queryset_user)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["form"] = self.filterset.form
        return context


class CornerDetailedView(LoginRequiredMixin, UserNeedToBeAuthor, DetailView):
    model = Corner
    context_object_name = "corner"
    template_name = 'dashboard/corner_detail.html'


class CornerDeleteView(LoginRequiredMixin, UserNeedToBeAuthor, DeleteView):
    model = Corner
    context_object_name = "corner"
    template_name = 'dashboard/delete_confirm.html'
    success_url = reverse_lazy('dashboard')


class RidgeCalculationView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/ridge.html'
    model = Ridge
    context_object_name = "Ridges"
    paginate_by = 5
    form_class = RidgeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset_user = queryset.filter(author=user).order_by("-created_date")
        self.filterset = self.form_class(self.request.GET, queryset_user)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["form"] = self.filterset.form
        return context


class RidgeDetailedView(LoginRequiredMixin, UserNeedToBeAuthor, DetailView):
    model = Ridge
    context_object_name = "ridge"
    template_name = 'dashboard/ridge_detail.html'


class RidgeDeleteView(LoginRequiredMixin, UserNeedToBeAuthor, DeleteView):
    model = Ridge
    context_object_name = "ridge"
    template_name = 'dashboard/delete_confirm.html'
    success_url = reverse_lazy('dashboard')


class BarCalculationView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/bar.html'
    model = CalculationRhs
    context_object_name = "calculation"
    paginate_by = 5
    form_class = CalculationRhsFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset_user = queryset.filter(author=user).order_by("-created_date")
        self.filterset = self.form_class(self.request.GET, queryset_user)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["form"] = self.filterset.form
        return context


class BarDetailedView(LoginRequiredMixin, UserNeedToBeAuthor, DetailView):
    model = CalculationRhs
    context_object_name = "bar"
    template_name = 'dashboard/bar_detail.html'


class BarDeleteView(LoginRequiredMixin, UserNeedToBeAuthor, DeleteView):
    model = CalculationRhs
    context_object_name = "bar"
    template_name = 'dashboard/delete_confirm.html'
    success_url = reverse_lazy('dashboard')
