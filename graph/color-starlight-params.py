import sys
import os
import pylab
from pylab import sqrt
from matplotlib import cm
from matplotlib import gridspec
from atpy import Table
import numpy as np 

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin:/opt/local/bin'

debug = False
outformat = 'eps'


def set_eps_output_1():
    # From http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
    fig_width_pt = 448.07378
    inches_per_pt = 1.0 / 72.27
    golden_mean = (sqrt(5) - 1.0) / 2.0
    fig_width = fig_width_pt * inches_per_pt
    fig_height = fig_width * golden_mean * 0.85
    fig_size = (fig_width, fig_height)
    params = {'backend': 'ps',
              'axes.labelsize': 10,
              'text.fontsize': 10,
              'legend.fontsize': 10,
              'xtick.labelsize': 10,
              'ytick.labelsize': 10,
              'text.usetex': True,
              'font.family': 'serif',
              'figure.subplot.bottom': 0.12,
              'figure.figsize': fig_size}
    pylab.rcParams.update(params)

def set_eps_output_3x2():
    # From http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
    fig_width_pt = 448.07378
    inches_per_pt = 1.0 / 72.27
    golden_mean = (sqrt(5) - 1.0) / 2.0
    fig_width = fig_width_pt * inches_per_pt
    fig_height = fig_width * golden_mean * 1.5
    fig_size = (fig_width, fig_height)
    params = {'backend': 'ps',
              'axes.labelsize': 8,
              'text.fontsize': 8,
              'legend.fontsize': 8,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              'text.usetex': True,
              'font.family': 'serif',
              'figure.subplot.hspace': .2,
              'figure.subplot.wspace': .2,
              'figure.figsize': fig_size}
    pylab.rcParams.update(params)

def randomFraction(arr, f):
    return (np.random.rand(len(arr)) < f)


tablename = sys.argv[1]
t = Table(tablename)

sample = (t.data['z'] < -21.5)
sample &= (t.data['z'] > -23.0)
sample &= (t.data['redshift'] > 0.04) 
sample &= (t.data['redshift'] < 0.17) 

NUV_r = t.data['NUV'][sample] - t.data['r'][sample]
g_r = t.data['g'][sample] - t.data['r'][sample]

bounds = [.5,7,.2,.9]
h, ex, ey = np.histogram2d(NUV_r, g_r, bins=20,
                           range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])

set_eps_output_1()
pylab.figure()
pylab.axis(bounds)
#pylab.title('Densidade')
pylab.xlabel('$NUV - r$')
pylab.ylabel('$g - r$')
pylab.hexbin(NUV_r, g_r, extent=bounds, bins='log', gridsize=50, cmap=cm.Greys)
cb = pylab.colorbar()
cb.set_label('$\\log{N}$')
if debug:
    pylab.show()
    #exit()
else:
    pylab.savefig('../doc/figuras/uvcolor-color-density.' + outformat, format=outformat)

# mcor_gal : massa em estrelas
# at_flux: idade ponderada em fluxo
# at_mass: idade em massa
# am_flux: metalicidade em fluxo
# am_mass: metalicidade em massa
# AV: extincao
vmin = {}
vmax = {}
label = {}
position = {}

vmin['at_flux'] = 7.25
vmax['at_flux'] = 10.25
label['at_flux'] = '{\\bf (a)} $\\log(\\mathrm{Idade}_{F}/\\mathrm{[a]})$'
position['at_flux'] = 321

vmin['at_mass'] = 9.2
vmax['at_mass'] = 10.2
label['at_mass'] = '{\\bf (b)} $\\log(\mathrm{Idade}_{M}/\\mathrm{[a]})$'
position['at_mass'] = 322

vmin['am_flux'] = 0.25
vmax['am_flux'] = 2.25
label['am_flux'] = '{\\bf (c)} $Z_{F}/Z_{\\odot}$'
position['am_flux'] = 323

vmin['am_mass'] = 0.25
vmax['am_mass'] = 2.25
label['am_mass'] = '{\\bf (d)} $Z_{M}/Z_{\\odot}$'
position['am_mass'] = 324

vmin['mcor_gal'] = 10.25
vmax['mcor_gal'] = 11.75
label['mcor_gal'] = '{\\bf (e)} $\log(M_{\star}/[M_{\odot}])$'
position['mcor_gal'] = 325

vmin['AV'] = -0.25
vmax['AV'] = 1.25
label['AV'] = '{\\bf (f)} $A_V$'
position['AV'] = 326

#if debug:
#    for col in label.keys():
#        pylab.figure()
#        #pylab.hist(t.data[col][sample], range=(vmin[col], vmax[col]))
#        pylab.hist(t.data[col][sample])
#        pylab.title(col)
#        pylab.show()
#    #exit()
set_eps_output_3x2()
pylab.figure()

# Plot less points
fraction = randomFraction(NUV_r, 0.1)

for col in vmin.keys():
    z = t.data[col][sample]
    ax = pylab.subplot(position[col])
    pylab.axis(bounds)
    pylab.text(3.0, .25, label[col], fontsize=8)
    pylab.scatter(NUV_r[fraction], g_r[fraction], c=z[fraction],
        marker='o', edgecolor='None', s=1, cmap=cm.spectral,
        vmin=vmin[col], vmax=vmax[col])
#    pylab.hexbin(NUV_r[fraction], g_r[fraction], z[fraction], extent=bounds,
#               gridsize=50, vmin=vmin[col], vmax=vmax[col], cmap=cm.spectral)
    pylab.colorbar()
    pylab.contour(h.T, extent=bounds, colors='black')

if debug:
    pylab.show()
else:    
    pylab.savefig('../doc/figuras/uvcolor-color.' + outformat, format=outformat)