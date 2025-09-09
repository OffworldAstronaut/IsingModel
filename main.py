from Ising import IsingMetal

coupling = 10
temp = 273
ext_field = 1

metal = IsingMetal(coupling=coupling, temp=temp, ext_field=ext_field)

metal.reset_spins(200)
metal.run_simulation(2_500)