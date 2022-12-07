'''
Author  : Michael Borden
Date    : Feb 16, 2019
Update  : Feb 17, 2019
Purpose : Simulation of the human brain using SNN.
'''
from Neuron import Neuron
from Memory import Memory
import numpy as np

class Brain:
    def __init__(self, dbFilename=None, learningRate=0.001, topology='ff'
                 inputNeurons=1, hiddenNeurons=1, outputNeurons=1):
        self.memory = Memory()
        if (dbFilename):
            self.memory.load(dbFilename)
            self.filename = dbFilename
            self.brainID = self.memory.brainScheme[0]
            self.learningRate = self.memory.brainScheme[2]
            self.topology = self.memory.brainScheme[3]
            self.network  = {'input':  self.memory.brainScheme[4],
                             'hidden': self.memory.brainScheme[5],
                             'output': self.memory.brainScheme[6]}
        else:
            self.memory.init()
            self.filename = self.memory.getAFilename()
            self.brainID = self.memory.brainScheme[0]
            self.learningRate = learningRate
            self.topology = topology            # {feedforward, resevoir}
            self.network  = {'input':  inputNeurons,
                             'hidden': hiddenNeurons,
                             'output': outputNeurons}
            self.ineurons = list()                  # Input neurons count
            self.hneurons = list()                  # Hidden neuron count
            self.oneurons = list()                  # Output neuron count
            if (topology in ['ff', 'feedforward']):
                self.buildFeedforward()
            elif (topology in ['rs', 'resevoir']):
                self.buildReservoir()

    def buildFeedForward(self):
        odict = dict()
        for o in range(self.network['output']):
            self.oneurons.append(Neuron([o, 2, 0]), 
                                 self.learningRate, 'output')
            odict[self.oneurons[-1].address] = self.oneurons[-1]
        hdict = dict()
        for h in range(self.network['hidden']):
            self.hneurons.append(Neuron([h, 1, 0]), 
                                 self.learningRate, 'hidden')
            hdict[self.hneurons[-1].address] = self.hneurons[-1]
            for o in range(self.oneurons):      # oneuron preSynaptic
                o.preSynaptic[self.oneurons[-1].address] = self.bttrRndDist()
            self.hneurons[-1].postSynaptic = odict # hneuron postSynaptic
        ilist = list()
        for i in range(self.network['input']):
            self.ineurons.append(Neuron([i, 0, 0]), 
                                 self.learningRate)
            ilist.append(self.ineurons[-1])
            for h in range(self.hneurons):      # hneuron preSynaptic
                h.preSynaptic[self.hneurons[-1].address] = self.bttrRndDist()
            self.ineurons[-1].postSynaptic = hdict # ineuron postSynaptic

    def buildReservoir(self):
        pass

    def bttrRndDist(self):
        pv = np.random.normal(0.5, 0.1)
        nv = np.random.normal(-0.5, 0.1)
        return np.random.choice([nv, pv])

    def simulate(self, spikeTrainMatrix):
        # Run the simulation, given input trains, and log neural activities
        pass

    def show(self):
        # Graph and show network and logged activities in animation. Plotly?
        pass
