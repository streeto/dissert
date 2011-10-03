import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from atpy import Table

# mcor_gal : massa em estrelas
# at_flux: idade ponderada em fluxo
# at_mass: idade em massa
# am_flux: metalicidade em fluxo
# am_mass: metalicidade em massa
# AV: extincao
tablename = sys.argv[1]
t = Table(tablename)
sample = (t.data['z'] < -21.5) & (t.data['z'] > -23.0)

vmin = {}
vmax = {}
vmin['mcor_gal'] = 10.0
vmax['mcor_gal'] = 12.5

vmin['at_flux'] = 7.0
vmax['at_flux'] = 10.5

vmin['at_mass'] = 8.5
vmax['at_mass'] = 10.5

vmin['am_flux'] = 0.0
vmax['am_flux'] = 2.5

vmin['am_mass'] = 0.0
vmax['am_mass'] = 2.5

vmin['AV'] = -1.0
vmax['AV'] = 2.0

for col in vmin.keys():
    NUV_r = t.data['NUV'][sample] - t.data['r'][sample]
    g_r = t.data['g'][sample] - t.data['r'][sample]
    z = t.data[col][sample]
    f = plt.figure()
    plt.axis([0.5, 7, 0.2, 0.9])
    plt.title(col)
    plt.xlabel('NUV - r')
    plt.ylabel('g - r')
    plt.scatter(NUV_r, g_r, c=z,
        marker='o', edgecolor='None', s=1, cmap=cm.spectral,
        vmin=vmin[col], vmax=vmax[col])
    plt.colorbar()
    plt.savefig('fig/uvcolor-color-' + col + '.png', format='png')

