from drizzlepac import astrodrizzle, tweakreg
from stwcs import updatewcs
import glob, os
from astropy.io import fits
from multiprocessing import Pool
from stsci.tools import teal


def upwcs(flt):
    try:
        hdr = fits.open(flt)[0].header
        print hdr['FILTER'], hdr['IMAGETYP']
        # if hdr['FILTER'] =='BLANK' or hdr['FILTER'] == 'Blank' or \
        # hdr['IMAGETYP'] == 'DARK' or hdr['IMAGETYP']=='BIAS' or hdr['PHOTCORR']== 'OMIT':
        if hdr['DRIZCORR'] == 'OMIT':
            return
        else:
            print 'UPDATING WCS'
            print '_______________________________________'
            updatewcs.updatewcs(flt)
    except Exception, e:
        print flt
        print hdr
        # print fits.info(flt)
        print e
        print traceback.format_exc()


flts = glob.glob('*drz.fits')
# p = Pool(6)
# p.map(upwcs, flts)


filts, targs = {}, {}
for f in flts:
    hdr = fits.getheader(f)
    if hdr['FILTER'] != 'F153M':
        # flts.remove(f)
        continue
    elif hdr['FILTER'] == 'F153M':
        filts[f] = hdr['FILTER']
        targs[f] = hdr['TARGNAME']
        print f, hdr['FILTER']

# p = Pool(30)
# p.map(upwcs, flts)
print '______________________________'
for f in filts.keys():
    print f, filts[f], targs[f]
print filts.values(), targs.values()
teal.teal('tweakreg')
# for filt in set(filts.values()):
for filt in ['F153M']:
    exps = []
    print filt
    for f in flts:
        if fits.getheader(f)['FILTER'] == filt:
            exps.append(f)
    print exps
    # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refcat='*.coo')
    # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refimage='f673n_drz.fits',refimagefindcfg={'threshold':250,'conv_width':3.5})
    # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=True,enforce_user_order=False, refimage=exps[0],refimagefindcfg={'threshold':50,'conv_width':2.5})
    print 'Tweaked and time to DRIZZLEEEE'
    astrodrizzle.AstroDrizzle(exps,output=filt.lower(), mdriztab=True, in_memory=True, num_cores=6, final_scale=0.7, final_pixfrac=0.5)
