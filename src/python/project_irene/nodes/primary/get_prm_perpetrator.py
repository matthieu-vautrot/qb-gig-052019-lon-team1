import pandas as pd
from kernelai.pipeline import node
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal


def get_prm_perpretators(raw_perpetrators):
    raw_perpetrators = clean_pandas_column_names(raw_perpetrators)
    perpetrators_df = raw_perpetrators[raw_perpetrators.unique_case_id.notnull()]
    perpetrators_df = perpetrators_df.rename(index=str, columns={"alias_name_prefix": 'field_office'})

    return perpetrators_df


g = PipelineGlobal()

# g.append_node(node(func=get_prm_perpretators,
#                    inputs='raw_perpetrators',
#                    outputs='prm_perpretators',
#                    name='get_prm_perpretators'))
