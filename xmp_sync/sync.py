import sys
import os
from .common import *
from .bib2lr import bib2lr_files
from .lr2bib import lr2bib_files

def main():
    print("Auto-using last-updated metadata...")
    for f in sys.argv[1:]:
        f = f.encode()
        bib, lr = xmp_filenames(f)

        try:
           lrtime = os.stat(lr).st_mtime
        except:
           lrtime = 0

        try:
           bibtime = os.stat(bib).st_mtime
        except:
           bibtime = 0

        if bibtime > lrtime:
            print(b'%s -> %s' % (bib, lr))
            bib2lr_files(bib, lr, f)
        elif bibtime < lrtime:
            print(b'%s -> %s' % (lr, bib))
            lr2bib_files(lr, bib, f)
        else:
           print(f.decode() + ' is already in sync.')


if __name__  == '__main__':
    main()

