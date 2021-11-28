import os

from oopnet.api import *

# todo: fix

filename = os.path.join('data', 'C-town.inp')
net = Read(filename)

net.times.duration = timedelta(hours=6)
net.times.reporttimestep = timedelta(minutes=5)

rpt = Run(net)

print(rpt)

print(Pressure(rpt))

fig = plt.figure(1)

ax1 = fig.add_subplot(211)
Flow(rpt)['P1000'].plot(ax=ax1)

plt.xlabel('time', fontsize=16)
plt.ylabel('Q (l/s)', fontsize=16)
plt.legend()

ax2 = fig.add_subplot(212)
Pressure(rpt)[['J10', 'J1058']].plot(ax=ax2)

plt.xlabel('time', fontsize=16)
plt.ylabel('p (m)', fontsize=16)
Show()
