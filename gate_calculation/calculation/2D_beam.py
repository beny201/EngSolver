# Example of a simply supported beam with a uniform distributed load.
# Units used in this example are inches and kips
# This example does not use load combinations. The program will create a
# default load combindation called 'Combo 1'

# Import `FEModel3D` from `PyNite`
from PyNite import FEModel3D

# Create a new finite element model
beam = FEModel3D()

# Add nodes (in m)
beam.add_node('N1', 0, 0, 0)
beam.add_node('N2', 10, 0, 0)

# Define a material
E = 210_000_000  # Modulus of elasticity (kPa) /
G = 81_000  # Shear modulus of elasticity (kPa)
nu = 0.3  # Poisson's ratio
rho = 2.836e-4 * (25.4**3) / 1e9  # Density (kg/mm3)
beam.add_material('Steel', E, G, nu, rho)

# Add a beam with the following properties:
# Iy = 100 mm^4, Iz = 150 mm^4, J = 250 mm^4, A = 20 mm^2
beam.add_member('M1', 'N1', 'N2', 'Steel', 100, 150, 250, 20)

# Provide simple supports
beam.def_support('N1', True, True, True, False, False, False)
beam.def_support('N2', True, True, True, True, False, False)

# kN/m
beam.add_member_dist_load('M1', 'Fz', -1, -1, 0, 10)

# Alternatively the following line would do apply the load to the full
# length of the member as well
# beam.add_member_dist_load('M1', 'Fy', 200/1000/12, 200/1000/12)

# Analyze the beam
beam.analyze()

# Print the shear, moment, and deflection diagrams
beam.Members['M1'].plot_shear('Fz')
beam.Members['M1'].plot_moment('My')
beam.Members['M1'].plot_deflection('dz')

# Print reactions at each end of the beam
print('Left Support Reaction:', beam.Nodes['N1'].RxnFY, 'kip')
print('Right Support Reacton:', beam.Nodes['N2'].RxnFY, 'kip')
print('Right Support Reacton:', beam.Nodes['N2'].RxnFY, 'kip')

# Render the deformed shape of the beam magnified 100 times, with a text
# height of 5 inches
from PyNite.Visualization import Renderer

renderer = Renderer(beam)
renderer.annotation_size = 1
renderer.deformed_shape = True
renderer.deformed_scale = 100
renderer.render_loads = True
renderer.render_model()
