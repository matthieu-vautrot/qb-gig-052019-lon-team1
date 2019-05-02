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

"""XlsLocalDataSet loads and saves data to a local Excel file. The
underlying functionality is supported by pandas, so it supports all
allowed pandas options for loading and saving Excel files.
"""
from os.path import isfile
from typing import Any, Mapping, Union, Dict

import pandas as pd

from kernelai.io.core import AbstractDataSet, ExistsMixin


class XlsLocalDataSet(AbstractDataSet, ExistsMixin):
    """``XlsLocalDataSet`` loads and saves data to a local Excel file. The
    underlying functionality is supported by pandas, so it supports all
    allowed pandas options for loading and saving Excel files.
    Example:
    ::
        >>> import pandas as pd
        >>>
        >>> data = pd.DataFrame({'col1': [1, 2], 'col2': [4, 5],
        >>>                      'col3': [5, 6]})
        >>> data_set = XlsLocalDataSet(filepath="test.xlsx",
        >>>                            load_args={'sheet_name':"Sheet1"},
        >>>                            save_args=None)
        >>> data_set.save(data)
        >>> reloaded = data_set.load()
        >>>
        >>> assert data.equals(reloaded)
    """

    def _describe(self) -> Mapping[str, Any]:
        return dict(filepath=self._filepath,
                    engine=self._engine,
                    load_args=self._load_args,
                    save_args=self._save_args)

    def __init__(self, filepath: str,
                 engine: str = 'xlsxwriter',
                 load_args: Mapping[str, Any] = None,
                 save_args: Mapping[str, Any] = None) -> None:
        """Creates a new instance of ``XlsLocalDataSet`` pointing to a concrete
        filepath.
        Args:
            engine (str): The engine used to write to excel files. The default
                          engine is 'xlswriter'.
            filepath (str): path to an Excel file
            load_args (Optional[Mapping[str, Any]]): Pandas options for loading
                Excel files. Here you can find all available arguments:
                https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_excel.html
                The default_load_arg engine is 'xlrd', all others preserved.
            save_args (Optional[Mapping[str, Any]]): Pandas options for saving
                Excel files. Here you can find all available arguments:
                https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_excel.html
                All defaults are preserved
        """
        self._filepath = filepath
        default_save_args = {}
        default_load_args = {"engine": "xlrd"}

        self._load_args = {**default_load_args, **load_args} \
            if load_args is not None else default_load_args
        self._save_args = {**default_save_args, **save_args} \
            if save_args is not None else default_save_args
        self._engine = engine

    def _load(self) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        return pd.read_excel(self._filepath, **self._load_args)

    def _save(self, data: pd.DataFrame) -> None:
        writer = pd.ExcelWriter(self._filepath, engine=self._engine)
        data.to_excel(writer, **self._save_args)
        writer.save()

    def _exists(self) -> bool:
        return isfile(self._filepath)