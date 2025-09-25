# Imports / Dependencies
import numpy as np                  # Numerical utilities
import matplotlib.pyplot as plt     # Plotting
from typing import Tuple            # Typing

class IsingMetal:
    # Boltzmann's constant -- by default normalized
    KB = 1.0
    
    def __init__(self, dim: Tuple[int, int], coupling: float, temp: float, ext_field: float):
        """Creates an object representing a sheet of metal. 

        Args:
            dim (Tuple[int, int]): dimensions of the metallic sheet, can be 1D or 2D
            coupling (float): coupling interaction between spins
            temp (float): the solid's temperature (in Kelvin)
            ext_field (float): external magnetic field strength
        """
        self.spins = np.zeros(shape=(dim))
        self.reset_spins()
        self.coupling = coupling
        self.temperature = temp
        self.external_field = ext_field
        
    def run_simulation(self, steps: int = 1_000) -> None:
        """Evolves the system's state over a certain amount of time and animates the spins as a heatmap.

        Args:
            steps (int, optional): Total simulation time. Defaults to 1_000.
        """
        import matplotlib.animation as animation

        # Steps array for data register and loop making
        steps_arr = np.arange(steps)
        # Stores the spins through time
        spins_evolution = []
        # Regulates the "interval" of each data registering / "photography"; 
        # Smaller intervals generate finer details but larger data quantity
        # and slower code. 
        photo_interval = 100


        # Main simulation loop
        for step in steps_arr:
            self._evolve_state()
            
            # Data registering
            if step % photo_interval == 0:
                # Store a copy to avoid referencing the same array
                spins_evolution.append(self.spins.copy())
                
                data = f"{step}    {self._calc_energy()}   {self._calc_magnetization()}\n"
                self._register_data(data)

        # Animation setup
        fig, ax = plt.subplots()
        im = ax.imshow(spins_evolution[0], cmap='coolwarm', vmin=-1, vmax=1, origin='lower')
        ax.set_title("Ising Model Spin Evolution")

        def update(frame):
            im.set_data(spins_evolution[frame])
            ax.set_xlabel(f"Step: {frame * photo_interval}")
            return [im]

        ani = animation.FuncAnimation(
            fig, update, frames=len(spins_evolution), interval=20, blit=True, repeat=False
        )
        
        ani.save(filename="ising_animation.gif")
        
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
        total_energy = -1.0 * self.coupling * neigh_interac - extfield_interac
        return total_energy
        
    def _calc_neighbor_interaction(self) -> float:
        """Computes the neighbor interaction factor for the total energy calc. 

        Returns:
            float: Neighboring spins interaction energy
        """
        neigh_interac_hor = 0
        neigh_interac_ver = 0
        
        # Stores the rows and cols for condensed loop typing
        rows = self.spins.shape[0]
        cols = self.spins.shape[1]
            
        # Traverses all spins
        # Note: the modulo induces a periodic boundary condition
        for i in range(0, rows):
            for j in range(0, cols):
                # Calcs the interaction between spins in the same row
                neigh_interac_hor += self.spins[i][j] * self.spins[i][(j + 1) % cols]
                # Calcs the interaction between spins in the same column
                neigh_interac_ver += self.spins[i][j] * self.spins[(i + 1) % rows][j]

        neigh_interac = neigh_interac_hor + neigh_interac_ver
        return neigh_interac
    
    def _calc_extfield_interaction(self) -> float:
        """Computes the external magnetic field interaction factor for the total energy calc.

        Returns:
            float: External field interaction
        """
                
        ext_field_interac = np.sum(self.external_field * self.spins)
            
        return ext_field_interac
    
    def _evolve_state(self) -> None:
        """Evolves the system to the next state with a Metropolis-Hastings algorithm."""
        
        # Picks a random spin
        random_spin_row, random_spin_col = np.random.randint(0, self.spins.shape[0]), np.random.randint(0, self.spins.shape[1])
    
        # Computes the energy difference if that spin is flipped
        dE = self._calc_dE(random_spin_row, random_spin_col)
        
        # If the energy is lower, accept the flip 
        if dE <= 0:
            self._flip_spin((random_spin_row, random_spin_col))
            
        # If the energy is higher, accepts the flip with a probability proportional to temperature
        else:
            prob_accept = np.exp(-dE / (IsingMetal.KB * self.temperature))
            if np.random.random() < prob_accept:
                self._flip_spin((random_spin_row, random_spin_col))

        
    def _calc_dE(self, spin_row: int, spin_col: int) -> float:
        """Computes the difference in energy generated by a spin flip

        Args:
            spin_row (int): spin's row coordinate
            spin_col (int): spin's col coordinate

        Returns:
            float: energy diff
        """
        rows, cols = self.spins.shape
        
        # Selects the chosen spin's value
        chosen_spin = self.spins[spin_row, spin_col]
        
        # Nearest-neighbors sum
        nn_sum = np.sum([
            self.spins[(spin_row + 1) % rows, spin_col],
            self.spins[(spin_row - 1) % rows, spin_col],
            self.spins[spin_row, (spin_col + 1) % cols],
            self.spins[spin_row, (spin_col - 1) % cols]
        ])
        
        # Computes the energy diff 
        dE = 2.0 * self.coupling * chosen_spin * nn_sum + 2.0 * self.external_field * chosen_spin
        return dE
        
    def _flip_spin(self, spin_pos: Tuple[int, int]) -> None:
        """Auxiliar function to flip a certain spin's value given its position.

        Args:
            spin_position (int): tuple with the position of the to-be-flipped spin.
        """
        self.spins[spin_pos[0], spin_pos[1]] *= -1