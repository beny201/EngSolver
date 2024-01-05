import factory
from faker import Faker

from bars_calculation.models import ProfileRhs

fake = Faker()


class ProfileRhsUseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProfileRhs

    name = factory.LazyAttribute(lambda x: fake.name())
    H = factory.Faker('random_int', min=100, max=300)
    B = factory.Faker('random_int', min=100, max=300)
    T = factory.Faker('pyfloat', min_value=4, max_value=10)
    G = factory.Faker('pyfloat', min_value=4, max_value=10)
    surf = factory.Faker('pyfloat', min_value=4, max_value=10)
    r0 = factory.Faker('pyfloat', min_value=4, max_value=10)
    r1 = factory.Faker('pyfloat', min_value=4, max_value=10)
    A = factory.Faker(
        'pyfloat', min_value=16.55 * (10**2), max_value=20.55 * (10**2)
    )
    Ix = factory.Faker(
        'pyfloat', min_value=348.05 * (10**4), max_value=500.05 * (10**4)
    )
    Iy = factory.Faker(
        'pyfloat', min_value=348.05 * (10**4), max_value=500.05 * (10**4)
    )
    Iz = factory.Faker(
        'pyfloat', min_value=348.05 * (10**4), max_value=500.05 * (10**4)
    )
    Wply = factory.Faker(
        'pyfloat', min_value=69.05 * (10**3), max_value=150.05 * (10**3)
    )
    Wplz = factory.Faker(
        'pyfloat', min_value=69.05 * (10**3), max_value=150.05 * (10**3)
    )
