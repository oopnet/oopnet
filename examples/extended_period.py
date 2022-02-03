import os
from datetime import timedelta

from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'C-town.inp')
net = on.Network.read(filename)

net.times.duration = timedelta(hours=6)
net.times.reporttimestep = timedelta(minutes=5)

rpt = net.run()

print(rpt)

print(rpt.pressure)

fig = plt.figure(1)

ax1 = fig.add_subplot(211)
rpt.flow['P1000'].plot(ax=ax1)

plt.xlabel('time', fontsize=16)
plt.ylabel('Q (l/s)', fontsize=16)
plt.legend()

ax2 = fig.add_subplot(212)
rpt.pressure[['J10', 'J1058']].plot(ax=ax2)

plt.xlabel('time', fontsize=16)
plt.ylabel('p (m)', fontsize=16)
plt.show()
