from django import forms
from django.forms import ModelForm

from bars_calculation.models import CalculationCfrhs, ProfileRhs

available_profiles = []


class CalculationCfrhsForm(ModelForm):
    profile = forms.ModelChoiceField(
        queryset=ProfileRhs.objects.values_list("name", flat=True)
        .filter(T__gte=3)
        .order_by("G"),
        to_field_name='name',
    )

    class Meta:
        model = CalculationCfrhs
        fields = [
            'case',
            'country',
            'steel',
            'axial_force',
            'eccentricity',
            'bending_moment',
            'length_profile',
            'limit_deformation',
        ]
        labels = {
            'case': 'Name or number of case ',
            'country': 'Country to chose (different ym)',
            'steel': 'Steel grade to chose',
            'axial_force': 'Sectional axial force[kN]',
            'eccentricity': 'Eccentricity for axial force [mm]',
            'bending_moment': "Sectional bending moment [kNm]",
            'length_profile': "Length of profile [m]",
            'limit_deformation': 'Limit of deformation x = [L/x = L/200]',
        }

        widgets = {
            'axial_force': forms.NumberInput(attrs={'max': '2500', 'min': '0'}),
            'eccentricity': forms.NumberInput(attrs={'max': '500', 'min': '0'}),
            'bending_moment': forms.NumberInput(attrs={'max': '2000', 'min': '0'}),
            'length_profile': forms.NumberInput(attrs={'max': '2000', 'min': '0.1'}),
            'limit_deformation': forms.NumberInput(attrs={'max': '2000', 'min': '50'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['case'].initial = 1000
        self.fields['country'].initial = "Denmark"
        self.fields['steel'].initial = "S355"
        self.fields['axial_force'].initial = 100
        self.fields['eccentricity'].initial = 10
        self.fields['bending_moment'].initial = 5
        self.fields['length_profile'].initial = 4
        self.fields['limit_deformation'].initial = 200
        # self.fields['profile'].initial = "SQUA100X100X5"
