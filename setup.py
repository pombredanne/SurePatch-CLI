import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="surepatch",
    version="0.2.3",
    author="BrainBankers",
    author_email="ws.bespalov@gmail.com",
    description=("CLI App - Console client for SurePatch project"),
    packages=["surepatch", ],
    license="BSD",
    url="",
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 5 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License"
    ]
)
