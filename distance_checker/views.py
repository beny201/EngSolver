from datetime import datetime

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import FormView, TemplateView

from .calculation import (
    CreatingCorner,
    CreatingRidge,
    FindingBolt,
    ThicknessPartsAssembly,
)
from .forms import CornerFormModel, RidgeFormModel
from .utils import creating_graph, render_to_pdf


class BasicView(TemplateView):
    template_name = 'distance_checker/index.html'


class DistanceCornerView(FormView):
    template_name = "distance_checker/frame_connection.html"
    form_class = CornerFormModel

    title = "Corner distance"
    connection_type = "Corner checker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['connection_type'] = self.connection_type
        return context

    def _get_searched_assembly_parts(
        self, bolt_grade_value, bolt_diameter_value, t_plate_connection_value
    ):
        bolt = FindingBolt()
        searched_bolt, searched_washer = bolt.searching_assembly_parts(
            bolt_grade_value, bolt_diameter_value, t_plate_connection_value
        )

        return searched_bolt, searched_washer

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        case_value = cleaned_data['case']
        girder_angle_value = cleaned_data['girder_angle']
        girder_height_value = cleaned_data['girder_height']
        t_flange_girder_value = cleaned_data['t_flange_girder']
        column_width_value = cleaned_data['column_width']
        t_flange_column_value = cleaned_data['t_flange_column']
        t_plate_connection_value = cleaned_data['t_plate_connection']
        bolt_grade_value = cleaned_data['bolt_grade']
        bolt_diameter_value = cleaned_data['bolt_diameter']

        form = CornerFormModel(initial=cleaned_data)
        searched_bolt, searched_washer = self._get_searched_assembly_parts(
            bolt_grade_value, bolt_diameter_value, t_plate_connection_value
        )

        assembly_part = ThicknessPartsAssembly()

        total_length_bolt_value = assembly_part.total_length_bolt(searched_bolt)

        space_for_screw_value = assembly_part.space_for_screw(
            searched_bolt, t_plate_connection_value
        )
        corner = CreatingCorner()
        try:
            lines, searched_distance = corner.creating_lines(
                girder_angle=girder_angle_value,
                girder_height=girder_height_value,
                t_flange_girder=t_flange_girder_value,
                column_width=column_width_value,
                t_flange_column=t_flange_column_value,
                t_plate_connection=t_plate_connection_value,
                total_length_bolt=total_length_bolt_value,
                space_for_screw=space_for_screw_value,
            )

            raw_distance_from_bottom, raw_distance_from_top = searched_distance

            distance_from_bottom = assembly_part.adding_w_bolt_head(
                searched_bolt, raw_distance_from_bottom
            )

            distance_from_top = assembly_part.adding_w_bolt_head(
                searched_bolt, raw_distance_from_top
            )

            image_data = creating_graph(*lines)
            context = {
                'form': form,
                "image_data": image_data,
                "distance_from_bottom": round(distance_from_bottom),
                "distance_from_top": round(distance_from_top),
                'title': self.title,
                'connection_type': self.connection_type,
            }

            if self.request.POST.get("save_pdf", ""):
                current_date = datetime.now()
                formatted_datetime = current_date.strftime("%d-%m-%Y %H:%M")
                data = {
                    'case': case_value,
                    'date': formatted_datetime,
                    'girder_angle_value': girder_angle_value,
                    'girder_height_value': girder_height_value,
                    't_flange_girder_value': t_flange_girder_value,
                    'column_width_value': column_width_value,
                    't_flange_column_value': t_flange_column_value,
                    't_plate_connection_value': t_plate_connection_value,
                    'used_bolt': searched_bolt,
                    "distance_from_bottom": round(distance_from_bottom),
                    "distance_from_top": round(distance_from_top),
                    "image_data": image_data,
                }

                name_pdf = f'Corner - {case_value}'
                response = render_to_pdf('pdfs/connection_corner.html', data, name_pdf)
                return response

            if (
                self.request.POST.get("save_db", "")
                and self.request.user.is_authenticated
            ):
                form = CornerFormModel(self.request.POST)
                corner = form.save(commit=False)
                corner.author = self.request.user
                corner.distance_top = round(distance_from_top)
                corner.distance_bottom = round(distance_from_bottom)
                corner.save()
                messages.success(self.request, "Connection was saved to Database !")
                context = {'form': form}
                return render(
                    self.request, template_name=self.template_name, context=context
                )

        except Exception:
            messages.error(
                self.request,
                "Something went wrong, please check once more geometry of connection",
            )
            context = {'form': form}
        return render(self.request, template_name=self.template_name, context=context)


class DistanceRidgeView(FormView):
    template_name = "distance_checker/frame_connection.html"
    form_class = RidgeFormModel

    title = "Ridge distance"
    connection_type = "Ridge checker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['connection_type'] = self.connection_type

        return context

    def _get_searched_assembly_parts(
        self, bolt_grade_value, bolt_diameter_value, t_plate_connection_value
    ):
        bolt = FindingBolt()
        searched_bolt, searched_washer = bolt.searching_assembly_parts(
            bolt_grade_value, bolt_diameter_value, t_plate_connection_value
        )

        return searched_bolt, searched_washer

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        case_value = cleaned_data['case']
        left_girder_angle_value = cleaned_data['left_girder_angle']
        right_girder_angle_value = cleaned_data['right_girder_angle']
        girder_height_value = cleaned_data['girder_height']
        left_t_flange_girder_value = cleaned_data['left_t_flange_girder']
        right_t_flange_girder_value = cleaned_data['right_t_flange_girder']
        t_plate_connection_value = cleaned_data['t_plate_connection']
        bolt_grade_value = cleaned_data['bolt_grade']
        bolt_diameter_value = cleaned_data['bolt_diameter']

        form = RidgeFormModel(initial=cleaned_data)

        searched_bolt, searched_washer = self._get_searched_assembly_parts(
            bolt_grade_value, bolt_diameter_value, t_plate_connection_value
        )

        assembly_part = ThicknessPartsAssembly()

        total_length_bolt_value = assembly_part.total_length_bolt(searched_bolt)

        space_for_screw_value = assembly_part.space_for_screw(
            searched_bolt, t_plate_connection_value
        )

        ridge = CreatingRidge()

        try:
            lines, searched_distance = ridge.creating_lines(
                left_girder_angle=left_girder_angle_value,
                right_girder_angle=right_girder_angle_value,
                girder_height=girder_height_value,
                left_t_flange_girder=left_t_flange_girder_value,
                right_t_flange_girder=right_t_flange_girder_value,
                t_plate_connection=t_plate_connection_value,
                total_length_bolt=total_length_bolt_value,
                space_for_screw=space_for_screw_value,
            )

            raw_distance_from_left, raw_distance_from_right = searched_distance

            distance_from_left = assembly_part.adding_w_bolt_head(
                searched_bolt, raw_distance_from_left
            )

            distance_from_right = assembly_part.adding_w_bolt_head(
                searched_bolt, raw_distance_from_right
            )

            image_data = creating_graph(*lines)
            context = {
                'form': form,
                "image_data": image_data,
                "distance_from_left": round(distance_from_left),
                "distance_from_right": round(distance_from_right),
                'title': self.title,
                'connection_type': self.connection_type,
            }

            if self.request.POST.get("save_pdf") and self.request.user.is_authenticated:
                current_date = datetime.now()
                formatted_datetime = current_date.strftime("%d-%m-%Y %H:%M")
                data = {
                    'case': case_value,
                    'date': formatted_datetime,
                    'left_girder_angle_value': left_girder_angle_value,
                    'right_girder_angle_value': right_girder_angle_value,
                    'girder_height_value': girder_height_value,
                    'left_t_flange_girder_value': left_t_flange_girder_value,
                    'right_t_flange_girder_value': right_t_flange_girder_value,
                    't_plate_connection_value': t_plate_connection_value,
                    'used_bolt': searched_bolt,
                    "distance_from_left": round(distance_from_left),
                    "distance_from_right": round(distance_from_right),
                    "image_data": image_data,
                }

                name_pdf = f'Ridge - {case_value}'
                response = render_to_pdf('pdfs/connection_ridge.html', data, name_pdf)
                return response

            if self.request.POST.get("save_db"):
                form = RidgeFormModel(self.request.POST)
                ridge = form.save(commit=False)
                ridge.author = self.request.user
                ridge.distance_left = round(distance_from_left)
                ridge.distance_right = round(distance_from_right)
                ridge.save()
                messages.success(self.request, "Connection was saved to Database !")
                context = {'form': form}
                return render(
                    self.request, template_name=self.template_name, context=context
                )

        except Exception:
            messages.error(
                self.request,
                "Something went wrong, please check once more geometry of connection",
            )
            context = {'form': form}

        return render(self.request, template_name=self.template_name, context=context)
