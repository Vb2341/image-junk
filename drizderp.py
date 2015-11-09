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
    # tweakreg.TweakReg(exps, updatehdr=True, expand_refcat=False,enforce_user_order=False, refimage=exps[0],refimagefindcfg={'threshold':2500,'conv_width':3.5,})
    astrodrizzle.AstroDrizzle(exps,output=(filt+'_'+targ).lower(),num_cores=12, mdriztab=True, in_memory=True, final_pixfrac=1)

ims = sorted(glob.glob('*flt.fits'))
orbs = list(set([i[:6] for i in ims]))

flts=[]
filts, targs = {}, {}
for f in ims:
    hdr = fits.getheader(f)
    # if hdr['FILTER'] != 'F128N':
        # continue
    # elif hdr['FILTER'] == 'F128N':
    flts.append(f)
    filts[f] = hdr['FILTER']
    targs[f] = hdr['TARGNAME']
    print f, hdr['FILTER'], hdr['TARGNAME']
print sorted(flts)
# p = Pool(12)
# p.map(updatewcs.updatewcs, flts)
# map(upwcs, flts)
print '______________________________'
for f in filts.keys():
    print f, filts[f], targs[f]
print filts.values(), targs.values()
print set(filts.values()), sorted(set(targs.values()))
teal.teal('tweakreg')

flts_by_targ = []
for targ in set(targs.values()):
    for filt in set(filts.values()):
        exps = []
        print filt
        for f in flts:
            if filts[f] == filt and targs[f] == targ:
                exps.append(f)
        flts_by_targ.append(exps)
#
teal.teal('astrodrizzle')
# p = Pool(3)
# map(reg,flts_by_targ)
#
for filt in set(filts.values()):
    exps = []
    print filt
    for f in flts:
        hdr = fits.getheader(f)
        if hdr['FILTER'] == filt:
            exps.append(f)
    print exps
#     # tweakreg.TweakReg(exps, updatewcs=True, updatehdr=True, expand_refcat=False,enforce_user_order=False, refcat='*.coo')
    # tweakreg.TweakReg(exps, updatehdr=True, expand_refcat=False, enforce_user_order=False, refimage='../m51/F110W_drz.fits',refimagefindcfg={'threshold':4,'conv_width':2.5})
#     # tweakreg.TweakReg(exps, updatehdr=True, expand_refcat=True,enforce_user_order=False, refimage=exps[4], refimagefindcfg={'threshold':1,'conv_width':2.5})
#     teal.teal('astrodrizzle')
    astrodrizzle.AstroDrizzle(exps,output=filt,num_cores=12, mdriztab=True, final_pixfrac=0.7)
#
#
# biglist=[]
# drzs = glob.glob('*drz.fits')
# for f in drzs:
#     hdr = fits.getheader(f)
#     subs =[sub[:9]+'_flt.fits' for sub in hdr['D*DATA'].values()]
#     biglist = biglist+subs
#     print 'Tweaking back {} from {}'.format(subs, f)
#     tweakback.tweakback(f,subs)
# #     # tweakreg.TweakReg(subs, updatehdr=True, expand_refcat=False, refimage=f, refimagefindcfg={'threshold':20,'conv_width':2.5})
#
# for filt in set(filts.values()):
#     exps = []
#     print filt
#     for f in flts:
#         hdr = fits.getheader(f)
#         if hdr['FILTER'] == filt:
#             exps.append(f)
#     print exps
#     astrodrizzle.AstroDrizzle(exps,output=filt,num_cores=12, mdriztab=True, in_memory=True, final_pixfrac=0.7)
