#!/usr/bin/env python

import os
import sys
import unittest

try:
    from atooms.adapters.atoomsf90 import Simulation, System
    SKIP = False
except ImportError:
    SKIP = True

# TODO: refactor adapters tests, they should be unique (except for constructors) because the interface is the same

class TestAtooms(unittest.TestCase):

    def setUp(self):
        if SKIP:
            self.skipTest('no atooms')
        self.file_ref = 'reference/kalj/config.dat'
        self.ref_u = -4805.69761109

    def test_potential_energy(self):
        s = System(self.file_ref)
        self.assertAlmostEqual(s.potential_energy(), self.ref_u)

    def test_potential_energy_from_simulation(self):
        s = Simulation(self.file_ref)
        self.assertAlmostEqual(s.system.potential_energy(), self.ref_u)

    def test_simulation_run(self):
        ref = -4740.46362485
        file_output = '/tmp/test_atooms_run.h5'
        s = Simulation(self.file_ref, file_output,
                       opts={'--dt':0.001, '-c':1, '-e':1})
        s.run(10)
        self.assertAlmostEqual(s.system.potential_energy(), ref)
        os.remove(file_output)

if __name__ == '__main__':
    unittest.main(verbosity=0)
