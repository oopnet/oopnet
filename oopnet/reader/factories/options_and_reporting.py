from typing import Union

from oopnet.elements import Network, Pattern
from oopnet.elements.options_and_reporting import Options, Report
from oopnet.reader.factories.base import ReadFactory
from oopnet.utils.getters import get_pattern


class OptionsReportFactory(ReadFactory):
    @staticmethod
    def _flatten_block(values: dict):
        return [x['values'] for x in values]

    @staticmethod
    def _set_attributes(obj: Union[Options, Report], attr_mapping: dict[str, tuple[str, ...]], values: list[str], network: Network) -> Union[Options, Report]:
        attr, attr_cls = attr_mapping[values[0]]
        val = values[1]
        if attr_cls == Pattern:
            val = get_pattern(network, val)
        # elif attr_name
        # setattr(obj, )


class OptionsFactory(OptionsReportFactory):
    def __new__(cls, values: dict, options: Options, network: Network):
        mapping = {'UNITS': ('units', str),
                   'HEADLOSS': ('headloss', str),
                   'HYDRAULICS': ('hydraulics', str),
                   'QUALITY': ('quality', str),
                   'VISCOSITY': ('viscosity', float),
                   'DIFFUSIVITY': ('diffusivity', float),
                   'SPECIFIC GRAVITY': ('specificgravity', float),
                   'TRIALS': ('trials', int),
                   'ACCURACY': ('accuracy', float),
                   'UNBALANCED': ('unbalanced', str),
                   'PATTERN': ('pattern', Pattern),
                   'DEMAND MULTIPLIER': ('demandmultiplier', float),
                   'EMITTER EXPONENT': ('exponent', float),
                   'TOLERANCE': ('tolerance', float),
                   'MAP': ('map', str),
                   'DEMAND MODEL': ('demandmodel', str),
                   'MINIMUM PRESSURE': ('minimumpressure', float),
                   'REQUIRED PRESSURE': ('requiredpressure', float),
                   'PRESSURE EXPONENT': ('pressureexponent', float)}
