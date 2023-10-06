from django import forms
from .models import Bolt


class CornerForm(forms.Form):
    girder_angle = forms.FloatField(
        label="Girder angle [degree]",
        min_value=1,
        max_value=89,
        initial=14.5
    )
    girder_height = forms.IntegerField(
        label="Girder height [mm]",
        min_value=1,
        initial=400
    )
    t_flange_girder = forms.IntegerField(
        label="Thickness of flange in girder [mm]",
        min_value=1,
        max_value=120,
        initial=20
    )
    column_width = forms.IntegerField(
        label="Column width [mm]",
        min_value=1,
        max_value=2000,
        initial=900
    )
    t_flange_column = forms.IntegerField(
        label="Thickness of flange in column [mm]",
        min_value=1,
        max_value=120,
        initial=20
    )
    t_plate_connection = forms.IntegerField(
        label="Thickness of plate in connection [mm]",
        min_value=1,
        initial=20
    )
    choices_bolt = (
        ("8_8", "8.8"),
        ("10_9", "10.9")
    )
    bolt_grade = forms.ChoiceField(choices=choices_bolt,)

    bolt_diameter = forms.ModelChoiceField(
        queryset=Bolt.objects.values_list("diameter", flat=True).distinct().order_by("diameter"),
        to_field_name='diameter',
        initial=30
    )

