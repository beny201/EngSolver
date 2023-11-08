# Create your views here.
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import FormView

from bars_calculation.forms import CalculationCfrhsForm

from .calculation import CalculationCFRHS, CountryFactors, SteelGrade
from .models import ProfileRhs


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
        # value_case = cleaned_data['case']
        value_country = cleaned_data['country']
        value_steel = cleaned_data['steel']
        value_axial_force = cleaned_data['axial_force']
        value_eccentricity = cleaned_data['eccentricity']
        value_bending_moment = cleaned_data['bending_moment']
        value_length_profile = cleaned_data['length_profile']
        value_limit_deformation = cleaned_data['limit_deformation']
        profile = ProfileRhs.objects.get(name=cleaned_data["profile"])

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

        utilization_compression = round(
            calculation.check_utilization_with_compression(), 2
        )
        utilization_tension = round(calculation.check_utilization_with_tension(), 2)
        utilization_deformation = round(calculation.check_deformation(), 2)

        if (
            utilization_compression >= 1
            or utilization_tension >= 1
            or utilization_deformation >= 1
        ):
            messages.error(self.request, "Capacity exceeded !")

        context = {
            "form": form,
            "utilization_compression": utilization_compression,
            'utilization_tension': utilization_tension,
            'utilization_deformation': utilization_deformation,
        }

        if self.request.POST.get('show_data'):
            context = {}
            return render(
                self.request,
                template_name=self.template_name_detailed,
            )

        return render(self.request, template_name=self.template_name, context=context)
