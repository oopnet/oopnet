import os
from multiprocessing import Pool

import numpy as np
import pandas as pd
import oopnet as on
from matplotlib import pyplot as plt


def roll_the_dice(network: on.Network) -> pd.Series:
    cnet = on.Copy(network)
    for j in on.get_junctions(cnet):
        j.demand += np.random.normal(0.0, 1.0)
    rpt = cnet.run()
    return rpt.pressure


if __name__ == '__main__':
    filename = os.path.join('data', 'Poulakis.inp')

    net = on.Network.read(filename)
    mcruns = 1_000
    networks = [net] * mcruns

    p = Pool().map(roll_the_dice, networks)

    p = pd.DataFrame(p, index=list(range(len(p))))
    print(p)

    p_mean = p.mean()
    print(p_mean)

    p_sub = p.sub(p_mean, axis=1)

    x = np.linspace(-1.5, 1.5, 40)
    p_sub[['J-03', 'J-31']].hist(bins=x, layout=(2, 1))
    plt.show()
