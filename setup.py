# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 22:40:54 2022

@author: philippe@loco-labs.io
"""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="json_ntv",
    version="0.1.0",
    description="JSON-NTV a semantic format for interoperability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loco-philippe/NTV/blob/main/README.md",
    author="Philippe Thomy",
    author_email="philippe@loco-labs.io",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"],
    keywords="JSON-NTV, semantic JSON, development, environmental data",
    packages=find_packages(include=['json_ntv', 'json_ntv.*']),
    python_requires=">=3.7, <4",
    install_requires=['shapely', 'cbor2', 'pandas']
)
