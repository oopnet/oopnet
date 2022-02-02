"""
Convert all units which are possible in the EPANET-Input file to LPS
Possible: (This are the flow units)
    CFS ... cubic feet per second
    GPM ... gallons per minute
    MGD ... million gallons per day
    IMGD ... Imperial MGD
    AFD ... acre-feet per day
    LPS ... liters per second
    LPM ... liters per minute
    MLD ... million liters per day
    CMH ... cubic meters per hour
    CMD ... cubic meters per day

The Input of OOPNET is possible in all units, but OOPNET uses and returns SI-Units (LPS).
"""
import logging

import numpy as np

from oopnet.utils.getters.element_lists import get_junctions, get_tanks, get_reservoirs, get_pipes

logger = logging.getLogger(__name__)

FEET2METER = 0.3048
INCH2MILLIMETER = 25.4
HORESEPOWER2KILOWATTS = 0.7457
PSI2METER = 0.703249614902
CFS2LPS = 28.3168
GPM2LPS = 0.063092
MGD2LPS = 43.8126364
IMGD2LPS = 52.6168042
AFD2LPS = 14.2764
LPM2LPS = 1.0 / 60.0
MLD2LPS = 11.5741
CMH2LPS = 0.27778
CMD2LPS = 0.0115741


class Converter:
    """ """

    f_demand: float = 1.0
    f_diameter_pipes: float = 1.0
    f_diameter_tanks: float = 1.0
    f_elevation: float = 1.0
    f_emitter_coefficient: float = 1.0
    f_flow: float = 1.0
    f_hydraulic_head: float = 1.0
    f_length: float = 1.0
    f_power: float = 1.0
    f_pressure: float = 1.0
    f_reaction_coeff_wall: float = 1.0
    f_roughness_coeff: float = 1.0
    f_velocity: float = 1.0
    f_volume: float = 1.0

    def __init__(self, network):
        if network.options.units == 'LPS':
            logger.debug('Already using LPS as unit. Skipping conversion.')
            return

        logger.debug(f'Converting units from {network.options.units} to LPS')

        us_units = ['CFS',
                    'GPM',
                    'MGD',
                    'IMGD',
                    'AFD']

        if network.options.units in us_units:

            self.f_diameter_pipes = INCH2MILLIMETER
            self.f_diameter_tanks = FEET2METER
            self.f_elevation = FEET2METER
            self.f_hydraulic_head = FEET2METER
            self.f_length = FEET2METER
            self.f_power = HORESEPOWER2KILOWATTS
            self.f_pressure = PSI2METER
            self.f_reaction_coeff_wall = FEET2METER
            if network.options.headloss == 'D-W':
                self.f_roughness_coeff = 1.0e3 * FEET2METER
            self.f_velocity = FEET2METER
            self.f_volume = FEET2METER ** 3

        if network.options.units == 'CFS':
            self.f_flow = CFS2LPS
        elif network.options.units == 'GPM':
            self.f_flow = GPM2LPS
        elif network.options.units == 'MGD':
            self.f_flow = MGD2LPS
        elif network.options.units == 'IMGD':
            self.f_flow = IMGD2LPS
        elif network.options.units == 'AFD':
            self.f_flow = AFD2LPS
        elif network.options.units == 'LPM':
            self.f_flow = LPM2LPS
        elif network.options.units == 'MLD':
            self.f_flow = MLD2LPS
        elif network.options.units == 'CMH':
            self.f_flow = CMH2LPS
        elif network.options.units == 'CMD':
            self.f_flow = CMD2LPS
        else:
            raise ValueError(f'Illegal unit {network.options.units} defined.')

        self.f_demand = self.f_flow
        si_units = ['LPS',
                    'LPM',
                    'MLD',
                    'CMH',
                    'CMD']

        if network.options.units in us_units:
            self.f_emitter_coefficient = self.f_flow * 1.0 / np.sqrt(PSI2METER)
        elif network.options.units in si_units:
            self.f_emitter_coefficient = self.f_flow


def convert(network):
    """

    Args:
      network: 

    Returns:

    """

    if network.options.units == 'LPS':
        return

    converter = Converter(network)

    for j in get_junctions(network):
        if j.emittercoefficient:
            j.emittercoefficient *= converter.f_emitter_coefficient
        if j.demand:
            if isinstance(j.demand, list):
                j.demand = [x * converter.f_demand for x in j.demand]
            else:
                j.demand *= converter.f_demand
        if j.elevation:
            j.elevation *= converter.f_elevation

    for t in get_tanks(network):
        t.diam *= converter.f_diameter_tanks
        t.elevation *= converter.f_elevation
        t.initlevel *= converter.f_elevation
        t.minlevel *= converter.f_elevation
        t.maxlevel *= converter.f_elevation
        t.minvolume *= converter.f_volume

    for r in get_reservoirs(network):
        r.elevation *= converter.f_elevation
        r.head *= converter.f_hydraulic_head

    for p in get_pipes(network):
        p.diameter *= converter.f_diameter_pipes
        p.length *= converter.f_length
        p.roughness *= converter.f_roughness_coeff

    network.options.units = 'LPS'
