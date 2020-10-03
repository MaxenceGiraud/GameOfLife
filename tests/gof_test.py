import unittest
import numpy as np
from GameOfLife import next_step

class Unittest(unittest.TestCase):
    def test_next_step_AllDead(self):
        self.assertTrue(np.all(next_step(np.zeros((100, 100), dtype=bool)) == np.zeros( (100, 100), dtype=bool)))


    def test_next_step_AllAlive(self):
        self.assertTrue(np.all( next_step(  np.ones((100, 100), dtype=bool)) == np.zeros(  (100, 100), dtype=bool)))


if __name__ == "__main__":
    unittest.main()