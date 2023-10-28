from django import forms
from django.forms import ModelForm

from .models import Bolt, Corner

# class CornerForm(forms.Form):
#     girder_angle = forms.FloatField(
#         label="Girder angle [degree]",
#         min_value=1,
#         max_value=89,
#         initial=14.5
#     )
#     girder_height = forms.IntegerField(
#         label="Girder height [mm]",
#         min_value=1,
#         initial=400
#     )
#     t_flange_girder = forms.IntegerField(
#         label="Thickness of flange in girder [mm]",
#         min_value=1,
#         max_value=120,
#         initial=20
#     )
#     column_width = forms.IntegerField(
#         label="Column width [mm]",
#         min_value=1,
#         max_value=2000,
#         initial=900
#     )
#     t_flange_column = forms.IntegerField(
#         label="Thickness of flange in column [mm]",
#         min_value=1,
#         max_value=120,
#         initial=20
#     )
#     t_plate_connection = forms.IntegerField(
#         label="Thickness of plate in connection [mm]",
#         min_value=1,
#         initial=20
#     )
#     choices_bolt = (
#         ("8_8", "8.8"),
#         ("10_9", "10.9")
#     )
#     bolt_grade = forms.ChoiceField(choices=choices_bolt, )
#
#     bolt_diameter = forms.ModelChoiceField(
#         queryset=Bolt.objects.values_list("diameter",
#                                           flat=True).distinct().order_by(
#             "diameter"),
#         to_field_name='diameter',
#         initial=30
#     )


class CornerFormModel(ModelForm):
    bolt_diameter = forms.ModelChoiceField(
        queryset=Bolt.objects.values_list("diameter", flat=True)
        .distinct()
        .order_by("diameter"),
        to_field_name='diameter',
    )

    class Meta:
        model = Corner
        fields = [
            'case',
            'girder_angle',
            'girder_height',
            't_flange_girder',
            'column_width',
            't_flange_column',
            't_plate_connection',
            'bolt_grade',
            'bolt_diameter',
        ]
        labels = {
            'case': 'Name or number of case ',
            'girder_angle': 'Girder angle [degree]',
            'girder_height': "Girder height [mm]",
            't_flange_girder': "Thickness of flange in girder [mm]",
            'column_width': "Column width [mm]",
            't_flange_column': "Thickness of flange in column [mm]",
            't_plate_connection': 'Thickness of plate in connection [mm]',
        }

        widgets = {
            'girder_angle': forms.NumberInput(
                attrs={
                    'max': '89',
                    'min': '0.1',
                }
            ),
            'girder_height': forms.NumberInput(
                attrs={
                    'max': '2000',
                    'min': '100',
                }
            ),
            't_flange_girder': forms.NumberInput(
                attrs={
                    'max': '100',
                    'min': '5',
                }
            ),
            'column_width': forms.NumberInput(
                attrs={
                    'max': '2500',
                    'min': '100',
                }
            ),
            't_flange_column': forms.NumberInput(
                attrs={
                    'max': '100',
                    'min': '5',
                }
            ),
            't_plate_connection': forms.NumberInput(
                attrs={
                    'max': '150',
                    'min': '5',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['case'].initial = 1000
        self.fields['girder_angle'].initial = 14.5
        self.fields['girder_height'].initial = 400
        self.fields['t_flange_girder'].initial = 20
        self.fields['column_width'].initial = 400
        self.fields['t_flange_column'].initial = 20
        self.fields['t_plate_connection'].initial = 20
        self.fields['bolt_grade'].initial = "8_8"
        self.fields['bolt_diameter'].initial = 30


class RidgeForm(forms.Form):
    left_girder_angle = forms.FloatField(
        label="Left girder angle [degree]", min_value=1, max_value=89, initial=14.5
    )

    right_girder_angle = forms.FloatField(
        label="Right girder angle [degree]", min_value=1, max_value=89, initial=14.5
    )

    girder_height = forms.IntegerField(
        label="Girder height [mm]", min_value=1, initial=400
    )
    left_t_flange_girder = forms.IntegerField(
        label="Thickness of left flange in girder [mm]",
        min_value=1,
        max_value=120,
        initial=20,
    )

    right_t_flange_girder = forms.IntegerField(
        label="Thickness of right flange in girder [mm]",
        min_value=1,
        max_value=120,
        initial=20,
    )

    t_plate_connection = forms.IntegerField(
        label="Thickness of plate in connection [mm]", min_value=1, initial=20
    )
    choices_bolt = (("8_8", "8.8"), ("10_9", "10.9"))
    bolt_grade = forms.ChoiceField(
        choices=choices_bolt,
    )

    bolt_diameter = forms.ModelChoiceField(
        queryset=Bolt.objects.values_list("diameter", flat=True)
        .distinct()
        .order_by("diameter"),
        to_field_name='diameter',
        initial=30,
    )
