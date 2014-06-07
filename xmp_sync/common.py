import re
import math
import subprocess
import os

BIB_OPT_NS = "{http://www.bibblelabs.com/BibbleOpt/5.0/}"
CR_OPT_NS = "{http://ns.adobe.com/camera-raw-settings/1.0/}"
RDF_NS = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"

EXT_REGEX = re.compile('\.[a-zA-Z]+$')

def xmp_filenames(filename):
    bib_file = filename + '.xmp'
    lr_file = EXT_REGEX.sub('.xmp', filename)
    return bib_file, lr_file

def rotated_box_size(rad, w, h):
    c, s = math.fabs(math.cos(rad)), math.fabs(math.sin(rad))
    return \
        w * c + h * s, \
        h * c + w * s

def rotate(rad, x, y):
    c, s = math.cos(rad), math.sin(rad)
    return \
        x * c - y * s, \
        x * s + y * c

def get_raw_image_size(raw_file):
    # parse dcraw info into dictionary
    data = dict(map(str.strip,row.split(':', 1)) for row in
        subprocess.check_output(['dcraw', '-i', '-v', raw_file], universal_newlines=True).split("\n")
        if row)

    # "Thumb size" in the image size Aftershot uses
    size = [float(s.strip()) for s in data['Thumb size'].split('x')]

    return size

def sync_mtime(src, dest):
    data = os.stat(src)
    os.utime(dest, (data.st_atime, data.st_mtime))
