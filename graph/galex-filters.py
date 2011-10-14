# coding=UTF-8
import sys
import pylab
from pylab import sqrt
from atpy import Table
import os

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin:/opt/local/bin'

fuv_table_name = 'galex1500.txt'
nuv_table_name = 'galex2500.txt'
fuv = Table(fuv_table_name, type='ascii')
nuv = Table(nuv_table_name, type='ascii')

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

pylab.figure(1)
pylab.axis([1200, 3100, 0, 0.7])
pylab.xlabel('$\lambda$ (\AA)')
pylab.ylabel('Transmit\^ancia')
pylab.plot(nuv.data['col1'], nuv.data['col2'], 'r-', label='NUV')
pylab.plot(fuv.data['col1'], fuv.data['col2'], 'b-', label='FUV')
pylab.legend()
#plt.show()

pylab.savefig('../doc/figuras/galex-filters.eps', format='eps')

