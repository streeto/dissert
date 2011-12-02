import sys
import os
import pylab
from pylab import sqrt
from matplotlib import cm
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
              'legend.fontsize': 8,
              'xtick.labelsize': 10,
              'ytick.labelsize': 10,
              'text.usetex': True,
              'font.family': 'serif',
              'figure.subplot.hspace': .5,
              'figure.subplot.bottom': 0.12,
              'figure.figsize': fig_size}
    pylab.rcParams.update(params)

def set_eps_output_2x1():
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
              'legend.fontsize': 8,
              'xtick.labelsize': 10,
              'ytick.labelsize': 10,
              'text.usetex': True,
              'font.family': 'serif',
              'figure.subplot.hspace': .5,
              'figure.figsize': fig_size}
    pylab.rcParams.update(params)

# FIXME: take only ten percent of points
def oneInTen(arr):
    return (np.random.rand(len(arr)) < 0.1) & arr


tablename = sys.argv[1]
t = Table(tablename)

sample = (t.data['redshift'] > 0.04) 
sample &= (t.data['redshift'] < 0.17) 

print('Total: %d' % len(t.data['r'][sample]))



# Data
logN2Ha = np.log10(t.data['nii_6584_flux'][sample] / t.data['halpha_flux'][sample])
logO3Hb = np.log10(t.data['oiii_5007_flux'][sample] / t.data['hbeta_flux'][sample])
WHa = t.data['halpha_ew'][sample]
WN2 = t.data['nii_6584_ew'][sample]
NUV_r = t.data['NUV'][sample] - t.data['r'][sample]
g_r = t.data['g'][sample] - t.data['r'][sample]

# Galaxy types
passive = (WHa < 0.5) & (WN2 < 0.5)
#passive = (WHa < 0.5) |  (WHa < 0.5/np.power(10.0, logN2Ha))
starforming = (logN2Ha < -0.4) & (WHa > 3.0) & ~passive
sAGN = (logN2Ha > -0.4) & (WHa > 6.0) & ~passive
wAGN = (logN2Ha > -0.4) & (WHa < 6.0) & (WHa > 3.0) & ~passive
retired = (WHa < 3.0) & (WHa > 0.5) & (WN2 > 0.5)
remaining = ~passive & ~starforming & ~sAGN & ~wAGN & ~retired 


# Color histogram
set_eps_output_1()
pylab.figure()

# Optical
pylab.subplot(211)
bounds = (0.2,0.9,0.0,1.1)
pylab.axis(bounds)
range = (bounds[0], bounds[1])
bins = 50
h, e = pylab.histogram(g_r[starforming], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'b-', label='SFG')

h, e = pylab.histogram(g_r[sAGN], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), '-', color='lightgreen', label='sAGN')

h, e = pylab.histogram(g_r[wAGN], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), '-', color='darkgreen', label='wAGN')

h, e = pylab.histogram(g_r[retired], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'k-', label='RG')

h, e = pylab.histogram(g_r[passive], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'r-', label='PG')

pylab.legend(loc='upper left')
pylab.xlabel('$g - r$')

# UV
pylab.subplot(212)
bounds = (1.0,6.5,0.0,1.1)
pylab.axis(bounds)
range = (bounds[0], bounds[1])
bins = 50
h, e = pylab.histogram(NUV_r[starforming], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'b-', label='SFG')
print('SFG: %d' % len(NUV_r[starforming]))

h, e = pylab.histogram(NUV_r[sAGN], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), '-', color='lightgreen', label='sAGN')
print('sAGN: %d' % len(NUV_r[sAGN]))

h, e = pylab.histogram(NUV_r[wAGN], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), '-', color='darkgreen', label='wAGN')
print('wAGN: %d' % len(NUV_r[wAGN]))

h, e = pylab.histogram(NUV_r[retired], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'k-', label='RG')
print('RG: %d' % len(NUV_r[retired]))

h, e = pylab.histogram(NUV_r[passive], bins, range)
pylab.plot(e[:-1], h*1.0/np.max(h), 'r-', label='PG')
print('PG: %d' % len(NUV_r[passive]))

#pylab.legend(loc='upper left')
pylab.xlabel('$\\mathrm{NUV} - r$')
if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/histo_galtype_color.' + outformat, format=outformat)


# WHaN plot
set_eps_output_1()
pylab.figure()
bounds = [-1.0,0.6,-1.0,2.5]

pylab.axis(bounds)
pylab.xlabel('$\\log([N\,II] / H\\alpha)$')
pylab.ylabel('$\\log(W_{H\\alpha}/[\\mathrm{\\AA}])$')

clean = (t.data['nii_6584_flux'][sample] > 0.0) & (t.data['halpha_flux'][sample] > 0.0)

plot = oneInTen(starforming) & clean
pylab.scatter(logN2Ha[plot], np.log10(WHa[plot]), c='b', marker='o', edgecolor='None', s=1)

plot = oneInTen(sAGN) & clean
pylab.scatter(logN2Ha[plot], np.log10(WHa[plot]), c='lightgreen', marker='o', edgecolor='None', s=1)

plot = oneInTen(wAGN) & clean
pylab.scatter(logN2Ha[plot], np.log10(WHa[plot]), c='darkgreen', marker='o', edgecolor='None', s=1)

plot = oneInTen(retired) & clean
pylab.scatter(logN2Ha[plot], np.log10(WHa[plot]), c='k', marker='o', edgecolor='None', s=1)

plot = oneInTen(passive) & clean
pylab.scatter(logN2Ha[plot], np.log10(WHa[plot]), c='r', marker='o', edgecolor='None', s=1)

plot = oneInTen(remaining) & clean
pylab.scatter(logN2Ha[plot], np.log10(WHa[plot]), c='m', marker='o', edgecolor='None', s=1)

# Plot constraints
pylab.axhline(np.log10(3.0), color='k', linestyle='-')

y = pylab.linspace(np.log10(3.0), 2.5, 10)
x = -0.4 * pylab.ones(len(y))
pylab.plot(x, y, color='k', linestyle='-')

x = pylab.linspace(-0.4, 0.6, 10)
y = np.log10(6.0) * pylab.ones(len(x))
pylab.plot(x, y, color='k', linestyle='-')

x = pylab.linspace(0.0, 0.6, 10)
y = np.log10(0.5) * pylab.ones(len(x))
pylab.plot(x, y, color='k', linestyle='--')

x = pylab.linspace(-1.0, 0, 10)
y = np.log10(0.5) * pylab.ones(len(x))
pylab.plot(x, y, color='k', linestyle=':')

x = pylab.linspace(0.0, 0.6, 10)
y = np.log10(0.5/5.0) * x + np.log10(0.5)
pylab.plot(x, y, color='k', linestyle=':')

x = pylab.linspace(np.log10(1.0/6.0), 0.0, 10)
y = np.log10(0.5/5.0) * x + np.log10(0.5)
pylab.plot(x, y, '--k')


pylab.text(-0.9, 0.75, 'SFG')
pylab.text(0.3, 1.0, 'sAGN')
pylab.text(0.3, 0.55, 'wAGN')
pylab.text(0.45, 0.0, 'RG')
pylab.text(-0.5, -0.75, 'PG')

pylab.plot(x, y, '--k')
if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/whan.' + outformat, format=outformat)


# WHaN-UV plot
logWHa = np.log10(WHa)
pylab.figure()
#bounds = [-1.0,0.6,np.log10(.1),np.log10(110.0)]
bounds = [-1.0,0.6,-1.0,2.5]
ax = pylab.subplot(111)
pylab.axis(bounds)
pylab.xlabel('$\\log([N\,II] / H\\alpha)$')
pylab.ylabel('$\\log(W_{H\\alpha}/[\\mathrm{\\AA}])$')

# Plot constraints
pylab.axhline(np.log10(3.0), color='k', linestyle='-')

y = pylab.linspace(np.log10(3.0), 2.5, 10)
x = -0.4 * pylab.ones(len(y))
pylab.plot(x, y, color='k', linestyle='-')

x = pylab.linspace(-0.4, 0.6, 10)
y = np.log10(6.0) * pylab.ones(len(x))
pylab.plot(x, y, color='k', linestyle='-')

x = pylab.linspace(0.0, 0.6, 10)
y = np.log10(0.5) * pylab.ones(len(x))
pylab.plot(x, y, color='k', linestyle='--')

x = pylab.linspace(-1.0, 0, 10)
y = np.log10(0.5) * pylab.ones(len(x))
pylab.plot(x, y, color='k', linestyle=':')

x = pylab.linspace(0.0, 0.6, 10)
y = np.log10(0.5/5.0) * x + np.log10(0.5)
pylab.plot(x, y, color='k', linestyle=':')

x = pylab.linspace(np.log10(1.0/6.0), 0.0, 10)
y = np.log10(0.5/5.0) * x + np.log10(0.5)
pylab.plot(x, y, '--k')

# Labels
pylab.text(-0.9, 0.75, 'SFG')
pylab.text(0.3, 1.0, 'sAGN')
pylab.text(0.3, 0.55, 'wAGN')
pylab.text(0.45, 0.0, 'RG')
pylab.text(-0.5, -0.75, 'PG')



clean = (t.data['nii_6584_flux'][sample] > 0.0) & (t.data['halpha_flux'][sample] > 0.0)
clean &= oneInTen(clean)

pylab.scatter(logN2Ha[clean], logWHa[clean], c=NUV_r[clean],
              marker='o', edgecolor='None', s=1, cmap=cm.spectral,
              vmin = 0.5, vmax = 7.0)
#pylab.hexbin(logN2Ha[clean], logWHa[clean], NUV_r[clean], extent=bounds, gridsize=50,
#              cmap=cm.spectral, vmin = 0.5, vmax = 7.0)
cb = pylab.colorbar()
cb.set_label('$\\mathrm{NUV} - r$')

#h, ex, ey = np.histogram2d(logN2Ha[clean], logWHa[clean], bins=20 ,
#                           range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])
# Hack so log(h) does not blow in my face.
#h = h + 1

#pylab.contour(np.log10(h.T), extent=bounds, colors='black')
if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/whan-uv.' + outformat, format=outformat)


# BPT-UV plot
bounds = [-1.0,0.5, -1.5,1.3]
pylab.figure()
pylab.axis(bounds)
pylab.xlabel('$\log([N\,II] / H\\alpha)$')
pylab.ylabel('$\log([O\,III] / H\\beta)$')

clean = (t.data['nii_6584_flux'][sample] > 0.0) & (t.data['halpha_flux'][sample] > 0.0)
clean &= (t.data['oiii_5007_flux'][sample] > 0.0) & (t.data['hbeta_flux'][sample] > 0.0)
clean &= oneInTen(clean)

pylab.scatter(logN2Ha[clean], logO3Hb[clean], c=NUV_r[clean],
              marker='o', edgecolor='None', s=1, cmap=cm.spectral,
              vmin = 0.5, vmax = 7.0)
#pylab.hexbin(logN2Ha[clean], logO3Hb[clean], NUV_r[clean], extent=bounds, gridsize=50,
#              cmap=cm.spectral, vmin = 0.5, vmax = 7.0)

pylab.text(-0.7, -0.5, 'SFG')
pylab.text(-0.5, 0.6, 'Seyfert')
pylab.text(0.0, -0.5, 'LINER')


# Plot constraints

# S06
x = np.linspace(-1.0, -0.3, 100)
y = 0.96 + 0.29 / (x + 0.20)
pylab.plot(x, y, color='k', linestyle='--')

# K03
#x = np.linspace(-1.0, 0.0, 100)
#y = 1.30 + 0.61 / (x - 0.05)
#pylab.plot(x, y, color='k', linestyle='--')

# K06
x = np.linspace(-0.5, 0.5, 10)
y = 1.01 * x + 0.48
pylab.plot(x, y, color='k', linestyle='--')

cb = pylab.colorbar()
cb.set_label('$\\mathrm{NUV} - r$')

#h, ex, ey = np.histogram2d(logN2Ha[clean], logO3Hb[clean], bins=20 ,
#                           range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])

#pylab.contour(h.T, extent=bounds, colors='black')

if debug:
    pylab.show()
else:
    pylab.savefig('../doc/figuras/bpt-uv.' + outformat, format=outformat)
    
    
