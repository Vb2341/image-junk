from drizzlepac import astrodrizzle, tweakreg, tweakback
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
            print 'UPDATING WCS of {}'.format(flt)
            print '_______________________________________'
            updatewcs.updatewcs(flt)
    except Exception, e:
        print flt
        print hdr
        # print fits.info(flt)
        print e
        print traceback.format_exc()

def reg(exps):
    hdr=fits.getheader(exps[0])
    print '_______________________________________'
    filt, targ = hdr['FILTER'], hdr['TARGNAME']
    if os.path.isfile((filt+'_'+targ).lower()+'_drz.fits'): return
    print filt, targ
    print '_______________________________________'
    tweakreg.TweakReg(exps, updatehdr=True, expand_refcat=True,enforce_user_order=False, refimage=exps[0],refimagefindcfg={'threshold':100,'conv_width':2.5,'peakmin':1500,'peakmax':5000})
    astrodrizzle.AstroDrizzle(exps,output=(filt+'_'+targ).lower(),num_cores=12, mdriztab=True, in_memory=True, final_pixfrac=0.7)

ims = glob.glob('*v38*drz.fits')
# p = Pool(6)
# p.map(upwcs, flts)

flts=[]
filts, targs = {}, {}
for f in ims:
    hdr = fits.getheader(f)
    if hdr['FILTER'] != 'F153M':
        continue
    elif hdr['FILTER'] == 'F153M':
        flts.append(f)
        filts[f] = hdr['FILTER']
        targs[f] = hdr['TARGNAME']
        print f, hdr['FILTER'], hdr['TARGNAME']

# p = Pool(12)
# p.map(upwcs, flts)
print '______________________________'
for f in filts.keys():
    print f, filts[f], targs[f]
print filts.values(), targs.values()
print set(filts.values()), set(targs.values())
teal.teal('tweakreg')

flts_by_targ = []
# for targ in set(targs.values()):
#     filt = 'F153M'
#     exps = []
#     print filt
#     for f in flts:
#         if filts[f] == filt and targs[f] == targ:
#             exps.append(f)
#     flts_by_targ.append(exps)

# p = Pool(4)
# map(reg,flts_by_targ)

        # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refcat='*.coo')
        # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refimage='f673n_drz.fits',refimagefindcfg={'threshold':250,'conv_width':3.5})
        # tweakreg.TweakReg(exps, updatehdr=True, expand_refcat=True,enforce_user_order=False, refimage=exps[0])
        # print 'Tweaked and time to DRIZZLEEEE'
        # astrodrizzle.AstroDrizzle(exps,output=(filt+'_'+targ).lower(),num_cores=12, mdriztab=True, in_memory=True, final_pixfrac=0.7)
#
for filt in ['F153M']:
    exps = []
    print filt
    for f in flts:
        hdr = fits.getheader(f)
        if hdr['FILTER'] == filt:
            exps.append(f)
    print exps
    # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refcat='*.coo')
    # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refimage='f673n_drz.fits',refimagefindcfg={'threshold':250,'conv_width':3.5})
    tweakreg.TweakReg(exps, updatehdr=True, expand_refcat=True,enforce_user_order=False, refimage='f153m_mw-nsc-v38-copy_drz.fits', refimagefindcfg={'threshold':50,'conv_width':2.5})
#
x = raw_input('DID THE TWEAK WORK?  IF NOT RESPOND n')
if x=='n': raise
#
biglist=[]
for f in exps:
    hdr = fits.getheader(f)
    subs =[sub[:9]+'_flt.fits' for sub in hdr['D*DATA'].values()]
    biglist = biglist+subs
    tweakback.tweakback(f,subs)

x = raw_input('DID THE TWEAKBACK WORK?  IF NOT RESPOND n')
if x=='n': raise

teal.teal('astrodrizzle')
astrodrizzle.AstroDrizzle(biglist,output='test',num_cores=12, mdriztab=True, in_memory=True, final_pixfrac=0.7)
