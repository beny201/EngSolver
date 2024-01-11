import factory
from faker import Faker

from bars_calculation.models import CalculationRhs, ProfileRhs
from distance_checker.models import Corner, Ridge

fake = Faker()


class CornerUseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Corner

    case = "case1"
    girder_angle = 30
    girder_height = 500
    t_flange_girder = 20
    column_width = 500
    t_flange_column = 20
    t_plate_connection = 20
    bolt_grade = "8_8"
    bolt_diameter = 20
    author = "empty"
    distance_top = 100
    distance_bottom = 100


class RidgeUseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ridge

    case = "case1"
    left_girder_angle = 30
    right_girder_angle = 30
    girder_height = 500
    left_t_flange_girder = 20
    right_t_flange_girder = 20
    t_plate_connection = 20
    bolt_grade = "8_8"
    bolt_diameter = 20
    author = "empty"
    distance_left = 100
    distance_right = 100


class ProfileRhsUseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProfileRhs

    name = 'test'
    H = 1
    B = 1
    T = 1
    G = 1
    surf = 1
    r0 = 1
    r1 = 1
    A = 1
    Ix = 1
    Iy = 1
    Iz = 1
    Wply = 1
    Wplz = 1


class CalculationRhsUseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CalculationRhs

    case = "case1"
    type_profile = 'CF'
    country = 'Denmark'
    steel = 'S235'
    axial_force = 10
    eccentricity_y = 10
    eccentricity_z = 10
    bending_moment_y = 10
    bending_moment_z = 10
    shear_force_y = 10
    shear_force_z = 10
    length_profile = 10
    buckling_factor = 10
    limit_deformation = 10
    profile = ('empty',)
    author = 'empty'
    cross_section_class = 1
