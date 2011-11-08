import sys
import os
import pylab
from pylab import sqrt
from matplotlib import cm
from atpy import Table
import numpy as np 

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin:/opt/local/bin'

debug = False
type = 'passive'
#type = None
outformat = 'png'


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


logN2Ha = np.log10(t.data['nii_6584_flux'] / t.data['halpha_flux'])
WHa = t.data['halpha_ew']
WN2 = t.data['nii_6584_ew']

#WHa_ = t.data['halpha_ew']
#WN2_ = t.data['nii_6584_ew']

# Galaxy types
if type == 'passive':
    typemask = (WHa < 0.5) & (WN2 < 0.5)
elif type == 'starforming':
    typemask = (logN2Ha < -0.4) & (WHa > 3.0)
elif type == 'sAGN':
    typemask = (logN2Ha > -0.4) & (WHa > 6.0)
elif type == 'wAGN':
    typemask = (logN2Ha > -0.4) & (WHa < 6.0) & (WHa > 3.0)
elif type == 'retired':
    typemask = (WHa < 3.0) & (WHa > 0.5) & (WN2 > 0.5)

sample = (t.data['z'] < -21.5)
sample &= (t.data['z'] > -23.0)
sample &= (t.data['redshift'] > 0.04) 
sample &= (t.data['redshift'] < 0.17) 
if type is not None:
    sample &= typemask

NUV_r = t.data['NUV'][sample] - t.data['r'][sample]
g_r = t.data['g'][sample] - t.data['r'][sample]

bounds = [.5,7,.2,.9]
h, ex, ey = np.histogram2d(NUV_r, g_r, bins=20,
                           range=[[bounds[0], bounds[1]],[bounds[2], bounds[3]]])

if debug:
    for col in label.keys():
        pylab.figure()
        #pylab.hist(t.data[col][sample], range=(vmin[col], vmax[col]))
        pylab.hist(t.data[col][sample])
        pylab.title(col)
        pylab.show()
    #exit()

if not debug:
    set_eps_output()

pylab.figure()
pylab.axis(bounds)
#pylab.title('Densidade')
pylab.xlabel('$NUV - r$')
pylab.ylabel('$g - r$')
pylab.hexbin(NUV_r, g_r, extent=bounds, bins='log', gridsize=50, cmap=cm.Greys)
cb = pylab.colorbar()
cb.set_label('$\log{N}$')
if debug:
    pylab.show()
    #exit()
else:
    if type is not None:
        figname = '../doc/figuras/' + type + '-uvcolor-color-density.' + outformat
    else:
        figname = '../doc/figuras/uvcolor-color-density.' + outformat
    pylab.savefig(figname, format=outformat)


for col in vmin.keys():
    z = t.data[col][sample]
    pylab.figure()
    pylab.axis(bounds)
    if debug:
        pylab.title(col)
    pylab.xlabel('$NUV - r$')
    pylab.ylabel('$g - r$')
#    pylab.scatter(NUV_r, g_r, c=z,
#        marker='o', edgecolor='None', s=1, cmap=cm.spectral,
#        vmin=vmin[col], vmax=vmax[col])
    pylab.hexbin(NUV_r, g_r, z, extent=bounds,
               gridsize=50, vmin=vmin[col], vmax=vmax[col], cmap=cm.jet)
    cb = pylab.colorbar()
    cb.set_label(label[col])
    pylab.contour(h.T, extent=bounds, colors='black')
    if type is not None:
        figname = '../doc/figuras/' + type + '-uvcolor-color-' + col + '.' + outformat
    else:
        figname = '../doc/figuras/uvcolor-color-' + col + '.' + outformat
        
    if debug:
        pylab.show()
    else:    
        pylab.savefig(figname, format=outformat)