import logging

import numpy as np

logger = logging.getLogger(__name__)


class BinaryFileReader:
    def __new__(cls, filename: str, *args, **kwargs):
        with open(filename, 'rb') as file:
            prolog = np.fromfile(file, dtype=np.int32, count=15)
            cls._read_prolog(prolog)

    @classmethod
    def _read_prolog(cls, prolog):
        print(prolog)
        magic = prolog[0]
        version = prolog[1]
        nnodes = prolog[2]
        ntanks = prolog[3]
        nlinks = prolog[4]
        npumps = prolog[5]
        nvalve = prolog[6]
        # wqopt = QualType(prolog[7])
        # srctrace = prolog[8]
        # flowunits = FlowUnits(prolog[9])
        # presunits = PressureUnits(prolog[10])
        # statsflag = StatisticsType(prolog[11])
        # reportstart = prolog[12]
        # reportstep = prolog[13]
        # duration = prolog[14]
