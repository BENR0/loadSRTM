try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Download SRTM data for domain.',
    'author': 'Benjamin Roesner',
    'url': 'https://github.com/BENR0/loadSRTM',
    'download_url': 'https://github.com/BENR0/loadSRTM',
    'author_email': '.',
    'version': '0.0',
    'install_requires': ['nose', 'tqdm'],
    'packages': ['loadSRTM'],
    'scripts': [],
    'name': 'loadSRTM'
}

setup(**config)

