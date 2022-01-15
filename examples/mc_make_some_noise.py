import os

from oopnet import *

filename = os.path.join('data', 'Poulakis.inp')

net = Read(filename)
net.reportprecision.flow = 3
net.reportprecision.pressure = 3
mcruns = 1000
p = []

for _ in range(mcruns):
    cnet = Copy(net)
    for j in get_junctions(cnet):
        j.demand += np.random.normal(0.0, 1.0)
    rpt = Run(cnet)
    p.append(Pressure(rpt))

p = pd.DataFrame(p, index=list(range(len(p))))
print(p)

pmean = p.mean()
print(pmean)

psub = p.sub(pmean, axis=1)

x = np.linspace(-1.5, 1.5, 40)
psub[['J-03', 'J-31']].hist(bins=x, layout=(2, 1))
plt.show()
