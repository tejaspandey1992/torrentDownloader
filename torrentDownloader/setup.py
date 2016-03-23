from setuptools import setup

setup (
    name='TorrentDownloader',
    version='1.0',
    py_modules=['main'],
    install_requires=[ 'Click','bs4','requests','simplejson' ],
    entry_points='''
        [console_scripts]
        tc=main:cli
    ''',
)
