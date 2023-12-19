# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
from distutils.core import setup
try:
    from mujincommon.setuptools import Distribution
except (ImportError, SyntaxError):
    from distutils.dist import Distribution

version = {}
exec(open('mujinvisioncontrollerclient/version.py').read(), version)

setup(
    distclass=Distribution,
    name='mujinvisioncontrollerclient',
    version=version['__version__'],
    packages=[
        'visionapi',
        'mujinvisioncontrollerclient'
    ],
    license='Apache License, Version 2.0',
    long_description=open('README.rst').read(),
    # flake8 compliance configuration
    enable_flake8=True,  # Enable checks
    fail_on_flake=True,  # Fail builds when checks fail
    install_requires=[
        'six',
        'pyzmq',
        'mujinplanningclient>=0.1.4',
        'mujinvisionmanager>=0.0.2',
        'mujinclientgenerators>=0.2.4',
    ],
    api_spec=["visionapi.spec.visionControllerClientSpec"],
    generate_packages=[
        (
            'mujinvisioncontrollerclientgenerated',
            'mujinclientgenerators.generateClient.GenerateClient',
            {
                'specDictName': 'visionapi.spec.visionControllerClientSpec',
                'generatorSettingsDictName': 'visionapi.generatorSettings.generatorSettingsDict',
                'language': 'python'
            }
        )
    ]
)
