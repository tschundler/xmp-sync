from setuptools import setup
xmp_sync = __import__('xmp_sync')

setup(
    name='XMP Sync',
    version=xmp_sync.__version__,
    author=xmp_sync.__author__,
    author_email=xmp_sync.__email__,
    packages=['xmp_sync'],
    install_requires=[
        'watchdog>=0.7.1',
    ],
    entry_points={
        'console_scripts': [
            'lr2bib = xmp_sync.lr2bib:main',
            'bib2lr = xmp_sync.bib2lr:main',
            'xmpsync = xmp_sync.sync:main',
            'xmpwatch = xmp_sync.watcher:main',
            ]
    },
    license=open("LICENSE").read(),
)
