import datetime
import os
from sys import platform as _platform
import subprocess
import uuid
import shutil
import re
from typing import Union, Optional

from oopnet.elements import Network
from oopnet.utils import utils
from oopnet.report.xrayreport import Report
from oopnet.writer import Write


def run(thing: Union[Network, str], filename: Optional[str] = None, delete: bool = True,
        path: Optional[str] = None, startdatetime: Optional[datetime.datetime] = None, output: bool = False):
    """Runs an EPANET simulation by calling command line EPANET

    Args:
      thing: either an OOPNET network object or the filename of an EPANET input file
      filename: if thing is an OOPNET network, filename is an option to perform command line EPANET simulations with a specific filename. If filename is a Python None object then a file with a random UUID (universally unique identifier) is generated
      delete: if delete is True the Epanet Input and Report file is deleted, if False then the simulation results won't be deleted and are stored in a folder named path
      path: Path were  to perform the simulations. If path is a Python None object then a tmp-folder is generated

    Returns:
      OOPNET report object

    """
    simulator = ModelSimulator(thing=thing, filename=filename, delete=delete, path=path, startdatetime=startdatetime,
                               output=output)
    return simulator.run()


# todo: add proper documentation
class ModelSimulator:
    """Runs an EPANET simulation by calling command line EPANET

    Attributes:
      thing: either an OOPNET network object or the filename of an EPANET input file
      filename: if thing is an OOPNET network, filename is an option to perform command line EPANET simulations with a specific filename. If filename is a Python None object then a file with a random UUID (universally unique identifier) is generated
      delete: if delete is True the EPANET Input and Report file is deleted, if False then the simulation results won't be deleted and are stored in a folder named path
      path: Path were to perform the simulations. If path is a Python None object then a tmp-folder is generated

    Returns:
      OOPNET report object

    """
    def __init__(self, thing: Union[Network, str], filename: Optional[str] = None, delete: bool = True,
                 path: Optional[str] = None, startdatetime: Optional[datetime.datetime] = None, output: bool = False):
        self.thing = thing
        self.filename = filename
        self.delete = delete
        self.path = path
        self.startdatetime = startdatetime
        self.output = output
        self.command = None

    def _set_path(self):
        """Sets path for temporary file placement."""
        # Set Path and generate it, if it does not exist
        if self.path is None:
            self.path = 'tmp'
            utils.mkdir(self.path)
        elif isinstance(self.path, str):
            if not os.path.isdir(self.path):
                utils.mkdir(self.path)
        else:
            raise TypeError(f'Path must either be None or of type string but a value of type {type(self.path)} was'
                            f'submitted')

    def _set_filename(self):
        """Sets filename for temporary file placement."""
        if isinstance(self.thing, str):
            self.filename = os.path.join(self.path, os.path.split(self.thing)[-1])
            shutil.copy(self.thing, self.filename)
        elif isinstance(self.thing, Network):
            self.filename = os.path.join(self.path, str(uuid.uuid4())+'.inp')  # generate filename with unique filename
            
    def _setup_report(self):
        """Sets up report."""
        if isinstance(self.thing, Network) and \
                (self.thing.report.nodes == 'NONE') and (self.thing.report.links == 'NONE'):
            self.thing.report.nodes = 'ALL'
            self.thing.report.links = 'ALL'

    def _create_command(self):
        """Creates command for simulating model."""
        cmd = []
        if _platform in ["linux", "linux2", "darwin"]:
            # Linux, macOS
            cmd.append('epanet2')
        elif _platform == "win32":
            # Windows...
            script_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep
            exe = os.path.join(script_dir, 'runepanet.exe')
            cmd.append(exe)
        else:
            raise Exception('Operating system unknown.')
        cmd.append(self.filename)
        cmd.append(self.filename.replace('.inp', '.rpt'))
        self.command = cmd

    def _execute(self):
        """Executes simulation and parses output."""
        def decorate_string(stdout_bytes: bytes) -> str:
            """

            Args:
              stdout_bytes: bytes: 

            Returns:

            """
            out = stdout_bytes.decode('utf-8')
            for char in ['\n', '\r', '...']:
                out = out.replace(char, '')
            pattern = re.compile(r'(\s){2,}')
            out = re.sub(pattern, '. ', out).strip()
            return out

        if isinstance(self.thing, Network):
            Write(self.thing, filename=self.filename)

        cmd = subprocess.run(self.command, capture_output=True, shell=False)
        out, err = cmd.stdout, cmd.stderr
        if out and self.output:
            print(decorate_string(out))
        if err and self.output:
            print(decorate_string(err))

    def run(self):
        """Simulates a hydraulic model using EPANET."""
        self._set_path()
        self._set_filename()
        self._setup_report()
        self._create_command()
        self._execute()

        rpt = Report(self.filename.replace('.inp', '.rpt'), startdatetime=self.startdatetime)

        if self.delete:
            os.remove(self.filename)
            os.remove(self.filename.replace('.inp', '.rpt'))

        return rpt
