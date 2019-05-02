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
"""Pipeline construction"""

from kernelai.pipeline import Pipeline, node
from project_irene.pipeline_global import *
from project_irene.nodes import *

# Here you can define your data-driven pipelines by importing your functions
# and adding them to the pipelines as follows:
#
# from nodes.data_wrangling import clean_data, compute_features
#
# pipelines = Pipeline([
#     node(clean_data, 'customers', 'prepared_customers'),
#     node(compute_features, 'prepared_customers', ['X_train', 'Y_train'])
# ])
#
# Once you have your pipelines defined, you can run it from the root of your
# project by calling:
#
# $ kernelai run
#

from .nodes.example import split_data, train_model, predict, report_accuracy


def create_pipeline(*tags: str):
    """
    Create the project's pipelines. If ``tags`` argument is provided, the
        resulting ``Pipeline`` will only contain the nodes that have *any* of
        the tags specified.

    Args:
        *tags: A list of node tags which should be used to filter
            the nodes of the new ``Pipeline``. If specified, only the nodes
            containing *any* of these tags will be added to the ``Pipeline``.

    Raises:
        ValueError: If ``tags`` were provided and the resulting pipelines is
            empty.

    Returns:
        Pipeline: The resulting pipelines.
    """
    ###########################################################################
    # Here you can find an example pipelines with 4 nodes.
    #
    # PLEASE DELETE THIS PIPELINE ONCE YOU START WORKING ON YOUR OWN PROJECT AS
    # WELL AS THE FILE nodes/example.py
    # -------------------------------------------------------------------------
    g = PipelineGlobal()

    irene_pipeline = Pipeline([
        *g.nodes,
    ])

    ###########################################################################

    # if tags:
    #     pipeline = Pipeline([])
    #     for tag in tags:
    #         pipeline += irene_pipeline.only_nodes_with_tags(tag)
    #     if not pipeline.nodes:
    #         raise ValueError("Not found any nodes having any of the following "
    #                          "tags attached: {}".format(", ".join(tags)))
    # else:
    #     pipeline = irene_pipeline

    return irene_pipeline
