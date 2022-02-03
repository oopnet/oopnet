import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'Poulakis.inp')

net = on.Network.read(filename)
net.reportprecision.flow = 3
net.reportprecision.pressure = 3
mcruns = 1000
p = []

for _ in range(mcruns):
    cnet = on.Copy(net)
    for j in on.get_junctions(cnet):
        j.demand += np.random.normal(0.0, 1.0)
    rpt = net.run()
    p.append(rpt.pressure)

p = pd.DataFrame(p, index=list(range(len(p))))
print(p)

pmean = p.mean()
print(pmean)

psub = p.sub(pmean, axis=1)

x = np.linspace(-1.5, 1.5, 40)
psub[['J-03', 'J-31']].hist(bins=x, layout=(2, 1))
plt.show()
