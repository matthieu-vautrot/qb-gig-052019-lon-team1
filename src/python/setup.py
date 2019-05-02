# QUANTUMBLACK CONFIDENTIAL
#
# Copyright (c) 2016 - present QuantumBlack Visual Analytics Ltd. All
# Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property of
# QuantumBlack Visual Analytics Ltd. and its suppliers, if any. The
# intellectual and technical concepts contained herein are proprietary to
# QuantumBlack Visual Analytics Ltd. and its suppliers and may be covered
# by UK and Foreign Patents, patents in process, and are protected by trade
# secret or copyright law. Dissemination of this information or
# reproduction of this material is strictly forbidden unless prior written
# permission is obtained from QuantumBlack Visual Analytics Ltd.

from setuptools import setup, find_packages

entry_point = 'project_irene = ' \
              'project_irene.run:main'

# get the dependencies and installs
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name='project_irene',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    entry_points={
                     'console_scripts': [entry_point]
                 },
    install_requires=requires,
    extras_require={
        'docs': [
            'sphinx>=1.6.3, <2.0',
            'sphinx_rtd_theme==0.4.1',
            'nbsphinx==0.3.4',
            'nbstripout==0.3.3',
            'jupyter_client>=5.1.0, <6.0',
            'ipykernel>=4.8.1, <5.0'
        ]
    }
)
