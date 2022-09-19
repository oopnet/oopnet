import os
from datetime import timedelta
import oopnet as on

filename = os.path.join('data', 'Poulakis.inp')
network = on.Network.read(filename)

report = network.run()
print(report.nodes)
print(report.links)

p = report.pressure
print(p)
print(p.describe())

eps_model_path = os.path.join('data', 'MICROPOLIS_v1.inp')
eps_network = on.Network.read(eps_model_path)
print(eps_network.times.duration)
print(eps_network.times.reporttimestep)

eps_network.times.duration = timedelta(days=1)
eps_network.times.reporttimestep = timedelta(minutes=10)

eps_report = eps_network.run()
print(eps_report.nodes)
print(eps_report.links)

eps_p = eps_report.pressure
print(eps_p)
