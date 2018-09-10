import unittest

from openaerostruct.structures.wing_weight_loads import StructureWeightLoads
from openaerostruct.structures.total_loads import TotalLoads
from openaerostruct.utils.testing import run_test, get_default_surfaces
from openmdao.api import Group, IndepVarComp
import numpy as np

class Test(unittest.TestCase):

    def test_0(self):
        surface = get_default_surfaces()[0]

        comp = TotalLoads(surface=surface)

        run_test(self, comp, complex_flag=True)

    def test_1(self):
        surface = get_default_surfaces()[0]
        surface['struct_weight_relief'] = True

        comp = TotalLoads(surface=surface)

        run_test(self, comp, complex_flag=True)

    def test_2(self):
        surface = get_default_surfaces()[0]
        surface['distributed_fuel_weight'] = True

        comp = TotalLoads(surface=surface)

        run_test(self, comp, complex_flag=True)

    def test_3(self):
        surface = get_default_surfaces()[0]

        comp = StructureWeightLoads(surface=surface)

        group = Group()

        indep_var_comp = IndepVarComp()

        ny = surface['num_y']

        nodesval = np.array([[0., 0., 0.],
                            [0., 1., 0.],
                            [0., 2., 0.],
                            [0., 3., 0.]],dtype=complex)
        element_weights_val = np.arange(ny-1)

        indep_var_comp.add_output('nodes', val=nodesval,units='m')
        indep_var_comp.add_output('element_weights', val=element_weights_val,units='N')

        group.add_subsystem('indep_var_comp', indep_var_comp, promotes=['*'])
        group.add_subsystem('load', comp, promotes=['*'])

        p = run_test(self, group, complex_flag=True)

        print(p['comp.struct_weight_loads'])

if __name__ == '__main__':
    unittest.main()
