# Create your views here.
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView

from bars_calculation.forms import CalculationCfrhsForm

from .calculation import CalculationCFRHS, CountryFactors, SteelGrade
from .models import DetailedCalculationCfrhs


class CalculationRhsView(FormView):
    form_class = CalculationCfrhsForm
    template_name = "bars_calculation/bar.html"
    template_name_detailed = "bars_calculation/bar_detailed.html"

    title = "Bars calculation"
    connection_type = "Cold formed - SHS checker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['connection_type'] = self.connection_type
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        value_country = cleaned_data['country']
        value_steel = cleaned_data['steel']
        value_axial_force = cleaned_data['axial_force']
        value_eccentricity = cleaned_data['eccentricity']
        value_bending_moment = cleaned_data['bending_moment']
        value_length_profile = cleaned_data['length_profile']
        value_limit_deformation = cleaned_data['limit_deformation']
        profile = cleaned_data["profile"]

        gammas = CountryFactors()
        gammas_country = gammas.finding_gammas(value_country)
        steel = SteelGrade()
        steel_grade = steel.finding_steel(value_steel)
        calculation = CalculationCFRHS(
            sectional_area=profile.A,
            second_moment_area=profile.Iy,
            yield_strength=steel_grade,
            length=value_length_profile,
            plastic_section=profile.Wply,
            sectional_axial_force=value_axial_force,
            sectional_bending_moment=value_bending_moment,
            eccentricity=value_eccentricity,
            gammas=gammas_country,
            limit_deformation=value_limit_deformation,
        )

        utilization_compression = calculation.check_utilization_with_compression()
        utilization_tension = calculation.check_utilization_with_tension()
        utilization_deformation = calculation.check_deformation()

        if (
            utilization_compression >= 1
            or utilization_tension >= 1
            or utilization_deformation >= 1
        ):
            messages.error(self.request, "Capacity exceeded !")
        else:
            messages.success(self.request, "Capacity ok !")

        context = {
            "form": form,
            "utilization_compression": utilization_compression,
            'utilization_tension': utilization_tension,
            'utilization_deformation': utilization_deformation,
        }

        detailed_obj = DetailedCalculationCfrhs(
            profile_radius_gyration=calculation.radius_of_gyration_iy(),
            buckling_curve=calculation.buckling_curve,
            buckling_factor=calculation.buckling_factor,
            epsilon=calculation.epsilon(),
            lambda_slenderness_1=calculation.lambda_slenderness_1(),
            buckling_length=calculation.buckling_length(),
            lambda_relative_slenderness=calculation.lambda_relative_slenderness(),
            theta_reduction_factor=calculation.theta_reduction_factor(),
            chi_reduction_factor=calculation.chi_reduction_factor(),
            tension_capacity=calculation.tension_capacity(),
            compression_capacity=calculation.compression_capacity(),
            total_bending=calculation.total_bending(),
            bending_capacity=calculation.bending_capacity(),
            total_deflection=calculation.total_deflection(),
        )

        if self.request.POST.get("show_data", ""):
            return HttpResponseRedirect(reverse("dashboard"))

        if self.request.POST.get("save_db", ""):
            detailed_obj.save()
            obj = form.save(commit=False)
            obj.author = self.request.user
            obj.profile = profile
            obj.utilization_compression = utilization_compression
            obj.utilization_tension = utilization_tension
            obj.utilization_deformation = utilization_deformation
            obj.detailed = detailed_obj
            obj.save()
            messages.success(self.request, "Connection was saved to Database !")
            context = {'form': form}
            return render(
                self.request, template_name=self.template_name, context=context
            )

        return render(self.request, template_name=self.template_name, context=context)
