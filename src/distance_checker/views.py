from datetime import datetime

from django.shortcuts import render
from django.views import View

from .forms import CornerForm

from . import calculation
from .utils import creating_graph
from django.views.generic import FormView
from django.contrib import messages
from .utils import render_to_pdf


class BasicView(View):
    template_name = 'distance_checker/index.html'

    def get(self, request):
        return render(request, template_name=self.template_name)



class DistanceView(FormView):
    template_name = "distance_checker/frame_corner.html"
    form_class = CornerForm

    def _get_searched_assembly_parts(self, bolt_grade_value,
                                     bolt_diameter_value,
                                     t_plate_connection_value):

        bolt = calculation.FindingBolt()
        searched_bolt, searched_washer = bolt.searching_assembly_parts(
            bolt_grade_value,
            bolt_diameter_value,
            t_plate_connection_value)

        return searched_bolt, searched_washer

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        girder_angle_value = cleaned_data['girder_angle']
        girder_height_value = cleaned_data['girder_height']
        t_flange_girder_value = cleaned_data['t_flange_girder']
        column_width_value = cleaned_data['column_width']
        t_flange_column_value = cleaned_data['t_flange_column']
        t_plate_connection_value = (cleaned_data[
            't_plate_connection'])
        bolt_grade_value = cleaned_data['bolt_grade']
        bolt_diameter_value = cleaned_data['bolt_diameter']

        form = CornerForm(initial=cleaned_data)

        searched_bolt, searched_washer = self._get_searched_assembly_parts(
            bolt_grade_value, bolt_diameter_value, t_plate_connection_value
        )

        assembly_part = calculation.ThicknessPartsAssembly()

        total_length_bolt_value = assembly_part.total_length_bolt(
            searched_bolt)

        thickness_washer_value = searched_washer.thickness_washer

        space_for_screw_value = assembly_part.space_for_screw(
            searched_bolt, t_plate_connection_value)

        corner = calculation.CreatingCorner()

        try:
            lines, searched_distance = corner.creating_lines(
                girder_angle=girder_angle_value,
                girder_height=girder_height_value,
                t_flange_girder=t_flange_girder_value,
                column_width=column_width_value,
                t_flange_column=t_flange_column_value,
                t_plate_connection=t_plate_connection_value,
                length_bolt=searched_bolt.length,
                total_length_bolt=total_length_bolt_value,
                thickness_washer=thickness_washer_value,
                space_for_screw=space_for_screw_value,
            )

            distance_from_bottom, distance_from_top = searched_distance

            image_data = creating_graph(*lines)
            context = {'form': form, "image_data": image_data,
                       "distance_from_bottom": round(distance_from_bottom, 0),
                       "distance_from_top": round(distance_from_top, 0)}

            if "save_to_pdf" == self.request.POST.get("save_pdf", ""):
                current_date = datetime.now()
                formatted_datetime = current_date.strftime(
                    "%d-%m-%Y %H:%M")
                data = {
                    'title': "Corner connection",
                    'date':formatted_datetime,
                    'girder_angle_value': girder_angle_value,
                    'girder_height_value': girder_height_value,
                    't_flange_girder_value': t_flange_girder_value,
                    'column_width_value': column_width_value,
                    't_flange_column_value': t_flange_column_value,
                    't_plate_connection_value': t_plate_connection_value,
                    'used_bolt': searched_bolt,
                    "distance_from_bottom": round(distance_from_bottom, 0),
                    "distance_from_top": round(distance_from_top, 0),
                    "image_data": image_data,
                }
                response = render_to_pdf('pdfs/connection.html', data,
                                         'corner')
                return response

        except:
            messages.error(self.request,
                           "Something went wrong, please check once more geometry of connection")
            context = {'form': form, }

        return render(self.request, template_name=self.template_name,
                      context=context)
