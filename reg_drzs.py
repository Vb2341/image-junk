from drizzlepac import astrodrizzle, tweakreg, tweakback
from stwcs import updatewcs
import glob, os
from astropy.io import fits
from multiprocessing import Pool
from stsci.tools import teal

drzs = glob.glob('f127m*drz.fits')+glob.glob('f153m*drz.fits')
teal.teal('tweakreg')
tweakreg.TweakReg(drzs, updatehdr=True, expand_refcat=False,enforce_user_order=False,refimage='F139M_drz.fits', refimagefindcfg={'threshold':25,'conv_width':2.5})
