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
        self.u_rest = Voltage(-65., 'm')    # Constant membrane potential
        self.u = deepcopy(self.u_rest)      # Membrane potential
        self.𝜗 = Voltage(20, 'm')           # Axon Hillock threashold
        self.preSynaptic = dict()           # {Address: Weight}
        self.postSynaptic = dict()          # {Address: Neuron}
        self.historyStack = deque()         # [Address, Time]
        self.hpt = 0                        # Hyperpolerization time
        self.t = 0                          # Time step (milliseconds)
        random.seed(time())

    def dendrite(self, address, t):
        self.t = t
        self.historyStack(address)
        self.STDP(False)
        synapticPotial = self.preSynaptic[address]
        self.u += Voltage(synapticPotial, 'm')
        self.PSP = self.u + self.u_rest
        self.axonHillock()

    def historyStack(self, address):
        # Remove anything longer than 20ms old
        l = len(self.historyStack)
        dt = self.t - self.historyStack[0][1]
        while(l > 0 and dt > 20):
            dt = self.t - self.historyStack[0][1]
            self.historyStack.popleft()
            l -= 1
        if ((self.hpt - self.t) >= 0):
            self.STDP(address)
        self.historyStack.append([address, self.t])

    def axonHillock(self):
        if (self.PSP >= self.𝜗):
            self.STDP()
            self.actionPotential()

    def actionPotential(self):
        self.hpt[0] = self.t + 20
        for neuron in self.postSynaptic.values:
            neuron.dendrite(self.address, self.t+1)
    
    def STDP(self, address=None):
        l = len(self.historyStack)
        if (address == None):
            i, dt = 1, self.t - self.historyStack[0][1]
            while(i < l and dt > 0):
                # Depolarize synaptic weights by learning rate
                dt = self.t - self.historyStack[i][1]
                i += 1
        else:
            # Hyperpolarize synaptic weight by learning rate
            
    def hashAddress(self, index_h_i_j):
        self.address  = hex(index_h_i_j[0])[2:]+','
        self.address += hex(index_h_i_j[1])[2:]+','
        self.address += hex(index_h_i_j[2])[2:]
