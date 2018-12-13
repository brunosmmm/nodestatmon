"""Setup."""

from setuptools import setup, find_packages

setup(
    name='nodestatman',
    version='0.1',
    packages=find_packages(),
    package_dir={'':'.'},
    install_requires=[
        'paho-mqtt>=1.4.0',
        'wifi>=0.3.8',
        'shortuuid>=0.5.0'
    ],
    author='Bruno Morais',
    author_email='brunosmmm@gmail.com',
    description='Node stats manager',
    scripts=['statman']
)
