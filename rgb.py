import subprocess, sys

if len(sys.argv) < 4:
    print 'Error, not enough images listed'
    print sys.argv[1:]
else:
    subprocess.call(['ds9', '-rgb','-red',sys.argv[-3],'-green',sys.argv[-2],'-blue',sys.argv[-1]])
