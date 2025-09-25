import numpy as np 
import matplotlib.pyplot as plt
from typing import Tuple

class IsingMetal:
    # Boltzmann's constant
    KB = 1.380649e-23
    
    def __init__(self, dim: Tuple[int, int], coupling: float, temp: float, ext_field: float):
        """Creates an object representing a sheet of metal. 

        Args:
            dim (Tuple[int, int]): dimensions of the metallic sheet, can be 1D or 2D
            coupling (float): coupling interaction between spins
            temp (float): the solid's temperature (in Kelvin)
            ext_field (float): external magnetic field strength
        """
        self.spins = np.zeros(shape=(dim))
        self.coupling = coupling
        self.temperature = temp
        self.external_field = ext_field
        
    def run_simulation(self, steps: int = 1_000) -> None:
        """Evolves the system's state over a certain amount of time. 

        Args:
            steps (int, optional): Total simulation time. Defaults to 1_000.
        """
        for i in range(steps):
            # Evolves a state in the system
            self._evolve_state()
            
            # Stores the measured quantities
            data = f"{i}    {self._calc_energy()}   {self._calc_magnetization()}\n"
            self._register_data(data)
        
    def reset_spins(self) -> None:
        """Resets the spins to a default, random, configuration."""
        self.spins = np.random.choice([-1, 1], self.spins.shape)
        
    def _register_data(self, data: str):
        """Auxiliar function for measurement registering into a file.

        Args:
            data (str): measurements taken and formatted, ready for storage.
        """
        # Filename formatting 
        filename = f"ising_data_c={self.coupling:.2f}_t={self.temperature:.2f}_h={self.external_field:.2f}.dat"
        # File output
        with open(filename, "a+") as f:
            f.write(data)
        
    def _calc_magnetization(self) -> float:
        """Auxiliar function to measure the metal's magnetization (spins arithmetic avg)

        Returns:
            float: average spin
        """
        avg_spin = np.average(self.spins)
        return avg_spin
        
    def _calc_energy(self) -> float:
        """Auxiliar function to measure the current state energy (computes the hamiltonian).

        Returns:
            float: the current state energy
        """
        # Computes the neighbor interaction factor 
        neigh_interac = self._calc_neighbor_interaction()
        # Computes the external interaction factor
        extfield_interac = self._calc_extfield_interaction()
        
        # Computes total energy 
        total_energy = -1.0 * neigh_interac - extfield_interac
        return total_energy
        
    def _calc_neighbor_interaction(self) -> float:
        """Computes the neighbor interaction factor for the total energy calc. 

        Returns:
            float: Neighboring spins interaction energy
        """
        neigh_interac = 0
        
        for i in range(len(self.spins)):
            neigh_interac += self.coupling * self.spins[i] * self.spins[(i+1) % len(self.spins)]

        return neigh_interac
    
    def _calc_extfield_interaction(self) -> float:
        """Computes the external magnetic field interaction factor for the total energy calc.

        Returns:
            float: External field interaction
        """
        ext_field_interac = 0
        
        for spin in self.spins:
            ext_field_interac += self.external_field * spin
            
        return ext_field_interac
    
    def _evolve_state(self) -> None:
        """Evolves the system to the next state with a Metropolis-Hastings algorithm."""
        
        # Current energy of the system
        energy_0 = self.calc_energy() 
    
        # Picks a random spin and flips it
        random_spin_idx = np.random.randint(0, len(self.spins))
        self._flip_spin(random_spin_idx)
        
        # Computes the system's energy after the flip 
        energy_1 = self.calc_energy()
        
        # Computes the energy difference, before and after 
        dE = energy_1 - energy_0
        
        # Accepts the flip if the energy is now lower 
        if dE < 0:
            pass
        
        # Accepts the flip under a certain probability in function of the temperature
        elif dE > 0:
            prob_accept = np.exp((-1.0 * dE) / (IsingMetal.KB * self.temperature))
            
            if np.random.random() <= prob_accept:
                pass
            else: 
                self._flip_spin(random_spin_idx)
        
    def _flip_spin(self, spin_index: int) -> None:
        """Auxiliar function to flip a certain spin's value given its index.

        Args:
            spin_index (int): index of the to-be-flipped spin.
        """
        self.spins[spin_index] *= -1