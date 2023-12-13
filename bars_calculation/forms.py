from bars_calculation.models import CalculationRhs, ProfileRhs
from django import forms
from django.forms import ModelForm

available_profiles = []


class CalculationRhsForm(ModelForm):
    profile = forms.ModelChoiceField(
        queryset=ProfileRhs.objects.filter(T__gte=3).order_by("G"),
        to_field_name='name',
    )

    class Meta:
        model = CalculationRhs
        fields = [
            'case',
            'type_profile',
            'country',
            'steel',
            'axial_force',
            'eccentricity_y',
            'eccentricity_z',
            'bending_moment_y',
            'bending_moment_z',
            'shear_force_y',
            'shear_force_z',
            'length_profile',
            'buckling_factor',
            'limit_deformation',
        ]
        labels = {
            'case': 'Name or number of case ',
            'type_profile': 'Type of used bar (different buckling curve)',
            'country': 'Country to chose (different ym)',
            'steel': 'Steel grade to chose',
            'axial_force': 'Sectional axial force[kN]' '- Compression negative',
            'eccentricity_y': 'Eccentricity for axial force in y [mm]',
            'eccentricity_z': 'Eccentricity for axial force in z [mm]',
            'bending_moment_y': "Sectional bending moment My [kNm]",
            'bending_moment_z': "Sectional bending moment Mz [kNm]",
            'shear_force_y': "Sectional shear force Vy [kN]",
            'shear_force_z': "Sectional shear force Vz [kN]",
            'buckling_factor': "Buckling length factor [u]",
            'length_profile': "Length of profile [m]",
            'limit_deformation': 'Limit of deformation x = [L/x = L/200]',
        }

        widgets = {
            'axial_force': forms.NumberInput(attrs={'max': '2500', 'min': '-1000'}),
            'eccentricity_y': forms.NumberInput(attrs={'max': '500', 'min': '0'}),
            'eccentricity_z': forms.NumberInput(attrs={'max': '500', 'min': '0'}),
            'bending_moment_y': forms.NumberInput(attrs={'max': '2000', 'min': '0'}),
            'bending_moment_z': forms.NumberInput(attrs={'max': '2000', 'min': '0'}),
            'shear_force_y': forms.NumberInput(attrs={'max': '2000', 'min': '0'}),
            'shear_force_z': forms.NumberInput(attrs={'max': '2000', 'min': '0'}),
            'buckling_factor': forms.NumberInput(attrs={'max': '10', 'min': '0'}),
            'length_profile': forms.NumberInput(attrs={'max': '2000', 'min': '0.1'}),
            'limit_deformation': forms.NumberInput(attrs={'max': '2000', 'min': '50'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['case'].initial = 1000
        self.fields['type_profile'].initial = "CF"
        self.fields['country'].initial = "Denmark"
        self.fields['steel'].initial = "S355"
        self.fields['axial_force'].initial = 100
        self.fields['eccentricity_y'].initial = 0
        self.fields['eccentricity_z'].initial = 0
        self.fields['bending_moment_y'].initial = 5
        self.fields['bending_moment_z'].initial = 0
        self.fields['shear_force_y'].initial = 0
        self.fields['shear_force_z'].initial = 5
        self.fields['buckling_factor'].initial = 1
        self.fields['length_profile'].initial = 4
        self.fields['limit_deformation'].initial = 200
        # self.fields['profile'].initial = "SQUA100X100X5"
