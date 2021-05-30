import setuptools
from discord.ext.components import __version__

with open("README.md", "r", encoding='utf-8') as f:
    long_desc = f.read()


def _requires_from_file(filename):
    return open(filename, encoding="utf8").read().splitlines()


setuptools.setup(
    name="dpy-components",
    version=__version__,
    author="sevenc_nanashi",
    description="Component for discord.py",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url="https://github.com/sevenc-nanashi/dpy-components",
    packages=['discord.ext.components'],
    project_urls={
        "Bug Tracker": "https://github.com/sevenc-nanashi/dpy-components/issues",
    },
    install_requires=_requires_from_file('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
