import setuptools
import pkg_resources
import os

# setup.cfg
pkg_resources.require('setuptools>=39.2')

setuptools.setup()

# Create configuration
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, '.qualtrutils')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'qualtrics.toml')

# Create config dir
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
