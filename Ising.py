import numpy as np 
from time import time
from typing import List

class IsingMetal():
    KB = 1.380649e-23
    
    def __init__(self, coupling, temp, ext_field): 
        self.spins = []
        self.coupling = coupling
        self.temperature = temp # in kelvin
        self.external_field = ext_field
        
    def run_simulation(self, steps: int = 1_000) -> None:
        for i in range(steps):
            self._evolve_state()
            
            data = f"{i}    {self.calc_energy()}   {self.calc_magnetization()}\n"
            self.register_data(data)
        
    def register_data(self, data: str):
        with open(f"ising_data_c={self.coupling:.2f}_t={self.temperature:.2f}_h={self.external_field:.2f}.dat", "a+") as f:
            f.write(data)
        
    def reset_spins(self, metal_size: int) -> None:
        self.spins = np.random.choice([-1, 1], metal_size)
        
    def calc_magnetization(self) -> float:
        avg_spin = np.average(self.spins)
        return avg_spin
        
    def calc_energy(self) -> float:
        neigh_interac = self._calc_neighbor_interaction()
        extfield_interac = self._calc_extfield_interaction()
        
        total_energy = -1.0 * neigh_interac - extfield_interac
        return total_energy
        
    def _calc_neighbor_interaction(self) -> float:
        neigh_interac = 0
        
        for i in range(len(self.spins)):
            neigh_interac += self.coupling * self.spins[i] * self.spins[(i+1) % len(self.spins)]

        return neigh_interac
    
    def _calc_extfield_interaction(self) -> float:
        ext_field_interac = 0
        
        for spin in self.spins:
            ext_field_interac += self.external_field * spin
            
        return ext_field_interac
    
    def _evolve_state(self) -> None:
        energy_0 = self.calc_energy() 
        
        random_spin_idx = np.random.randint(0, len(self.spins))
        self._flip_spin(random_spin_idx)
        
        energy_1 = self.calc_energy()
        dE = energy_1 - energy_0
        
        if dE < 0:
            pass
        
        elif dE > 0:
            prob_accept = np.exp((-1.0 * dE) / (IsingMetal.KB * self.temperature))
            
            if np.random.random() <= prob_accept:
                pass
            else: 
                self._flip_spin(random_spin_idx)
        
    def _flip_spin(self, spin_index) -> None:
        self.spins[spin_index] *= -1