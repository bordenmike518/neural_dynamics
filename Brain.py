'''
Author  : Michael Borden
Date    : Feb 16, 2019
Update  : Feb 17, 2019

Purpose : Simulation of the human brain using SNN.
'''
from Neuron import Neuron
import numpy as np

class Brain:
    def __init__(self):
        self.age = 0
    
    def build(self, learning_rate, topology, 
              input_neurons, hidden_neurons, output_neurons):
        self.learning_rate = learning_rate
        self.topology = topology                # {feedforward, resevoir}
        self.network  = {'input':  input_neurons,
                         'hidden': hidden_neurons,
                         'output': output_neurons}
        self.ineurons = list()                  # Input neurons count
        self.hneurons = list()                  # Hidden neuron count
        self.oneurons = list()                  # Output neuron count
        if (topology in ['ff', 'feedforward']):
            self.buildFeedforward()
        elif (topology in ['rs', 'resevoir']):
            self.buildResevoir()

    def buildFeedForward(self):
        odict = dict()
        for o in range(self.network['output']):
            self.oneurons.append(Neuron([o, 2, 0]), 
                                 self.learning_rate, 'output')
            odict[self.oneurons[-1].address] = self.oneurons[-1]
        hdict = dict()
        for h in range(self.network['hidden']):
            self.hneurons.append(Neuron([h, 1, 0]), 
                                 self.learning_rate, 'hidden')
            hdict[self.hneurons[-1].address] = self.hneurons[-1]
            for o in range(self.oneurons):      # oneuron preSynaptic
                o.preSynaptic[self.oneurons[-1].address] = self.bttrRndDist()
            self.hneurons[-1].postSynaptic = odict # hneuron postSynaptic
        ilist = list()
        for i in range(self.network['input']):
            self.ineurons.append(Neuron([i, 0, 0]), 
                                 self.learning_rate)
            ilist.append(self.ineurons[-1])
            for h in range(self.hneurons):      # hneuron preSynaptic
                h.preSynaptic[self.hneurons[-1].address] = self.bttrRndDist()
            self.ineurons[-1].postSynaptic = hdict # ineuron postSynaptic

    def buildResevoir(self):
        pass

    def bttrRndDist(self):
        pv = np.random.normal(0.5, 0.1)
        nv = np.random.normal(-0.5, 0.1)
        return np.random.choice([nv, pv])

    def simulate(self):
        # Run the simulation, given input trains, and log neural activities
        pass

    def show(self):
        # Graph and show network and logged activities in animation. Plotly?
        pass
