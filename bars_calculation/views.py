# Create your views here.
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import FormView

from bars_calculation.forms import CalculationRhsForm

from .calculation import (
    CalculationRHS,
    CountryFactors,
    CrossSectionClass,
    ForceToCalculation,
    ProfileRhsToCalculation,
    ReductionBucklingFactorsRHS,
    SteelGrade,
)
from .models import ProfileRhs


class CalculationRhsView(FormView):
    form_class = CalculationRhsForm
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
        value_type_profile = cleaned_data['type_profile']
        value_country = cleaned_data['country']
        value_steel = cleaned_data['steel']
        value_axial_force = cleaned_data['axial_force']
        value_eccentricity_y = cleaned_data['eccentricity_y']
        value_eccentricity_z = cleaned_data['eccentricity_z']
        value_bending_moment_y = cleaned_data['bending_moment_y']
        value_bending_moment_z = cleaned_data['bending_moment_z']
        value_shear_force_y = cleaned_data['shear_force_y']
        value_shear_force_z = cleaned_data['shear_force_z']
        value_length_profile = cleaned_data['length_profile']
        value_buckling_factor = cleaned_data['buckling_factor']
        value_limit_deformation = cleaned_data['limit_deformation']
        profile = cleaned_data["profile"]

        gammas = CountryFactors()
        gammas_country = gammas.finding_gammas(value_country)
        steel = SteelGrade()
        steel_grade = steel.finding_steel(value_steel)

        profile_to_calculation = ProfileRhsToCalculation(
            type_profile=value_type_profile,
            sectional_area=profile.A,
            height_profile=profile.H,
            width_profile=profile.B,
            thickness_flange=profile.T,
            second_moment_area_y=profile.Iy,
            second_moment_area_z=profile.Iz,
            yield_strength=steel_grade,
            length=value_length_profile,
            plastic_section_y=profile.Wply,
            plastic_section_z=profile.Wplz,
            radius=profile.r1,
        )

        forces = ForceToCalculation(
            sectional_axial_force=value_axial_force,
            sectional_bending_moment_y=value_bending_moment_y,
            sectional_bending_moment_z=value_bending_moment_z,
            sectional_shear_y=value_shear_force_y,
            sectional_shear_z=value_shear_force_z,
            eccentricity_y=value_eccentricity_y,
            eccentricity_z=value_eccentricity_z,
            main_axis="z",
            profile=profile_to_calculation,
        )

        buckling_factor_to_calculate = ReductionBucklingFactorsRHS(
            buckling_factor=value_buckling_factor, profile=profile_to_calculation
        )

        cross_section_class = CrossSectionClass(
            main_axis="z",
            sectional_force=forces,
            profile=profile_to_calculation,
        )

        calculation = CalculationRHS(
            sectional_forces=forces,
            gammas=gammas_country,
            limit_deformation=value_limit_deformation,
            main_axis="z",
            profile=profile_to_calculation,
            buckling_factor=buckling_factor_to_calculate,
            section_class=cross_section_class.check_class(),
        )

        if value_axial_force >= 0:
            axial_check = calculation.check_when_tensioned_and_bended()
        else:
            axial_check = calculation.check_interaction_buckling_and_bending()

        utilization_shear = calculation.check_total_shear()
        utilization_deformation = calculation.check_deformation()

        if utilization_deformation > 1 or utilization_shear > 1 or axial_check > 1:
            messages.error(self.request, "Capacity exceeded !")
        else:
            messages.success(self.request, "Capacity ok !")

        available_profiles = ProfileRhs.objects.filter(T__gte=3).order_by("G")

        filtered_profiles_tension = []
        filtered_profiles_compression = []
        for searched_profile in available_profiles:
            temp_profile = ProfileRhsToCalculation(
                type_profile=value_type_profile,
                sectional_area=searched_profile.A,
                height_profile=searched_profile.H,
                width_profile=searched_profile.B,
                thickness_flange=searched_profile.T,
                second_moment_area_y=searched_profile.Iy,
                second_moment_area_z=searched_profile.Iz,
                yield_strength=steel_grade,
                length=value_length_profile,
                plastic_section_y=searched_profile.Wply,
                plastic_section_z=searched_profile.Wplz,
                radius=searched_profile.r1,
            )

            temp_forces = ForceToCalculation(
                sectional_axial_force=value_axial_force,
                sectional_bending_moment_y=value_bending_moment_y,
                sectional_bending_moment_z=value_bending_moment_z,
                sectional_shear_y=value_shear_force_y,
                sectional_shear_z=value_shear_force_z,
                eccentricity_y=value_eccentricity_y,
                eccentricity_z=value_eccentricity_z,
                main_axis="z",
                profile=temp_profile,
            )

            temp_buckling_factor_to_calculate = ReductionBucklingFactorsRHS(
                buckling_factor=value_buckling_factor, profile=temp_profile
            )

            temp_cross_section_class = CrossSectionClass(
                main_axis="z",
                sectional_force=temp_forces,
                profile=temp_profile,
            )

            temp_calculation = CalculationRHS(
                sectional_forces=temp_forces,
                gammas=gammas_country,
                limit_deformation=value_limit_deformation,
                main_axis="z",
                profile=temp_profile,
                buckling_factor=temp_buckling_factor_to_calculate,
                section_class=temp_cross_section_class.check_class(),
            )

            if value_axial_force >= 0:
                if (
                    temp_calculation.check_when_tensioned_and_bended() <= 1
                    and temp_calculation.check_deformation() <= 1
                ):
                    filtered_profiles_tension.append(searched_profile)
            if value_axial_force < 0:
                if (
                    temp_calculation.check_interaction_buckling_and_bending() <= 1
                    and temp_calculation.check_deformation() <= 1
                ):
                    filtered_profiles_compression.append(searched_profile)
        context = {
            "form": form,
            "utilization_shear": utilization_shear,
            "utilization_compression": axial_check,
            'utilization_tension': axial_check,
            'utilization_deformation': utilization_deformation,
            'list_of_lightest_profiles_tension': filtered_profiles_tension[:4],
            'list_of_lightest_profiles_compression': filtered_profiles_compression[:4],
        }

        if value_axial_force >= 0:
            del context["utilization_compression"]
        else:
            del context["utilization_tension"]

        #
        # detailed_obj = DetailedCalculationRhs(
        #     profile_radius_gyration_y=calculation.radius_of_gyration_iy(),
        #     profile_radius_gyration_z=calculation.radius_of_gyration_iz(),
        #     shear_capacity_y=calculation.shear_capacity_y(),
        #     shear_capacity_z=calculation.shear_capacity_z(),
        #     reduction_due_shear=calculation.reduction_due_shear(),
        #     tension_profile=calculation.tension_profile(),
        #     check_tension_profile=calculation.check_tension_profile(),
        #     bending_capacity_profile_y=calculation.bending_capacity_profile_y(),
        #     bending_capacity_profile_z=calculation.bending_capacity_profile_z(),
        #     reduced_bending_capacity_y=calculation.reduced_bending_capacity_y(),
        #     reduced_bending_capacity_z=calculation.reduced_bending_capacity_z(),
        #     reduction_biaxial_bending_capacity=calculation.reduction_biaxial_bending_capacity(),
        #     check_interaction_axial_force_and_bending=calculation.check_interaction_axial_force_and_bending(),
        #     buckling_curve=calculation.buckling_curve,
        #     epsilon=calculation.epsilon(),
        #     lambda_slenderness_1=calculation.lambda_slenderness_1(),
        #     buckling_length=calculation.buckling_length(),
        #     lambda_relative_slenderness_y=calculation.lambda_relative_slenderness_y(),
        #     lambda_relative_slenderness_z=calculation.lambda_relative_slenderness_z(),
        #     theta_reduction_factor_y=calculation.theta_reduction_factor_y(),
        #     theta_reduction_factor_z=calculation.theta_reduction_factor_z(),
        #     chi_reduction_factor_y=calculation.chi_reduction_factor_y(),
        #     chi_reduction_factor_z=calculation.chi_reduction_factor_z(),
        #     compression_capacity_y=calculation.compression_capacity_y(),
        #     compression_capacity_z=calculation.compression_capacity_z(),
        #     check_buckling_y=calculation.check_buckling_y(),
        #     check_buckling_z=calculation.check_buckling_z(),
        #     check_total_buckling=calculation.check_total_buckling(),
        #     total_bending_my=calculation.total_bending_my(),
        #     total_bending_mz=calculation.total_bending_mz(),
        #     bending_capacity_y=calculation.bending_capacity_y(),
        #     bending_capacity_z=calculation.compression_capacity_z(),
        #     check_bending_y=calculation.check_bending_y(),
        #     check_bending_z=calculation.check_bending_z(),
        #     check_total_bending=calculation.check_total_bending(),
        #     Cmy=calculation.Cmy(),
        #     kyy=calculation.kyy(),
        #     kzz=calculation.kzz(),
        #     kzy=calculation.kzy(),
        #     kyz=calculation.kyz(),
        #     check_interaction_buckling_and_bending=calculation.check_interaction_buckling_and_bending(),
        #     check_deformation_y=calculation.check_deformation_y(),
        #     check_deformation_z=calculation.check_deformation_z(),
        #     check_deformation=calculation.check_deformation(),
        # )
        #
        # if self.request.POST.get("show_data", ""):
        #     return HttpResponseRedirect(reverse("dashboard"))
        #
        # if self.request.POST.get("save_db", ""):
        #     detailed_obj.save()
        #     obj = form.save(commit=False)
        #     obj.author = self.request.user
        #     obj.profile = profile
        #     obj.utilization_shear = utilization_compression
        #     obj.utilization_compression = utilization_compression
        #     obj.utilization_tension = utilization_tension
        #     obj.utilization_deformation = utilization_deformation
        #     obj.detailed = detailed_obj
        #     obj.save()
        #     messages.success(self.request, "Connection was saved to Database !")
        #     context = {'form': form}
        #     return render(
        #         self.request, template_name=self.template_name, context=context
        #     )

        return render(self.request, template_name=self.template_name, context=context)
