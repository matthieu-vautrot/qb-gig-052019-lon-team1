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

"""Application entry point
"""

import logging.config
from typing import Any, Dict, Tuple, Optional, Iterable
from os.path import join, basename, curdir, abspath

from kernelai.config import ConfigLoader
from kernelai.io import DataCatalog
from kernelai.pipeline.runner import SequentialRunner

from project_irene.pipeline import create_pipeline
from project_irene.catalog_irene import get_catalog_irene


# Name of root directory containing project configuration.
CONF_ROOT = "conf"


# Configuration environment to be used for running the pipelines.
# Change this constant value if you want to load configuration
# from from a different location.
RUN_ENV = "local"


def init_context(proj_dir: str) -> Tuple[ConfigLoader,
                                         DataCatalog,
                                         Dict[str, Any]]:
    """
    Loads KernelAI's context: the ``ConfigLoader``, the ``DataCatalog``
        and the parameters.

    Args:
        proj_dir (str): The root directory of the KernelAI project

    Returns:
        Tuple[ConfigLoader, DataCatalog, dict]: ConfigLoader instance,
            DataCatalog defined in `catalog.yml`
            and the parameters dictionary from `parameters.yml`

    """

    conf_paths = [join(proj_dir, CONF_ROOT, "base"),
                  join(proj_dir, CONF_ROOT, RUN_ENV)]
    conf = ConfigLoader(conf_paths)

    conf_logging = conf.get("logging*", "logging*/**")
    conf_catalog = conf.get("catalog*", "catalog*/**",
                            "catalog_primary*", "catalog_primary*/**")
    conf_params = conf.get("parameters*", "parameters*/**")

    logging.config.dictConfig(conf_logging)
    io = DataCatalog.from_config(conf_catalog)

    return conf, io, conf_params


def main(pipeline_tags: Optional[Iterable[str]] = None,
         run_pipeline: Optional[bool] = True):
    """
    Application main entry point.

    Args:
        pipeline_tags: An optional list of node tags which should be used to
            filter the nodes of the ``Pipeline``. If specified, only the nodes
            containing *any* of these tags will be added to the ``Pipeline``.
        run_pipeline: An optional boolean flag that indicates whether the
            constructed ``Pipeline`` needs to be run.

    """
    # Load KernelAI context (io, parameters)
    _, io, parameters = init_context(curdir)

    # Report project name
    logging.info("** KernelAI project {}".format(basename(abspath(curdir))))

    # Load and run the pipelines
    pipeline_tags = pipeline_tags or []
    pipeline = create_pipeline(*pipeline_tags)
    print(pipeline.describe())
    pipeline.log_pipeline_to_json()
    if run_pipeline:
        feed_dict = {"parameters": parameters}
        SequentialRunner().run(pipeline, io, feed_dict=feed_dict)


if __name__ == '__main__':
    main()
