import sys
import os
import pylab
from pylab import sqrt
from matplotlib import cm
from atpy import Table
import numpy as np 

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin:/opt/local/bin'

# mcor_gal : massa em estrelas
# at_flux: idade ponderada em fluxo
# at_mass: idade em massa
# am_flux: metalicidade em fluxo
# am_mass: metalicidade em massa
# AV: extincao
vmin = {}
vmax = {}
label = {}

vmin['mcor_gal'] = 10.25
vmax['mcor_gal'] = 11.75
label['mcor_gal'] = '$\log(M_{\star}/[M_{\odot}])$'

vmin['at_flux'] = 7.25
vmax['at_flux'] = 10.25
label['at_flux'] = '$\log(\mathrm{Idade}/\mathrm{[Anos]})$'

vmin['at_mass'] = 9.2
vmax['at_mass'] = 10.2
label['at_mass'] = '$\log(\mathrm{Idade}/\mathrm{[Anos]})$'

vmin['am_flux'] = 0.25
vmax['am_flux'] = 2.25
label['am_flux'] = 'Metalicidade'

vmin['am_mass'] = 0.25
vmax['am_mass'] = 2.25
label['am_mass'] = 'Metalicidade'

vmin['AV'] = -0.25
vmax['AV'] = 1.25
label['AV'] = 'Extin\c{c}\~ao'


tablename = sys.argv[1]
t = Table(tablename)

#np.power(10, t.data['at_mass'], t.data['at_mass'])
#np.power(10, t.data['at_flux'], t.data['at_flux'])

sample = (t.data['z'] < -21.5) & (t.data['z'] > -23.0)
NUV_r = t.data['NUV'][sample] - t.data['r'][sample]
g_r = t.data['g'][sample] - t.data['r'][sample]

bounds = [.5,7,.2,.9]
h, ex, ey = np.histogram2d(NUV_r, g_r, bins=20,
                           range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])

#for col in label.keys():
#    pylab.figure()
#    pylab.hist(t.data[col][sample], range=(vmin[col], vmax[col]))
#    pylab.title(col)
#    pylab.show()
#exit()

# From http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
fig_width_pt = 448.07378
inches_per_pt = 1.0 / 72.27
golden_mean = (sqrt(5) - 1.0) / 2.0
fig_width = fig_width_pt * inches_per_pt
fig_height = fig_width * golden_mean
fig_size = (fig_width, fig_height)
params = {'backend': 'ps',
          'axes.labelsize': 10,
          'text.fontsize': 10,
          'legend.fontsize': 10,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True,
          'font.family': 'serif',
          'figure.figsize': fig_size}
pylab.rcParams.update(params)

pylab.figure()
pylab.axis(bounds)
#pylab.title('Densidade')
pylab.xlabel('NUV - r')
pylab.ylabel('g - r')
pylab.hexbin(NUV_r, g_r, extent=bounds, bins='log', gridsize=50, cmap=cm.Greys)
cb = pylab.colorbar()
cb.set_label('$\log{N}$')
pylab.savefig('../doc/figuras/uvcolor-color-density.eps', format='eps')

for col in vmin.keys():
    z = t.data[col][sample]
    pylab.figure()
    pylab.axis(bounds)
    #pylab.title(col)
    pylab.xlabel('NUV - r')
    pylab.ylabel('g - r')
#    pylab.scatter(NUV_r, g_r, c=z,
#        marker='o', edgecolor='None', s=1, cmap=cm.spectral,
#        vmin=vmin[col], vmax=vmax[col])
    pylab.hexbin(NUV_r, g_r, z, extent=bounds,
               gridsize=50, vmin=vmin[col], vmax=vmax[col], cmap=cm.jet)
    cb = pylab.colorbar()
    cb.set_label(label[col])
    pylab.contour(h.T, extent=bounds, colors='black')
    #pylab.show()
    pylab.savefig('../doc/figuras/uvcolor-color-' + col + '.eps', format='eps')
