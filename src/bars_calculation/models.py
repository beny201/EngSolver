from django.contrib.auth.models import User
from django.db import models


class ProfileRhs(models.Model):
    name = models.CharField(max_length=50)  # name
    H = models.IntegerField(help_text="Height of the object [mm]")  # DIM1
    B = models.IntegerField(help_text="Width of the object [mm]")  # DIM2
    T = models.FloatField(help_text="Thickness of the web [mm]")  # DIM3
    G = models.FloatField(help_text="Nominal weight per [kg/m]")  # MASS
    surf = models.FloatField(help_text="Painting surface [/m]")  # SURF
    r0 = models.FloatField(help_text="Radius r0 [mm]")  # RS
    r1 = models.FloatField(help_text="Radius r1 [mm]")  # RA
    A = models.FloatField(help_text="Cross-section area [mm^2]")  # SX
    Iy = models.FloatField(help_text="Moment of inertia about the Y [mm^4]")  # IY
    Iz = models.FloatField(help_text="Moment of inertia about the Z [mm^4]")  # IZ
    Wply = models.FloatField(help_text="plastic_section Wply [mm^3]")  # MSY
    Wplz = models.FloatField(help_text="plastic_section Wplz [mm^3]")  # MSZ

    def __str__(self):
        return f'{self.name}'


class CalculationCfrhs(models.Model):
    case = models.CharField(max_length=50)
    country = models.CharField(
        choices=[
            ("Denmark", "Denmark"),
            ("Germany", "Germany"),
            ("Norway", "Norway"),
            ("Sweden", "Sweden"),
        ]
    )
    steel = models.CharField(
        choices=[("S235", "S235"), ("S275", "S275"), ("S355", "S355")]
    )
    axial_force = models.FloatField()
    eccentricity = models.FloatField()
    bending_moment = models.FloatField()
    length_profile = models.FloatField()
    limit_deformation = models.FloatField()
    profile = models.ForeignKey(ProfileRhs, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    utilization_compression = models.IntegerField(null=True)
    utilization_tension = models.IntegerField(null=True)
    utilization_deformation = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.case} + {self.profile}'
