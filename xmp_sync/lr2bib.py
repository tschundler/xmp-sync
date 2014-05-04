import xml.etree.ElementTree as ET
import math
import os
from .common import *

import logging
logger = logging.getLogger('xmp_sync')


def lr2bib_data(src_data, dest_data, raw_file):

    in_tree = ET.fromstring(src_data)
    out_tree = ET.fromstring(dest_data)
    out_data = out_tree.find('.//*[@%srating]' % BIB_OPT_NS).attrib
    in_data = in_tree.find('.//%sDescription' % RDF_NS).attrib

    VNATTR='{http://www.bibblelabs.com/DigitalMasterFileVersion/1.0/}versionName'
    out_tree.find('.//*[@%s]' % VNATTR).attrib[VNATTR] = os.path.basename(raw_file.decode())

    out_data[BIB_OPT_NS + 'optionchanged'] = 'true'

    # rating
    rating = in_data.get('{http://ns.adobe.com/xap/1.0/}Rating') or '0'
    out_data[BIB_OPT_NS + 'rating'] = rating

    # exposure
    exposure = in_data.get(CR_OPT_NS + 'Exposure2012') or '0.00'
    out_data[BIB_OPT_NS + 'exposureval'] = exposure
    if exposure != '0.00':
    	out_data[BIB_OPT_NS + 'hasSettings'] = 'true'

    # rotation
    rotation = float(in_data.get(CR_OPT_NS + 'CropAngle') or '0.00')
    out_data[BIB_OPT_NS + 'rotateangle'] = str(-1.0 * rotation)

    # crop
    if in_data.get(CR_OPT_NS + 'HasCrop') == 'True':
         out_data[BIB_OPT_NS + 'cropon'] = 'true'
         out_data[BIB_OPT_NS + 'cropdpi'] = "1"
         # @TODO: Auto switch when 2:3 or 16:9
         out_data[BIB_OPT_NS + 'cropmenuitem'] = "Custom;0;0;1;Size"
         out_data[BIB_OPT_NS + 'croppercent'] = "1"
         out_data[BIB_OPT_NS + 'croplocked'] = "false"
         out_data[BIB_OPT_NS + 'cropstyle'] = "1"
         out_data[BIB_OPT_NS + 'cropstickydpi'] = "-1"
         out_data[BIB_OPT_NS + 'cropstickyx'] = "-1"
         out_data[BIB_OPT_NS + 'cropstickyy'] = "-1"

         rotation = math.radians(rotation)

         size = get_raw_image_size(raw_file)
         cropsize = rotated_box_size(rotation, *size)

         top = (float(in_data.get(CR_OPT_NS + 'CropTop') or '0.0') - 0.5) * size[1]
         left = (float(in_data.get(CR_OPT_NS + 'CropLeft') or '0.0') - 0.5) * size[0]
         bottom = (float(in_data.get(CR_OPT_NS + 'CropBottom') or '0.0') - 0.5) * size[1]
         right = (float(in_data.get(CR_OPT_NS + 'CropRight') or '0.0') - 0.5) * size[0]

         # in LR, these are positions on the ORIGIAL image, before rotation, so translate positions
         top, left = rotate(rotation, top, left)
         bottom, right = rotate(rotation, bottom, right)

         out_data[BIB_OPT_NS + 'croptop'] = str(top / cropsize[1] + 0.5)
         out_data[BIB_OPT_NS + 'cropleft'] = str(left / cropsize[0] + 0.5)
         out_data[BIB_OPT_NS + 'cropheight'] = str((bottom - top))
         out_data[BIB_OPT_NS + 'cropwidth'] = str((right - left))
         out_data[BIB_OPT_NS + 'croppercent'] = str((right - left) / cropsize[0])
    else:
         out_data[CR_OPT_NS + 'cropon'] = 'false'

    return ET.tostring(out_tree, encoding='utf-8')

def lr2bib_files(src_file, dest_file, raw_file):
    with open(src_file, "br") as src:
        src_data = src.read()

    if not src_data:
       return

    try:
        with open(dest_file, "br") as dest:
            dest_data = dest.read()
    except FileNotFoundError:
        raise  # not needed - Bibble with import rating for LR itself
        dest_data = """
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dmf="http://www.bibblelabs.com/DigitalMasterFile/1.0/"
    xmlns:dmfversion="http://www.bibblelabs.com/DigitalMasterFileVersion/1.0/"
    xmlns:bset="http://www.bibblelabs.com/BibbleSettings/5.0/"
    xmlns:blay="http://www.bibblelabs.com/BibbleLayers/5.0/"
    xmlns:bopt="http://www.bibblelabs.com/BibbleOpt/5.0/"
   dmf:versionCount="1">
   <dmf:versions>
    <rdf:Seq>
     <rdf:li>
      <rdf:Description
       dmfversion:software="bibble"
       dmfversion:softwareVersion="2008.1"
       dmfversion:versionName=""
       >
      <dmfversion:settings>
       <rdf:Description
        bset:curLayer="0"
        bset:respectsTransform="True"
        bset:settingsVersion="66">
       <bset:layers>
        <rdf:Seq>
         <rdf:li>
          <rdf:Description
           blay:layerId="0"
           blay:layerPos="0"
           blay:name=""
           blay:enabled="True">
          <blay:options
           bopt:optionchanged="true"
           bopt:hasSettings="false"
           bopt:metaDirty="true"
           bopt:version="8.2"
           bopt:rating="0"
           bopt:cropon="false"
           bopt:croplocked="true"
           bopt:cropstyle="0"
           bopt:cropleft="-1"
           bopt:croptop="-1"
           bopt:cropheight="2"
           bopt:cropwidth="3"
           bopt:cropdpi="-1"
           bopt:cropstickydpi="-1"
           bopt:cropstickyx="-1"
           bopt:cropstickyy="-1"
           bopt:cropmenuitem=""
           bopt:croppercent="1"
           >
          </blay:options>
          </rdf:Description>
         </rdf:li>
        </rdf:Seq>
       </bset:layers>
       </rdf:Description>
      </dmfversion:settings>
      </rdf:Description>
     </rdf:li>
    </rdf:Seq>
   </dmf:versions>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
        """

    dest_data = lr2bib_data(src_data, dest_data, raw_file)
    with open(dest_file, "wb") as dest:
        dest.write(dest_data)

    sync_mtime(src_file, dest_file)


def main():
    import sys
    print("Converting from Aftershpt to Lightroom.")
    for f in sys.argv[1:]:
        f = f.encode()
        o, i = xmp_filenames(f)
        print("Processing %s -> %s" % (i.decode(), o.decode()))
        try:
            lr2bib_files(i, o, f)
        except FileNotFoundError:
            print("No data.")
        except:
            import traceback
            traceback.print_exc()


if __name__  == '__main__':
    main()

