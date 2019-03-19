'''
Author  : Michael Borden
Date    : Feb 6, 2019
Update  : Feb 17, 2019

Purpose : Memory class helps with storing and recalling with the use of sqlite3.
'''
from datetime import date
import numpy as np
import os.path
import sqlite3

class Memory:
    def __init__(self)
    
    def load(self, dbFilename):
        self.memoryDB = sqlite3.connect(dbFilename)
        self.memory = self.memoryDB.cursor()
        self.brainInitVars = self.memory.execute('''
            select *
            from brainInitVars
            order by brainID desc
            limit 1;
        ''')[0]

    def init(self)
        self.memoryDB = sqlite3.connect(':memory:')
        self.memory = self.memoryDB.cursor()
        self.initSchemes()

    def getAFilename(self):
       filename = 'brain_'+str(date.today())
        count = 1
        while (not os.path.isfile(filename+'.db')):
           filename =filename[:16]+'('+str(count)+')'
            count += 1
        return filename

    def initSchemes(self):
        self.memory.execute('''
            create table brainInitVars (
                brainID integer primary key autoincrement,
                tdate text,
                learningRate real,
                topology text,
                inputNeurons integer,
                hiddenNeurons integer,
                outputNeurons integer,
                inputNeuronFilename text,
                hiddenNeuronFilename text,
                outputNeuronFilename text
            )
        ''')

    def saveMemory(self, close=False):
        self.memory.execute('''
            insert into brainInit
            values (date('now'), {}, {}, {}, {}, {})
        '''.format(self.learningRate, self.topology, self.network[0],
                   self.network[1], self.network[2]))
        with open(self.dbFilename) as f:
            for line in self.brainDB.iterdump():
                f.write('{}/n'.format(line))
        if (close):
            self.brainDB.close()
