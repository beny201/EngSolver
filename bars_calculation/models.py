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
    Ix = models.FloatField(help_text="Torsional moment of inertia [mm^2]")  # IX",
    Iy = models.FloatField(help_text="Moment of inertia about the Y [mm^4]")  # IY
    Iz = models.FloatField(help_text="Moment of inertia about the Z [mm^4]")  # IZ
    Wply = models.FloatField(help_text="plastic_section Wply [mm^3]")  # MSY
    Wplz = models.FloatField(help_text="plastic_section Wplz [mm^3]")  # MSZ

    def __str__(self):
        return f'{self.name}'


class DetailedCalculationRhs(models.Model):
    profile_radius_gyration_y = models.FloatField()
    profile_radius_gyration_z = models.FloatField()
    shear_capacity_y = models.FloatField()
    shear_capacity_z = models.FloatField()
    reduction_due_shear = models.FloatField()
    tension_profile = models.FloatField()
    check_tension_profile = models.FloatField()
    bending_capacity_profile_y = models.FloatField()
    bending_capacity_profile_z = models.FloatField()
    reduced_bending_capacity_y = models.FloatField()
    reduced_bending_capacity_z = models.FloatField()
    reduction_biaxial_bending_capacity = models.FloatField()
    check_interaction_axial_force_and_bending = models.FloatField()
    buckling_curve = models.CharField()
    epsilon = models.FloatField()
    lambda_slenderness_1 = models.FloatField()
    buckling_length = models.FloatField()
    lambda_relative_slenderness_y = models.FloatField()
    lambda_relative_slenderness_z = models.FloatField()
    theta_reduction_factor_y = models.FloatField()
    theta_reduction_factor_z = models.FloatField()
    chi_reduction_factor_y = models.FloatField()
    chi_reduction_factor_z = models.FloatField()
    compression_capacity_y = models.FloatField()
    compression_capacity_z = models.FloatField()
    check_buckling_y = models.FloatField()
    check_buckling_z = models.FloatField()
    check_total_buckling = models.FloatField()
    total_bending_my = models.FloatField()
    total_bending_mz = models.FloatField()
    bending_capacity_y = models.FloatField()
    bending_capacity_z = models.FloatField()
    check_bending_y = models.FloatField()
    check_bending_z = models.FloatField()
    check_total_bending = models.FloatField()
    Cmy = models.FloatField()
    kyy = models.FloatField()
    kzz = models.FloatField()
    kzy = models.FloatField()
    kyz = models.FloatField()
    check_interaction_buckling_and_bending = models.FloatField()
    check_deformation_y = models.FloatField()
    check_deformation_z = models.FloatField()
    check_deformation = models.FloatField()
    last_modified_date = models.DateTimeField(auto_now=True)


class CalculationRhs(models.Model):
    case = models.CharField(max_length=50)
    type_profile = models.CharField(
        choices=[
            ("CF", "Cold formed"),
            ("HF", "Hot formed"),
        ]
    )
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
    eccentricity_y = models.FloatField()
    eccentricity_z = models.FloatField()
    bending_moment_y = models.FloatField()
    bending_moment_z = models.FloatField()
    shear_force_y = models.FloatField()
    shear_force_z = models.FloatField()
    length_profile = models.FloatField()
    buckling_factor = models.FloatField()
    limit_deformation = models.FloatField()
    profile = models.ForeignKey(ProfileRhs, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    utilization_shear = models.FloatField(null=True)
    utilization_compression = models.FloatField(null=True)
    utilization_tension = models.FloatField(null=True)
    utilization_deformation = models.FloatField(null=True)
    detailed = models.ForeignKey(
        DetailedCalculationRhs, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f'{self.case} + {self.profile}'
