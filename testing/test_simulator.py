import os
import unittest

import numpy as np
import pandas as pd

from oopnet.report import *

from testing.base import CTownModel, MicropolisModel, PoulakisEnhancedPDAModel, RulesModel, SimpleModel, \
    activate_all_report_parameters, set_dir_testing, PatternCurveModel


class SimulatorTest(unittest.TestCase):
    def read_data(self, filename):
        def strip_index_columns(df):
            df = df.rename(columns=lambda x: x.strip())
            df.index = [x.strip() for x in df.index]
            return df

        def replace_invalid_vals(df):
            return df.replace('#N\/A\s+', np.nan, regex=True)

        set_dir_testing()
        node_results = pd.read_excel(filename, sheet_name='nodes', engine='openpyxl', index_col=0)
        node_results = replace_invalid_vals(node_results)
        self.node_results = strip_index_columns(node_results)
        link_results = pd.read_excel(filename, sheet_name='links', engine='openpyxl', index_col=0)
        link_results = replace_invalid_vals(link_results)
        self.link_results = strip_index_columns(link_results)

    def compare_elevation(self):
        self.assertTrue(all(self.node_results['Elevation'].sort_index() == self.rpt.elevation))

    def compare_demand(self):
        self.assertTrue(all(self.node_results['Demand'].sort_index() == self.rpt.demand))

    def compare_consumption(self):
        self.assertTrue(all(self.node_results['Consumption'].sort_index() == self.rpt.consumption))

    def compare_head(self):
        self.assertTrue(all(self.node_results['Head'].sort_index() == self.rpt.head))

    def compare_pressure(self):
        self.assertTrue(all(self.node_results['Pressure'].sort_index() == self.rpt.pressure))

    def compare_length(self):
        length = self.link_results['Length'].sort_index().fillna(0)
        self.assertTrue(all(length == self.rpt.length))

    def compare_flow(self):
        self.assertTrue(all(self.link_results['Flow'].sort_index() == self.rpt.flow))

    def compare_velocity(self):
        self.assertTrue(all(self.link_results['Velocity'].sort_index() == self.rpt.velocity))

    def compare_headloss(self):
        headloss = self.link_results['Unit Headloss'].sort_index().fillna(0)
        self.assertTrue(all(headloss == self.rpt.headlossper1000m))

    def compare_ffactor(self):
        ffactor = self.link_results['Friction Factor'].sort_index().fillna(0)
        ffactor = ffactor.round(2)
        self.assertTrue(all(ffactor == self.rpt.ffactor))


class CTownSimulatorTest(SimulatorTest):
    def setUp(self) -> None:
        self.model = CTownModel()
        activate_all_report_parameters(self.model.network)
        self.rpt = self.model.network.run(output=True)
        self.read_data(os.path.join('networks', 'C-town.xlsx'))

    def test_data(self):
        self.compare_elevation()
        self.compare_pressure()
        self.compare_demand()
        self.compare_head()
        self.compare_length()
        self.compare_flow()
        self.compare_velocity()
        self.compare_headloss()
        # self.compare_ffactor()
        # self.compare_status()


class CTownPythonPDMSimulatorTest(SimulatorTest):
    def setUp(self) -> None:
        self.model = CTownModel()
        activate_all_report_parameters(self.model.network)
        self.rpt = self.model.network.run(simulator='PYTHON_PDM')
        # self.rpt = self.model.network.run(simulator='PYTHON_PDM', delete=False, path='Ouputs', output=True)
        for comp_rpt, comp_vars in \
                ((self.rpt.nodes, ('Elevation', 'Pressure', 'Demand', 'Consumption', 'Head')),
                 (self.rpt.links, ('Length', 'Flow', 'Velocity', 'Headloss'))):
            for var_name in comp_vars:
                comp_rpt.loc[dict(vars=var_name)] = comp_rpt.loc[dict(vars=var_name)].round(2)
        self.read_data(os.path.join('networks', 'C-town_PDM.xlsx'))

    def test_data(self):
        self.compare_elevation()
        self.compare_pressure()
        self.compare_demand()
        self.compare_consumption()
        self.compare_head()
        self.compare_length()
        self.compare_flow()
        self.compare_velocity()
        self.compare_headloss()


class MicropolisSimulatorTest(SimulatorTest):
    def setUp(self) -> None:
        self.model = MicropolisModel()


class PoulakisEnhancedPDASimulatorTest(SimulatorTest):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()
        activate_all_report_parameters(self.model.network)
        self.rpt = self.model.network.run(output=True)
        self.read_data(os.path.join('networks', 'Poulakis_enhanced_PDA.xlsx'))

    def test_pump_headloss(self):
        p_pump = self.rpt.headloss['P-1']
        self.assertEqual(-5.28, p_pump)

    def test_data(self):
        self.compare_elevation()
        self.compare_pressure()
        self.compare_demand()
        self.compare_head()
        self.compare_length()
        self.compare_flow()
        self.compare_velocity()
        self.compare_headloss()
        # self.compare_ffactor()
        # self.compare_status()


class RulesModelSimulatorTest(SimulatorTest):
    def setUp(self) -> None:
        self.model = RulesModel()


class SimpleModelSimulatorTest(SimulatorTest):
    def setUp(self) -> None:
        self.model = SimpleModel()


class PatternCurveModelSimulatorTest(SimulatorTest):
    def setUp(self) -> None:
        self.model = PatternCurveModel()

    def test_run(self):
        self.model.network.run()


if __name__ == '__main__':
    unittest.main()
