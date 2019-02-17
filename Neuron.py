from EE import Power, Voltage, Current, Resistance 
from copy import deepcopy
from collections import deque
from time import time
import random

'''
PoNS Page 33.    ::   Amplitude(mV)  | Duration                | Summation
Receptor potentials   Small (0.1-10) | Brief (5-100ms)         | Graded
Synaptic potentials   Small (0.1-10) | Brief->Long (5ms-20min) | Graded
Action potentials     Large (70-110) | Brief (1-10ms)          | All-or-none
'''

class Neuron:
    def __init__(self, index_h_i_j, learning_rate):
        self.hashAddress(index_h_i_j)
        self.learning_rate = learning_rate
        self.u_rest = Voltage(-65., 'm')        # Constant membrane potential
        self.u = deepcopy(self.u_rest)          # Membrane potential
        self.𝜗 = Voltage(20, 'm')               # Axon Hillock threshold
        self.preSynaptic = dict()               # {Address: Weight}
        self.postSynaptic = dict()              # {Address: Neuron}
        self.historyStack = deque()             # [Address, Time]
        self.hpt = 0                            # Hyperpolerization time
        self.t = 0                              # Time step (milliseconds)
        random.seed(time())

    def hashAddress(self, index_h_i_j):
        self.address  = hex(index_h_i_j[0])[2:]+'.' # Hex address converted
        self.address += hex(index_h_i_j[1])[2:]+'.' # to a string to be used
        self.address += hex(index_h_i_j[2])[2:]     # as key in dict().

    def dendrite(self, address, t):
        self.t = t                              # Update current time
        self.historyStack(address)              # Record presynaptic potential
        synapticPotial = self.preSynaptic[address] # Get synaptic weight
        self.u += Voltage(synapticPotial, 'm')  # Update membrane potential
        self.PSP = self.u + self.u_rest         # Update postsynaptic potential
        self.axonHillock()                      # Move to axonHillock()

    def historyStack(self, address):
        l = len(self.historyStack)              # Record length of stack
        dt = self.t - self.historyStack[0][1]   # Record time since oldest spike
        while(l > 0 and dt > 20):               # For all older than 20ms
            self.historyStack.popleft()         # Erase from historyStack
            dt = self.t - self.historyStack[0][1] # Record next spike dt
            l -= 1                              # Update loop condition
        self.historyStack.append([address, self.t]) # Append to historyStack
    
    def STDP(self, depolarization):
        if (depolarization):                    # If depolarization:
            self.hpt[1] = self.t + 20           # Hyperpolarization next 20ms
            for address, t in self.historyStack:# Depolarize all in historyStack
                # Depolarize synaptic weights by learning rate and distance from
                dt = self.t - t if (self.t - t > 0) else 1 # recent fire
                self.preSynaptic[address] *= Voltage(1+(self.learning_rate/dt))
        else:                                   # Else hyperpolarization:
            dhpt = self.hpt - self.t            # Difference in hpt
            if (dhpt > 0):                      # If Hyperpolerization active
                address = self.historyStack[-1][0] # Get most recent address
                # Hyperpolarize synaptic weight by learning rate
                self.preSynaptic[address] *= \
                                        Voltage(1-(self.learning_rate*(dt/20)))

    def axonHillock(self):
        if (self.PSP >= self.𝜗):                # If PSP > threshold : FIRE!!!
            self.STDP(True)                     # Activate STDP learning
            self.actionPotential()              # Move to actionPotential()
        else:                                   # Else
            self.STDP(False)                    # Check hyperpolerization

    def actionPotential(self):
        for neuron in self.postSynaptic.values: # For each neuron linked to axon
            neuron.dendrite(self.address, self.t+1) # Postsynaptic potential
