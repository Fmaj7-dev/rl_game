import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from src.weightset import WeightSet

import unittest
import numpy as np

class TestWeightSet(unittest.TestCase):
    def test_random(self):
        w = WeightSet(2, 2, 2)

        self.assertEqual( w.getSize(), 12 )
        print()
        print("-----> weight set zeros:")
        print(w)

        w.mutate(0.5)
        print("-----> weight set mutated:")
        print(w)
    
    def test_constructor(self):
        arr = np.zeros(12)
        WeightSet(2, 2, 2, arr)

    def test_mix(self):
        w1 = WeightSet(2, 2, 2)
        w2 = WeightSet(2, 2, 2)
        w2.mutate(1)

        print()
        print("-----> w1:")
        print(w1)

        print("-----> w2:")
        print(w2)

        wmix = WeightSet.mix(w1, w2)

        print("-----> wmix:")
        print(wmix)


suite = unittest.TestLoader().loadTestsFromTestCase(TestWeightSet)
unittest.TextTestRunner(verbosity=2).run(suite)