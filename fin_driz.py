from drizzlepac import astrodrizzle, tweakreg, tweakback
from stwcs import updatewcs
import glob, os
from astropy.io import fits
from multiprocessing import Pool
from stsci.tools import teal

filts=['F139M', 'F153M']
fs = glob.glob('*flt.fits')
teal.teal('astrodrizzle')
for filt in filts:
    exps = []
    for f in fs:
        expfil = fits.getheader(f)['FILTER']
        if expfil == filt:
            print f
            exps.append(f)
    astrodrizzle.AstroDrizzle(exps,output=filt+'_v2', mdriztab=False, num_cores=12, in_memory=False, final_pixfrac=0.75, final_scale=0.075)
