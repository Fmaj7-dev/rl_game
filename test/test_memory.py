import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from src.memory import Memory

import unittest
import numpy as np

class TestMemory(unittest.TestCase):
    def test_push_size(self):
        mem = Memory(200)

        state = [100]*10
        action = [1, 2]
        reward = 0

        for i in range(1, 50):
            mem.push(state, action, reward)
            self.assertEqual(mem.size(), i)
        
        mem.clear()

        for i in range(1, 300):
            mem.push(state, action, reward)
        
        self.assertEqual(mem.size(), 200)

    def test_randomize(self):
        mem = Memory()

        state = [1]*10
        action = [1]
        reward = 1
        mem.push(state, action, reward)

        state = [2]*10
        action = [2]
        reward = 2
        mem.push(state, action, reward)

        state = [3]*10
        action = [3]
        reward = 3
        mem.push(state, action, reward)

        state = [4]*10
        action = [4]
        reward = 4
        mem.push(state, action, reward)

        mem.randomize()
        print(mem)
        self.assertEqual(mem.size(), 4)

    def test_get(self):
        mem = Memory()

        state_0 = [1]*10
        action_0 = [1]
        reward_0 = 1
        mem.push(state_0, action_0, reward_0)

        state_1 = [2]*10
        action_1 = [2]
        reward_1 = 2
        mem.push(state_1, action_1, reward_1)

        state0, action0, reward0 = mem.get(0)
        state1, action1, reward1 = mem.get(1)
        
        self.assertEqual(state_0, state0)
        self.assertEqual(state_1, state1)

        self.assertEqual(action_0, action0)
        self.assertEqual(action_1, action1)

        self.assertEqual(reward_0, reward0)
        self.assertEqual(reward_1, reward1)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf

suite = unittest.TestLoader().loadTestsFromTestCase(TestMemory)
unittest.TextTestRunner(verbosity=2).run(suite)