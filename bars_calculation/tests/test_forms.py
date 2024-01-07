from django.test import TestCase

from ..forms import CalculationRhsForm
from ..models import ProfileRhs


class CalculationRhsFormTest(TestCase):
    def setUp(self):
        self.profile = ProfileRhs.objects.create(
            name='test',
            H=1,
            B=1,
            T=1,
            G=1,
            surf=1,
            r0=1,
            r1=1,
            A=1,
            Ix=1,
            Iy=1,
            Iz=1,
            Wply=1,
            Wplz=1,
        )
        self.profile_2 = ProfileRhs.objects.create(
            name='test2',
            H=4,
            B=4,
            T=4,
            G=4,
            surf=4,
            r0=4,
            r1=4,
            A=4,
            Ix=4,
            Iy=4,
            Iz=4,
            Wply=4,
            Wplz=4,
        )

    form = CalculationRhsForm()

    def test_profile_queryset_filtering(self):
        queryset = self.form.fields['profile'].queryset
        self.assertNotIn(self.profile, queryset)
        self.assertIn(self.profile_2, queryset)

    def test_if_form_have_proper_initial_values(self):
        country = self.form.fields['country'].initial
        self.assertIn('Denmark', country)
