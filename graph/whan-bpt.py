import sys
import os
import pylab
from pylab import sqrt
from matplotlib import cm
from atpy import Table
import numpy as np 

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin:/opt/local/bin'

debug = False

def set_eps_output():
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


tablename = sys.argv[1]
t = Table(tablename)

# Sanity
clean = (t.data['nii_6584_flux'] != -999)
clean &= (t.data['oiii_5007_flux'] != -999)
clean &= (t.data['halpha_flux'] != -999)
clean &= (t.data['halpha_ew'] != -999)
clean &= (t.data['hbeta_flux'] != -999)

# take only ten percent of points
sample = (np.random.rand(len(clean)) < 0.1) & clean

# Data
logN2Ha = np.log10(t.data['nii_6584_flux'][sample] / t.data['halpha_flux'][sample])
logO3Hb = np.log10(t.data['oiii_5007_flux'][sample] / t.data['hbeta_flux'][sample])
WHa = t.data['halpha_ew'][sample]
WN2 = t.data['nii_6584_ew'][sample]
NUV_r = t.data['NUV'][sample] - t.data['r'][sample]

# Galaxy types
starforming = (logN2Ha < -0.4) & (WHa > 3.0)
sAGN = (logN2Ha > -0.4) & (WHa > 6.0)
wAGN = (logN2Ha > -0.4) & (WHa < 6.0) & (WHa > 3.0)
passive = (WHa < 0.5) |  (WN2 < 0.5)
#passive = (WHa < 0.5) |  (WHa < 0.5/np.power(10.0, logN2Ha))
retired = (WHa < 3.0) & ~passive

if not debug:
    set_eps_output()

# WHaN plot
bounds = [-1.0,0.6,.1,110.0]
ax = pylab.subplot(111)
pylab.axis(bounds)
ax.set_yscale('log')
pylab.xlabel('$\log([N_{II}] / H_{\\alpha})$')
pylab.ylabel('$W_{H\\alpha}$ [\AA]')
pylab.plot(logN2Ha[starforming], WHa[starforming], '.r', markersize=1)
pylab.plot(logN2Ha[sAGN], WHa[sAGN], '.g', markersize=1)
pylab.plot(logN2Ha[wAGN], WHa[wAGN], '.b', markersize=1)
pylab.plot(logN2Ha[passive], WHa[passive], '.k', markersize=1)
pylab.plot(logN2Ha[retired], WHa[retired], '.y', markersize=1)

# Plot constraints
pylab.axvline(-0.4, color='k')
pylab.axhline(0.5, color='k')
pylab.axhline(3.0, color='k')
pylab.axhline(6.0, color='k')
x = pylab.linspace(-1.0, 0.0, 10)
y = 0.5 / np.power(10, x)
pylab.plot(x, y, '-k')
if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/whan.eps', format='eps')


# WHaN-UV plot
pylab.figure()
bounds = [-1.0,0.6,.1,110.0]
ax = pylab.subplot(111)
pylab.axis(bounds)
ax.set_yscale('log')
pylab.xlabel('$\log([N_{II}] / H_{\\alpha})$')
pylab.ylabel('$W_{H\\alpha}$ [\AA]')

# Plot constraints
pylab.axvline(-0.4, color='k')
pylab.axhline(0.5, color='k')
pylab.axhline(3.0, color='k')
pylab.axhline(6.0, color='k')
x = pylab.linspace(-1.0, 0.0, 10)
y = 0.5 / np.power(10, x)
pylab.plot(x, y, '-k')

pylab.scatter(logN2Ha, WHa, c=NUV_r,
              marker='o', edgecolor='None', s=1, cmap=cm.spectral,
              vmin = 0.5, vmax = 7.0)
cb = pylab.colorbar()
cb.set_label('$NUV - r$')
if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/whan-uv.eps', format='eps')


# BPT-UV plot
bounds = [-1.0,0.5, -1.5,1.3]
pylab.figure()
pylab.axis(bounds)
pylab.xlabel('$\log([N_{II}] / H_{\\alpha})$')
pylab.ylabel('$\log([O_{III}] / H_{\\beta})$')
pylab.scatter(logN2Ha, logO3Hb, c=NUV_r,
              marker='o', edgecolor='None', s=1, cmap=cm.spectral,
              vmin = 0.5, vmax = 7.0)
cb = pylab.colorbar()
cb.set_label('$NUV - r$')
if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/bpt-uv.eps', format='eps')
