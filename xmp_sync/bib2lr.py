import xml.etree.ElementTree as ET
import math
from .common import *

import logging
logger = logging.getLogger('xmp_sync')


def bib2lr_data(src_data, dest_data, raw_file):

    in_tree = ET.fromstring(src_data)
    out_tree = ET.fromstring(dest_data)
    in_data = in_tree.find('.//*[@%srating]' % BIB_OPT_NS).attrib
    out_data = out_tree.find('.//%sDescription' % RDF_NS).attrib

    # flag... wtf why isn't this saved in Lightroom?
    flag = int(in_data.get(BIB_OPT_NS + 'tag') or '0')
    
    # rating
    rating = in_data.get(BIB_OPT_NS + 'rating') or '0'
    out_data['{http://ns.adobe.com/xap/1.0/}Rating'] = rating

    # exposure
    exposure = in_data.get(BIB_OPT_NS + 'exposureval') or '0.00'
    out_data[CR_OPT_NS + 'Exposure2012'] = exposure

    # rotation
    rotation = float(in_data.get(BIB_OPT_NS + 'rotateangle') or '0.00')
    out_data[CR_OPT_NS + 'CropAngle'] = str(-1.0 * rotation)

    # crop
    if in_data.get(BIB_OPT_NS + 'cropon') == 'true':
         out_data[CR_OPT_NS + 'HasCrop'] = 'True'

         rotation = math.radians(rotation)

         size = get_raw_image_size(raw_file)
         cropsize = rotated_box_size(rotation, *size)

         cropscale = float(in_data.get(BIB_OPT_NS + 'cropdpi') or 1)

         # In AfterShot, these are positions AFTER rotation, relative to the rotated size
         width = float(in_data.get(BIB_OPT_NS + 'cropwidth')) * cropscale
         height = float(in_data.get(BIB_OPT_NS + 'cropheight')) * cropscale
         left = float(in_data.get(BIB_OPT_NS + 'cropleft')) * cropsize[0] - cropsize[0] / 2
         top = float(in_data.get(BIB_OPT_NS + 'croptop')) * cropsize[1] - cropsize[1] / 2
         bottom = top + height
         right = left + width

         # in LR, these are positions on the ORIGIAL image, before rotation, so translate positions
         top, left = rotate(rotation, top, left)
         bottom, right = rotate(rotation, bottom, right)

         out_data[CR_OPT_NS + 'CropTop'] = str(top / size[1] + 0.5)
         out_data[CR_OPT_NS + 'CropLeft'] = str(left / size[0] + 0.5)
         out_data[CR_OPT_NS + 'CropBottom'] = str(bottom / size[1] + 0.5)
         out_data[CR_OPT_NS + 'CropRight'] = str(right / size[0] + 0.5)
         
    else:
         out_data[CR_OPT_NS + 'HasCrop'] = 'False'

    return ET.tostring(out_tree, encoding='utf-8')

def bib2lr_files(src_file, dest_file, raw_file):
    with open(src_file, "br") as src:
        src_data = src.read()

    if not src_data:
       return

    try:
        with open(dest_file, "br") as dest:
            dest_data = dest.read()
    except FileNotFoundError:
        dest_data = """
   <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.5-c002 1.148022, 2012/07/15-18:06:45">
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
     <rdf:Description rdf:about=""
       xmlns:tiff="http://ns.adobe.com/tiff/1.0/"
       xmlns:exif="http://ns.adobe.com/exif/1.0/"
       xmlns:xmp="http://ns.adobe.com/xap/1.0/"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:aux="http://ns.adobe.com/exif/1.0/aux/"
       xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
       xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
       xmlns:stEvt="http://ns.adobe.com/xap/1.0/sType/ResourceEvent#"
       xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
       >
     </rdf:Description>
    </rdf:RDF>
   </x:xmpmeta>
        """

    dest_data = bib2lr_data(src_data, dest_data, raw_file)
    with open(dest_file, "wb") as dest:
        dest.write(dest_data)
    os.chmod(dest_file, int('0666', 8))  # It's a shared drive, not doing this can confuse things

    sync_mtime(src_file, dest_file)


def main():
    import sys
    print("Converting from Lightroom to AfterShot.")
    for f in sys.argv[1:]:
        f = f.encode()
        i, o = xmp_filenames(f)
        print("Processing %s -> %s" % (i.decode(), o.decode()))
        try:
            bib2lr_files(i, o, f)
        except FileNotFoundError:
            print("No data.")
        except:
            import traceback
            traceback.print_exc()


if __name__  == '__main__':
    main()

