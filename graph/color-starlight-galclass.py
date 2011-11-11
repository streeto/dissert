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


logN2Ha = np.log10(t.data['nii_6584_flux'][sample] / t.data['halpha_flux'][sample])
WHa = t.data['halpha_ew'][sample]
WN2 = t.data['nii_6584_ew'][sample]

typemask = {
            'all': np.zeros(len(NUV_r)) == 0,
            'starforming': (logN2Ha < -0.4) & (WHa > 3.0),
            'sAGN': (logN2Ha > -0.4) & (WHa > 6.0),
            'wAGN': (logN2Ha > -0.4) & (WHa < 6.0) & (WHa > 3.0),
            'retired': (WHa < 3.0) & (WHa > 0.5) & (WN2 > 0.5),
            'passive': (WHa < 0.5) & (WN2 < 0.5)
            }

position = {
            'all': 321,
            'starforming': 322,
            'sAGN': 323,
            'wAGN': 324,
            'retired': 325,
            'passive': 326
}

color = {
         'all': None,
         'starforming': 'blue',
         'sAGN': 'lightgreen',
         'wAGN': 'darkgreen',
         'retired': 'black',
         'passive': 'red'
         }

label = {
         'all': '{\\bf (a)} Todos',
         'starforming': '{\\bf (b)} SFG',
         'sAGN': '{\\bf (c)} sAGN',
         'wAGN': '{\\bf (d)} wAGN',
         'retired': '{\\bf (e)} RG',
         'passive': '{\\bf (f)} PG'
         }

label2 = {
         'all': 'Todos',
         'starforming': 'SFG',
         'sAGN': 'sAGN',
         'wAGN': 'wAGN',
         'retired': 'RG',
         'passive': 'PG'
         }


bounds = [.5,7,.2,.9]

# Color - UV color for all the galaxy classes.
set_eps_output_1()
pylab.figure()
for type, mask in typemask.items():
    if type == 'all': continue
    # Plot less points
    fraction = randomFraction(NUV_r[mask], 0.1)
    pylab.axis(bounds)
    pylab.xlabel('$NUV - r$')
    pylab.ylabel('$g - r$')
    pylab.plot(NUV_r[mask][fraction], g_r[mask][fraction], '.', label=label2[type],
               color=color[type], markersize=0.5, zorder=1)
    
pylab.legend(loc='lower right', markerscale=20, numpoints=1)

if debug:
    pylab.show()
else:    
    pylab.savefig('../doc/figuras/uvcolor-color-class.' + outformat, format=outformat)


# mcor_gal : massa em estrelas
# at_flux: idade ponderada em fluxo
# at_mass: idade em massa
# am_flux: metalicidade em fluxo
# am_mass: metalicidade em massa
# AV: extincao
vmin = {}
vmax = {}
param = {}

vmin['at_flux'] = 7.25
vmax['at_flux'] = 10.25
param['at_flux'] = '(a) $\log(\mathrm{Idade}_{F})/\mathrm{[a]})$'

vmin['at_mass'] = 9.2
vmax['at_mass'] = 10.2
param['at_mass'] = '(b) $\log(\mathrm{Idade}_{M})/\mathrm{[a]})$'

vmin['am_flux'] = 0.25
vmax['am_flux'] = 2.25
param['am_flux'] = '(c) $Z_{F}$'

vmin['am_mass'] = 0.25
vmax['am_mass'] = 2.25
param['am_mass'] = '(d) $Z_{M}$'

vmin['mcor_gal'] = 10.25
vmax['mcor_gal'] = 11.75
param['mcor_gal'] = '(e) $\log(M_{\star}/[M_{\odot}])$'

vmin['AV'] = -0.25
vmax['AV'] = 1.25
param['AV'] = '(f) $AV$'


#if debug:
#    for col in label.keys():
#        pylab.figure()
#        #pylab.hist(t.data[col][sample], range=(vmin[col], vmax[col]))
#        pylab.hist(t.data[col][sample])
#        pylab.title(col)
#        pylab.show()
#    #exit()

set_eps_output_3x2()

for p in param.keys():
    pylab.figure()
    for type, mask in typemask.items():
        h, ex, ey = np.histogram2d(NUV_r[mask], g_r[mask], bins=20,
                                   range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])

        # Plot less points
        fraction = randomFraction(NUV_r[mask], 0.1)

        z = t.data[p][sample]
        ax = pylab.subplot(position[type])
        pylab.axis(bounds)
        pylab.text(4.75, .25, label[type], fontsize=8)
        pylab.scatter(NUV_r[mask][fraction], g_r[mask][fraction], c=z[mask][fraction],
            marker='o', edgecolor='None', s=1, cmap=cm.spectral,
            vmin=vmin[p], vmax=vmax[p], zorder=1)
        pylab.colorbar()

        pylab.contour(h.T, extent=bounds, colors='black')

    if debug:
        pylab.show()
    else:    
        pylab.savefig('../doc/figuras/uvcolor-color-' + p + '-byclass.' + outformat, format=outformat)
