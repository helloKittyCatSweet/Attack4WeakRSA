#!/usr/bin/env python3
"""
Setup script for Common Modulus Attack package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="common-modulus-attack",
    version="1.0.0",
    author="NTU SC6104 Student",
    description="Common Modulus Attack on RSA and ECC-RSA variants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Attack4WeakRSA",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pycryptodome>=3.15.0",
    ],
    entry_points={
        "console_scripts": [
            "common-modulus-attack=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

