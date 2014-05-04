xmp-sync
========

Python tool for syncing XMP files between Bibble5/Corel Aftershot Pro and Adobe Lightroom.

Install Depndencies
-------------------

Designed for python3. Uses ``dcraw`` to get image sizes

Ubuntu::

  #sudo apt-get install imagemagick ufraw-batch
  #sudo apt-get install libtiff4-dev
  sudo apt-get install python3-dev python3-setuptools dcraw

OSX::

  brew install dcraw

Install xmp-sync
----------------

::

  python3 setup.py install

This should automatically fetch all python dependencies


Related Projects
----------------

* https://github.com/asmartin/asptools
* https://github.com/dasmaeh/xmpfix
* https://github.com/marcoil/afp2xmp 
