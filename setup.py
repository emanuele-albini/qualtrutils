import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qualtrutils",
    version="0.0.1",
    author="Emanuele Albini",
    description="A simple package to interact with the Qualtrics API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emanuele-albini/qualtrutils",
    project_urls={
        "Bug Tracker": "https://github.com/emanuele-albini/qualtrutils/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=['qualtrutils'],
    # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'tqdm',
        'toml',
        'requests',
    ]
)

# Create configuration
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, '.qualtrutils')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'qualtrics.toml')

# Create config dir
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

