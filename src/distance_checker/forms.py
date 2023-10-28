from django import forms
from django.forms import ModelForm

from .models import Bolt, Corner, Ridge

searched_bolt_standard = "14399-4"


class CornerFormModel(ModelForm):
    bolt_diameter = forms.ModelChoiceField(
        queryset=Bolt.objects.values_list("diameter", flat=True)
        .filter(standard__title=searched_bolt_standard)
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
            'girder_angle': forms.NumberInput(attrs={'max': '89', 'min': '0'}),
            'girder_height': forms.NumberInput(attrs={'max': '2000', 'min': '100'}),
            't_flange_girder': forms.NumberInput(attrs={'max': '100', 'min': '5'}),
            'column_width': forms.NumberInput(attrs={'max': '2500', 'min': '100'}),
            't_flange_column': forms.NumberInput(attrs={'max': '100', 'min': '5'}),
            't_plate_connection': forms.NumberInput(attrs={'max': '150', 'min': '5'}),
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


class RidgeFormModel(ModelForm):
    bolt_diameter = forms.ModelChoiceField(
        queryset=Bolt.objects.values_list("diameter", flat=True)
        .filter(standard__title=searched_bolt_standard)
        .distinct()
        .order_by("diameter"),
        to_field_name='diameter',
    )

    class Meta:
        model = Ridge
        fields = [
            'case',
            'left_girder_angle',
            'right_girder_angle',
            'girder_height',
            'left_t_flange_girder',
            'right_t_flange_girder',
            't_plate_connection',
            'bolt_grade',
            'bolt_diameter',
        ]

        labels = {
            'case': 'Name or number of case ',
            'left_girder_angle': 'Left girder angle [degree]',
            'right_girder_angle': "Right girder angle [degree]",
            'girder_height': 'Girder height [mm]',
            'left_t_flange_girder': 'Thickness of left flange in girder [mm]',
            'right_t_flange_girder': 'Thickness of right flange in girder [mm]',
            't_plate_connection': 'Thickness of plate in connection [mm]',
        }

        widgets = {
            'left_girder_angle': forms.NumberInput(attrs={'max': '89', 'min': '0'}),
            'right_girder_angle': forms.NumberInput(attrs={'max': '89', 'min': '0'}),
            'girder_height': forms.NumberInput(attrs={'max': '2000', 'min': '100'}),
            'left_t_flange_girder': forms.NumberInput(attrs={'max': '100', 'min': '5'}),
            'right_t_flange_girder': forms.NumberInput(
                attrs={'max': '100', 'min': '5'}
            ),
            't_plate_connection': forms.NumberInput(attrs={'max': '150', 'min': '5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['case'].initial = 1000
        self.fields['left_girder_angle'].initial = 14.5
        self.fields['right_girder_angle'].initial = 14.5
        self.fields['girder_height'].initial = 400
        self.fields['left_t_flange_girder'].initial = 20
        self.fields['right_t_flange_girder'].initial = 20
        self.fields['t_plate_connection'].initial = 20
        self.fields['bolt_grade'].initial = "8_8"
        self.fields['bolt_diameter'].initial = 30
