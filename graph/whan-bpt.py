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
              'figure.subplot.hspace': .5,
              'figure.figsize': fig_size}
    pylab.rcParams.update(params)

# take only ten percent of points
def oneInTen(arr):
    return (np.random.rand(len(arr)) < 0.1) & arr



tablename = sys.argv[1]
t = Table(tablename)

# Data
logN2Ha = np.log10(t.data['nii_6584_flux'] / t.data['halpha_flux'])
logO3Hb = np.log10(t.data['oiii_5007_flux'] / t.data['hbeta_flux'])
WHa = t.data['halpha_ew']
WN2 = t.data['nii_6584_ew']
NUV_r = t.data['NUV'] - t.data['r']
g_r = t.data['g'] - t.data['r']

# Galaxy types
passive = (WHa < 0.5) & (WN2 < 0.5)
#passive = (WHa < 0.5) |  (WHa < 0.5/np.power(10.0, logN2Ha))
starforming = (logN2Ha < -0.4) & (WHa > 3.0) & ~passive
sAGN = (logN2Ha > -0.4) & (WHa > 6.0) & ~passive
wAGN = (logN2Ha > -0.4) & (WHa < 6.0) & (WHa > 3.0) & ~passive
retired = (WHa < 3.0) & (WHa > 0.5) & (WN2 > 0.5)
remaining = ~passive & ~starforming & ~sAGN & ~wAGN & ~retired 

if not debug:
    set_eps_output()


# Color histogram

# Optical
pylab.figure()
pylab.subplot(211)
bounds = (0,1,0.0,1.1)
pylab.axis(bounds)
range = (bounds[0], bounds[1])
bins = 50
h, e = pylab.histogram(g_r[starforming], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'b-', label='SFG')

h, e = pylab.histogram(g_r[sAGN], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), '-', color='lightgreen', label='sAGN')

h, e = pylab.histogram(g_r[wAGN], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), '-', color='darkgreen', label='wAGN')

h, e = pylab.histogram(g_r[passive], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'r-', label='PG')

h, e = pylab.histogram(g_r[retired], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'k-', label='RG')
pylab.legend(loc='upper left')
pylab.xlabel('$g - r$')

# UV
pylab.subplot(212)
bounds = (0.0,7.0,0.0,1.1)
pylab.axis(bounds)
range = (bounds[0], bounds[1])
bins = 50
h, e = pylab.histogram(NUV_r[starforming], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'b-', label='SFG')

h, e = pylab.histogram(NUV_r[sAGN], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), '-', color='lightgreen', label='sAGN')

h, e = pylab.histogram(NUV_r[wAGN], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), '-', color='darkgreen', label='wAGN')

h, e = pylab.histogram(NUV_r[passive], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'r-', label='PG')

h, e = pylab.histogram(NUV_r[retired], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'k-', label='RG')
#pylab.legend(loc='upper left')
pylab.xlabel('$NUV - r$')
if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/histo_galtype_color.eps', format='eps')


# WHaN plot
bounds = [-1.0,0.6,.1,110.0]
ax = pylab.subplot(111)
pylab.axis(bounds)
ax.set_yscale('log')
pylab.xlabel('$\log([N_{II}] / H_{\\alpha})$')
pylab.ylabel('$W_{H\\alpha}$ [\AA]')

sample = oneInTen(starforming)
pylab.plot(logN2Ha[sample], WHa[sample], '.b', markersize=.1)

sample = oneInTen(sAGN)
pylab.plot(logN2Ha[sample], WHa[sample], '.', color='lightgreen', markersize=.1)

sample = oneInTen(wAGN)
pylab.plot(logN2Ha[sample], WHa[sample], '.', color='darkgreen', markersize=.1)

sample = oneInTen(passive)
pylab.plot(logN2Ha[sample], WHa[sample], '.r', markersize=.1)

sample = oneInTen(retired)
pylab.plot(logN2Ha[sample], WHa[sample], '.k', markersize=.1)

sample = oneInTen(remaining)
pylab.plot(logN2Ha[sample], WHa[sample], '.m', markersize=.1)

# Plot constraints
pylab.axvline(-0.4, color='k', linestyle='--')
pylab.axhline(0.5, color='k', linestyle='--')
pylab.axhline(3.0, color='k', linestyle='--')
pylab.axhline(6.0, color='k', linestyle='--')
x = pylab.linspace(-1.0, 0.0, 10)
y = 0.5 / np.power(10, x)
pylab.plot(x, y, '--k')
if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/whan.eps', format='eps')


# WHaN-UV plot
logWHa = np.log10(WHa)
pylab.figure()
#bounds = [-1.0,0.6,np.log10(.1),np.log10(110.0)]
bounds = [-1.0,0.6,-1.0,2.5]
ax = pylab.subplot(111)
pylab.axis(bounds)
#ax.set_yscale('log')
pylab.xlabel('$\log([N_{II}] / H_{\\alpha})$')
pylab.ylabel('$\log(W_{H\\alpha}/[\mathrm{\AA}])$')

# Plot constraints
pylab.axvline(-0.4, color='k', linestyle='--', label='bla')
pylab.axhline(np.log10(0.5), color='k', linestyle='--')
pylab.axhline(np.log10(3.0), color='k', linestyle='--')
pylab.axhline(np.log10(6.0), color='k', linestyle='--')
x = pylab.linspace(-1.0, 0.0, 10)
y = 0.5 / np.power(10, x)
#pylab.plot(x, y, '--k')

#pylab.scatter(logN2Ha, logWHa, c=NUV_r,
#              marker='o', edgecolor='None', s=1, cmap=cm.spectral,
#              vmin = 0.5, vmax = 7.0)
pylab.hexbin(logN2Ha, logWHa, NUV_r, extent=bounds, gridsize=50,
              cmap=cm.spectral, vmin = 0.5, vmax = 7.0)
cb = pylab.colorbar()
cb.set_label('$NUV - r$')

h, ex, ey = np.histogram2d(logN2Ha, logWHa, bins=20 ,
                           range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])
# Hack so log(h) does not blow in my face.
h = h + 1

pylab.contour(np.log10(h.T), extent=bounds, colors='black')
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
#pylab.scatter(logN2Ha, logO3Hb, c=NUV_r,
#              marker='o', edgecolor='None', s=1, cmap=cm.spectral,
#              vmin = 0.5, vmax = 7.0)
pylab.hexbin(logN2Ha, logO3Hb, NUV_r, extent=bounds, gridsize=50,
              cmap=cm.spectral, vmin = 0.5, vmax = 7.0)
cb = pylab.colorbar()
cb.set_label('$NUV - r$')

h, ex, ey = np.histogram2d(logN2Ha, logO3Hb, bins=20 ,
                           range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])

pylab.contour(h.T, extent=bounds, colors='black')

if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/bpt-uv.eps', format='eps')
    
    
