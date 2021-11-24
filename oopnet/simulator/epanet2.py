import os
import subprocess
import uuid
import shutil
from traits.api import HasStrictTraits
from .. import elements
from ..utils import utils
from ..report.xrayreport import Report
from ..writer.decorator_writer.write import write
from sys import platform as _platform
import re


def decorate_string(stdout_bytes):
    out = stdout_bytes.decode('utf-8')
    for char in ['\n', '\r', '...']:
        out = out.replace(char, '')
    pattern = re.compile(r'(\s){2,}')
    out = re.sub(pattern, '. ', out).strip()
    return out


def make_command(filename):
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
        print('unknown operating system!')
    cmd.append(filename + '.inp')
    cmd.append(filename + '.rpt')
    print(cmd)
    return cmd


class Run(HasStrictTraits):
    """
    Runs an EPANET simulation by calling command line EPANET

    :param thing: either an OOPNET network object or the filename of an EPANET input file
    :param filename: if thing is an OOPNET network, filename is an option to perform command line EPANET simulations with a specific filename. If filename is a Python None object then a file with a random UUID (universally unique identifier) is generated
    :param delete: if delete is True the Epanet Input and Report file is deleted, if False then the simulation results won't be deleted and are stored in a folder named path
    :param path: Path were  to perform the simulations. If path is a Python None object then a tmp-folder is generated
    :return: OOPNET report object
    """
    def __new__(self, thing, filename=None, delete=True, path=None, startdatetime=None, output=False):

        cmd_str = ''

        # Set Path and generate it, if it does not exist

        if path is None:
            path = 'tmp'
            utils.mkdir(path)
        elif isinstance(path, str):
            if not os.path.isdir(path):
                utils.mkdir(path)
        else:
            print('simulator/simulate/Epanet2: path format is not a String')

        # Filename conversion

        if filename is None:
            pass
        elif isinstance(filename, str):
            if '.inp' in filename:
                filename = filename.replace('.inp', '')
            filename = os.path.join(path, os.path.split(filename)[-1])
        else:
            print('simulator/simulate/Epanet2: filename format is not a String')

        # Print Input File if not existing

        if isinstance(thing, elements.network.Network):
            if (thing.report.nodes == 'NONE') and (thing.report.links == 'NONE'):
                thing.report.nodes = 'ALL'
                thing.report.links = 'ALL'

            if filename is None:
                filename = os.path.join(path, str(uuid.uuid4()))  # generate filename with unique filename

            write(thing, filename=filename + '.inp')
            cmd_str = make_command(filename)

        elif isinstance(thing, str):
            if thing.endswith('.inp'):
                if filename is None:
                    filename = os.path.join(path, os.path.split(thing)[-1].replace('.inp', ''))
                shutil.copy(thing, filename + '.inp')
                cmd_str = make_command(filename)

        elif isinstance(thing, file):
            # ToDo: Implement Running Simulation when getting a file-object
            pass

        else:
            print('simulator/simulate/Epanet2: unknown type to simulate')

        # called command line epanet
        cmd = subprocess.run(cmd_str, capture_output=True, shell=False)
        out, err = cmd.stdout, cmd.stderr

        if out and output:
            print(decorate_string(out))
        if err and output:
            print(decorate_string(err))

        report = Report(filename + '.rpt', startdatetime=startdatetime)

        if delete:
            os.remove(filename + '.inp')
            os.remove(filename + '.rpt')
            # os.removedirs(path)

        return report
