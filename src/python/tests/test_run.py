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

"""
This module contains an example test.

Tests should be placed in ``src/python/tests``, in modules that mirror your
project's structure, and in files named test_*.py. They are simply functions
named ``test_*`` which test a unit of logic.

To run the tests, run ``kernelai test``.
"""
from os.path import curdir, abspath
from unittest.mock import patch
import pytest

from kernelai.io import DataCatalog
from kernelai.config import ConfigLoader
from project_irene.run import init_context, main


@patch('project_irene.run.curdir', 'invalid/')
def test_main_wrong_cwd():
    with pytest.raises(ValueError,
                       match=r'Given configuration path either does not '
                             r'exist or is not a valid directory: invalid.*'):
        main()

def test_init_context():
    project_dir = abspath(curdir)
    conf, io, params = init_context(project_dir)
    assert isinstance(conf, ConfigLoader)
    assert isinstance(io, DataCatalog)
    assert params
