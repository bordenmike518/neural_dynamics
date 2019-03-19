'''
Author  : Michael Borden
Date    : Feb 10, 2019
Update  : Feb 17, 2019

Purpose : Simulation of a single spiking neuron.
'''
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
    def __init__(self, indexXYZ, learningRate, ntype):
        self.hashAddress(indexXYZ)
        self.learningRate = learningRate
        self.type = ntype
        self.uRest = Voltage(-65., 'm')        # Constant membrane potential
        self.u = deepcopy(self.uRest)          # Membrane potential
        self.𝜗 = Voltage(20, 'm')               # Axon Hillock threshold
        self.preSynaptic = dict()               # {Address: Weight} Dentrites
        self.postSynaptic = dict()              # {Address: Neuron} Axon 
        self.historyStack = deque()             # [Address, Time]
        self.hpt = 0                            # Hyperpolerization time
        self.t = 0                              # Time step (milliseconds)
        random.seed(time())

    def hashAddress(self, indexXYZ):           # Up to 3 dim addressing for
        self.iaddress = indexXYZ               # more advanced topologies.
        self.address  = hex(indexXYZ[0])[2:]+'.' # Hex address converted
        self.address += hex(indexXYZ[1])[2:]+'.' # to a string to be used
        self.address += hex(indexXYZ[2])[2:]     # as key in dict().

    def dendrite(self, address, t):
        self.t = t                              # Update current time
        self.historyStack(address)              # Record presynaptic potential
        synapticPotial = self.preSynaptic[address] # Get synaptic weight
        self.u += Voltage(synapticPotial, 'm')  # Update membrane potential
        self.PSP = self.u + self.uRest         # Update postsynaptic potential
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
                # Depolarize synaptic weights by learning rate and distance ...
                dt = self.t - t if (self.t - t > 0) else 1 #...from recent spike
                self.preSynaptic[address] *= Voltage(1+(self.learningRate/dt))
        else:                                   # Else hyperpolarization:
            dhpt = self.hpt - self.t            # Difference in hpt
            if (dhpt > 0):                      # If Hyperpolerization active
                address = self.historyStack[-1][0] # Get most recent address
                # Hyperpolarize synaptic weight by learning rate
                self.preSynaptic[address] *= \
                                        Voltage(1-(self.learningRate*(dt/20)))

    def axonHillock(self):
        if (self.PSP >= self.𝜗):                # If PSP > threshold : FIRE!!!
            self.STDP(True)                     # Activate STDP learning
            self.actionPotential()              # Move to actionPotential()
        else:                                   # Else
            self.STDP(False)                    # Check hyperpolerization

    def actionPotential(self):
        if (self.type == 'output'):
            print('Output Potential')           # TODO: LOG!!*~*~*~*~*~*~*~*~*~*
        for neuron in self.postSynaptic.values: # For each neuron linked to axon
            neuron.dendrite(self.address, self.t+1) # Postsynaptic potential
            print('{} Potential'.format(self.address)) # TODO: LOG!! *~*~*~*~*~*
