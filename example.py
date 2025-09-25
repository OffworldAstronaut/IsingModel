# Imports
from Ising import IsingMetal

# parameters
coupling = 1.0
temp = 1.0
ext_field = 0.0
dim = (100, 100)

# Creates the model 
metal = IsingMetal(dim=dim, coupling=coupling, temp=temp, ext_field=ext_field)
# Runs it
metal.run_simulation(100_000)