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

def set_eps_output_5x2():
    # From http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
    fig_width_pt = 448.07378
    inches_per_pt = 1.0 / 72.27
    golden_mean = (sqrt(5) - 1.0) / 2.0
    fig_width = fig_width_pt * inches_per_pt
    fig_height = fig_width * golden_mean * 2.0
    fig_size = (fig_width, fig_height)
    params = {'backend': 'ps',
              'axes.labelsize': 8,
              'text.fontsize': 8,
              'title.horizontalalignment': 'left',
              'legend.fontsize': 8,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              'text.usetex': True,
              'font.family': 'serif',
              'figure.subplot.hspace': .7,
              'figure.subplot.wspace': .15,
              'figure.subplot.left': 0.05,
              'figure.subplot.right': 0.95,
              'figure.subplot.top': 0.95,
              'figure.subplot.bottom': 0.05,
              'figure.figsize': fig_size}
    pylab.rcParams.update(params)

def randomFraction(arr, f):
    return (np.random.rand(len(arr)) < f)


tablename = sys.argv[1]
t = Table(tablename)

redshift_filter = (t.data['redshift'] < 0.17) & (t.data['redshift'] > 0.04)


# Completeness in redshift
bounds = [0.04, 0.17, -24.5, -18.5]

redshift = t.data['redshift'][redshift_filter]
Mr = t.data['r'][redshift_filter]

set_eps_output_1()
pylab.figure()
pylab.axis(bounds)
pylab.xlabel('Redshift')
pylab.ylabel('$r$')
pylab.hexbin(redshift, Mr, extent=bounds, bins='log', gridsize=50, cmap=cm.Oranges)

if debug:
    pylab.show()
else:    
    pylab.savefig('../doc/figuras/completeness-volume.' + outformat, format=outformat)



# Histograms

cols = ['FUV', 'NUV', 'nii_6584_flux', 'halpha_ew',
        'at_flux', 'at_mass', 'am_flux', 'am_mass', 'mcor_gal', 'AV']

filter = {'FUV': t.data['FUV'] <> -999,
          'NUV': t.data['NUV'] <> -999,
          'nii_6584_flux': t.data['nii_6584_flux'] > 0,
          'halpha_ew': t.data['halpha_ew'] > 0,
          'at_flux': (t.data['at_flux'] <> -999) ,
          'at_mass': t.data['at_mass'] <> -999,
          'am_flux': t.data['am_flux'] <> -999,
          'am_mass': t.data['am_mass'] <> -999,
          'mcor_gal': t.data['mcor_gal'] <> -999,
          'AV': t.data['AV'] <> -999
          }


op = {'FUV':None,
          'NUV': None,
          'nii_6584_flux': np.log10,
          'halpha_ew': np.log10,
          'at_flux': None,
          'at_mass': None,
          'am_flux': None,
          'am_mass': None,
          'mcor_gal': None,
          'AV': None
          }

range = {'FUV': (-22.0, -12.0),
          'NUV':  (-22.0, -12.0),
          'nii_6584_flux': (0.0, 3.5),
          'halpha_ew': (-1.0, 2.5),
          'at_flux': (7.0, 10.25),
          'at_mass': (9.0, 10.25),
          'am_flux': (0, 2.5),
          'am_mass': (0, 2.5),
          'mcor_gal': (8.0, 13.0),
          'AV': (-0.7, 1.5)
          }

title     = {'FUV': '\\textbf{(a)} $\\mathrm{FUV}$',
          'NUV': '\\textbf{(b)} $\\mathrm{NUV}$',
          'at_flux': '\\textbf{(c)} $<\\!\\log(t_{\\star})\\!>_F$',
          'at_mass': '\\textbf{(d)} $<\\!\\log(t_{\\star})\\!>_M$',
          'am_flux': '\\textbf{(e)} $<\\!\\log(Z_{\\star}/Z_{\\odot})\\!>_F$',
          'am_mass': '\\textbf{(f)} $<\\!\\log(Z_{\\star}/Z_{\\odot})\\!>_M$',
          'mcor_gal': '\\textbf{(g)} $\\log(M_{\\star}/M_{\\odot})$',
          'AV': '\\textbf{(h)} $A_V$',
          'nii_6584_flux': '\\textbf{(i)} $\\log([\mathrm{N\\,II}]/[\\mathrm{erg}\\,\\mathrm{cm}^2\\, \\mathrm{s}^{-1}])$',
          'halpha_ew': '\\textbf{(j)} $\\log(W_{\\mathrm{H}\\alpha}/[\\mathrm{\\AA}])$',
          }

position = {'FUV': 521,
          'NUV': 522,
          'at_flux': 523,
          'at_mass': 524,
          'am_flux': 525,
          'am_mass': 526,
          'mcor_gal': 527,
          'AV': 528,
          'nii_6584_flux': 529,
          'halpha_ew': 520,
          }


set_eps_output_5x2()
pylab.figure()
for col in cols:
    pylab.subplot(position[col])
    if op[col] is not None:
        x = op[col](t.data[col])
    else:
        x = t.data[col]
    x1 = x[filter[col] & redshift_filter]
    h1, e1 = pylab.histogram(x1, 50, range[col])
    pylab.title(title[col], ha='left', x=0.0, y=1.0)
    pylab.ylim(0.0, 1.1)
    pylab.setp(pylab.gca(), 'yticklabels', [])
    pylab.plot(e1[:-1], h1*1.0/np.max(h1), 'k-')

if debug:
    pylab.show()
else:    
    pylab.savefig('../doc/figuras/histogram-sample.' + outformat, format=outformat)

