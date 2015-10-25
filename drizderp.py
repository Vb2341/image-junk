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


flts = glob.glob('*flt.fits')
# p = Pool(6)
# p.map(upwcs, flts)


filts, targs = {}, {}
for f in flts:
    hdr = fits.getheader(f)
    if hdr['FILTER'] != 'F139M':
        # flts.remove(f)
        continue
    elif hdr['FILTER'] == 'F139M':
        filts[f] = hdr['FILTER']
        targs[f] = hdr['TARGNAME']
        print f, hdr['FILTER']

# p = Pool(30)
# p.map(upwcs, flts)
print '______________________________'
for f in filts.keys():
    print f, filts[f], targs[f]
print filts.values(), targs.values()
# teal.teal('tweakreg')
# for filt in set(filts.values()):
for targ in targs.values()[:1]:
    for filt in ['F139M']:
        exps = []
        print filt
        for f in flts:
            hdr = fits.getheader(f)
            if hdr['FILTER'] == filt and hdr['TARGNAME'] == targ:
                exps.append(f)
        print exps
        # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refcat='*.coo')
        # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refimage='f673n_drz.fits',refimagefindcfg={'threshold':250,'conv_width':3.5})
        # tweakreg.TweakReg(exps, updatehdr=True, expand_refcat=True,enforce_user_order=False, refimage=exps[0])
        print 'Tweaked and time to DRIZZLEEEE'
        astrodrizzle.AstroDrizzle(exps,output=(filt+'_'+targ).lower(), mdriztab=True, in_memory=True, final_scale=0.7, final_pixfrac=0.5)
