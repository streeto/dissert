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

np.power(10, t.data['at_mass'], t.data['at_mass'])
#np.power(10, t.data['at_flux'], t.data['at_flux'])

sample = (t.data['z'] < -21.5) & (t.data['z'] > -23.0)
NUV_r = t.data['NUV'][sample] - t.data['r'][sample]
g_r = t.data['g'][sample] - t.data['r'][sample]

bounds = [.5,7,.2,.9]
h, ex, ey = np.histogram2d(NUV_r, g_r, bins=20,
                           range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])
plt.figure()
plt.axis(bounds)
plt.title('Densidade')
plt.xlabel('NUV - r')
plt.ylabel('g - r')
plt.hexbin(NUV_r, g_r, extent=bounds, bins='log', gridsize=50, cmap=cm.Greys)
cb = plt.colorbar()
cb.set_label('log10(N)')
plt.savefig('fig/uvcolor-color-density.png', format='png')

vmin = {}
vmax = {}
vmin['mcor_gal'] = 8.0
vmax['mcor_gal'] = 12.5

vmin['at_flux'] = 6.5
vmax['at_flux'] = 10.5

vmin['at_mass'] = 0.0
vmax['at_mass'] = 1.75e10

vmin['am_flux'] = 0.0
vmax['am_flux'] = 2.5

vmin['am_mass'] = 0.0
vmax['am_mass'] = 2.5

vmin['AV'] = -0.25
vmax['AV'] = 1.25

for col in vmin.keys():
    z = t.data[col][sample]
    plt.figure()
    plt.axis(bounds)
    plt.title(col)
    plt.xlabel('NUV - r')
    plt.ylabel('g - r')
#    plt.scatter(NUV_r, g_r, c=z,
#        marker='o', edgecolor='None', s=1, cmap=cm.spectral,
#        vmin=vmin[col], vmax=vmax[col])
    plt.hexbin(NUV_r, g_r, z, extent=bounds,
               gridsize=50, vmin=vmin[col], vmax=vmax[col], cmap=cm.jet)
    plt.colorbar()
    plt.contour(h.T, extent=bounds, colors='black')
    #plt.show()
    plt.savefig('fig/uvcolor-color-' + col + '.png', format='png')
