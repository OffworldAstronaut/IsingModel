import numpy as np 
from typing import List

class IsingMetal():
    def __init__(self): 
        self.spins = []
        self.coupling = 0
        self.temperature = 0 # in kelvin
        self.energy = 0
        self.magnetization = 0
        self.external_field = 0
        
    def run_simulation(self) -> None:
        ...
    
    def _evolve_state(self) -> None:
        KB = 1.380649 * 10E-23
        
        energy_0 = self.calc_energy() 
        
        random_spin_idx = np.random.randint(0, len(self.spins))
        self._flip_spin(random_spin_idx)
        
        energy_1 = self.calc_energy()
        dE = energy_1 - energy_0
        
        if dE < 0:
            pass
        
        elif dE > 0:
            ...  
        
    def _flip_spin(self, spin_index) -> None:
        self.spins[spin_index] *= -1
            
    def reset_spins(self, metal_size: int) -> None:
        self.spins = np.random.choice([-1, 1], metal_size)
        
    def calc_magnetization(self) -> float:
        avg_spin = np.average(self.spins)
        return avg_spin
        
    def calc_energy(self) -> float:
        neigh_interac = self._calc_neighbor_interaction()
        extfield_interac = self._calc_extfield_interaction()
        
        total_energy = -1.0 * self.coupling * neigh_interac - extfield_interac
        return total_energy
        
    def _calc_neighbor_interaction(self) -> float:
        neigh_interac = 0
        
        for index, spin in enumerate(self.spins):
            if index < len(self.spins) - 1:
                neigh_interac += np.prod(spin, self.spins[index + 1])
                                
        return neigh_interac
    
    def _calc_extfield_interaction(self) -> float:
        ext_field_interac = 0
        
        for spin in self.spins:
            ext_field_interac += self.external_field * spin
            
        return ext_field_interac