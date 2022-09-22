import os
from datetime import timedelta

import pandas as pd
from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'C-town.inp')
net = on.Network.read(filename)

net.times.duration = timedelta(hours=6)
net.times.reporttimestep = net.times.hydraulictimestep = net.times.patterntimestep = timedelta(minutes=5)

# Run EPANET
rpt = net.run(simulator='EPANET')
consumptions_at_J156_from_epanet, consumptions_at_J494_from_epanet = rpt.consumption['J156'], rpt.consumption['J494']
consumptions_at_J156_from_epanet.rename('EPANET', inplace=True)
consumptions_at_J494_from_epanet.rename('EPANET', inplace=True)
startdatetime = consumptions_at_J156_from_epanet.first_valid_index()

# Run PYTHON_PDM
rpt = net.run(startdatetime=startdatetime, simulator='PYTHON_PDM')
consumptions_at_J156_from_python, consumptions_at_J494_from_python = rpt.consumption['J156'], rpt.consumption['J494']
consumptions_at_J156_from_python.rename('PYTHON_PDM', inplace=True)
consumptions_at_J494_from_python.rename('PYTHON_PDM', inplace=True)

# Plot the results
fig = plt.figure(1)

for pos, nid, c_to_plot in \
        ((211, 'J156', (consumptions_at_J156_from_epanet, consumptions_at_J156_from_python)),
         (212, 'J494', (consumptions_at_J494_from_epanet, consumptions_at_J494_from_python))):

    ax = fig.add_subplot(pos)
    c_to_plot = pd.concat(c_to_plot, axis=1)
    c_to_plot.plot(ax=ax)
    plt.xlabel('time', fontsize=16)
    plt.ylabel('c at {} (l/s)'.format(nid), fontsize=16)
    plt.legend()

plt.tight_layout()
plt.show()
