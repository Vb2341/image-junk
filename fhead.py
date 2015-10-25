#! /usr/bin/env python

import sys, glob
from astropy.io import fits

try: ext = int(sys.argv[2])
except: ext = 0

print sys.argv[1]
ims = glob.glob(sys.argv[1])
for im in ims:
    print repr(fits.getheader(im, ext))
