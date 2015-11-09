from drizzlepac import astrodrizzle, tweakreg, tweakback
from stwcs import updatewcs
import glob, os
from astropy.io import fits
from multiprocessing import Pool
from stsci.tools import teal

def upwcs(f):
  print f
  updatewcs.updatewcs(f)

def reg(exps):
    hdr = fits.getheader(exps[0])
    filt = hdr['FILTER']
    targ = hdr['TARGNAME']
    prop = hdr['PROPOSID']
    vis = exps[0][4:6]
    print targ, filt, len(exps)
    astrodrizzle.AstroDrizzle(exps,output=(filt+'_'+targ+'_'+str(prop)+'_'+vis).lower(),num_cores=1, mdriztab=True, in_memory=False, final_pixfrac=1)

ims = sorted(glob.glob('*flt.fits'))
orbs = list(set([i[:6] for i in ims]))

visbyfilt = []
i=0
for orb in orbs:
    print 'Processing orbit {} of {}'.format(i+1,len(orbs))
    i+=1
    tmp = glob.glob(orb+'*flt.fits')
    hdr = fits.getheader(tmp[0])
    print 'Target appears to be {} for visit {} with {} exposures'.format(hdr['TARGNAME'], orb, len(tmp))
    filts=set([fits.getheader(f)['FILTER'] for f in tmp])
    for filt in filts:
        exps = []
        for f in tmp:
            if fits.getheader(f)['FILTER'] == filt:
                exps.append(f)
        visbyfilt.append(exps)

p = Pool(10)
print '______________________________'
print '______________________________'
print 'Updating WCS'
print '______________________________'
print '______________________________'
# p.map(upwcs, ims)


print '______________________________'
print '______________________________'
print 'Drizzling'
print '______________________________'
print '______________________________'
teal.teal('astrodrizzle')
p.map(reg, visbyfilt)
