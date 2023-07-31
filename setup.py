from pathlib import Path

from setuptools import setup, find_packages

long_description = Path(__name__).parent / 'README.md'
long_description = long_description.read_text()

setup(
    name='model-connect',
    version='0.0.3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(
        include=[
            'model_connect',
            'model_connect.*'
        ],
        exclude=[
            'tests',
            'tests.*'
        ]
    ),
    install_requires=[
        'setuptools~=60.2.0',
    ]
)