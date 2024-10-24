# -*- coding: utf-8 -*-
"""
@author: philippe@loco-labs.io
"""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="ntv_pandas",
    version="2.0.1",
    description="NTV-pandas : A tabular analyzer and a semantic, compact and reversible converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loco-philippe/ntv-pandas/blob/main/README.md",
    author="Philippe Thomy",
    author_email="philippe@loco-labs.io",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="pandas, JSON-NTV, semantic JSON, development, environmental data",
    packages=find_packages(include=["ntv_pandas", "ntv_pandas.*"]),
    package_data={"ntv_pandas": ["*.ini"]},
    python_requires=">=3.10, <4",
    install_requires=[
        "ntv_numpy",
        "tab_analysis",
        "tab_dataset",
        "json_ntv",
        "numpy",
        "pandas",
        "shapely",
    ],
)
