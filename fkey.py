#! /usr/bin/env python

import sys, glob
from astropy.io import fits

try:
    ext = int(sys.argv[-1])
    kw = sys.argv[2:-1]
except:
    ext = 0
    kw = sys.argv[2:]
ims = glob.glob(sys.argv[1])

for im in ims:
    hdr = fits.getheader(im, ext)
    print im, ' '.join(str(hdr[k]) for k in kw)
