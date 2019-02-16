import numpy as np
from EE import Power, Voltage, Current, Resistance 

class neuron:

    def __init__(self):
        self.u      = Voltage(0.0)           # Potential difference
        self.u_rest = Voltage(-65., 'm')     # Constant membrane potential
        
