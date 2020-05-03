import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from src.neural_network import NeuralNetwork
from src.weightset import WeightSet

import unittest
import numpy as np

class TestNeuralNetwork(unittest.TestCase):
    def test_assignment(self):
        for _ in range(10):
            w = WeightSet(2, 2, 2)
            w.mutate()
            nn = NeuralNetwork(2, 2, 2, w)

            nn.setWeights( w )
            self.assertEqual(nn.getArr(), w.getWeights().flatten().tolist())
        

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
import tensorflow as tf

suite = unittest.TestLoader().loadTestsFromTestCase(TestNeuralNetwork)
unittest.TextTestRunner(verbosity=2).run(suite)