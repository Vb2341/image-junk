from drizzlepac import astrodrizzle, tweakreg, tweakback
from stwcs import updatewcs
import glob, os
from astropy.io import fits
from multiprocessing import Pool
from stsci.tools import teal


def tback(drz):
    flts = tweakback.extract_input_filenames(drz)
    print 'Tweaking back exposures for ', drz
    tweakback.tweakback(drz,input=flts)


drzs=glob.glob('f127m*drz.fits')+glob.glob('f153m*drz.fits')
p = Pool(10)
p.map(tback, drzs)
