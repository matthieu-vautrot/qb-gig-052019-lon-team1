import pandas as pd
from kernelai.pipeline import node
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal

# unique on unique_participant_id


def get_prm_demographics(df_demographics):
    """
    participants demographics filtered for participant_type = primary participant & case role = victim
    Args:
        df_demographics: raw participants demographics file

    Returns:
        dataframe with demographics information only for victims/ primary participants
    """
    df_demographics = clean_pandas_column_names(df_demographics)
    df_filtered = df_demographics[df_demographics.aft_participant_type == 'Primary Participant'][df_demographics.case_role=='Victim']
    df_filtered = df_filtered.rename(index=str, columns={"alias_name_prefix": 'field_office'})
    return df_filtered


g = PipelineGlobal()


# g.append_node(node(func=get_prm_demographics,
#                    inputs='raw_aftcr_partic_demographics',
#                    outputs='prm_demographics',
#                    name='get_prm_demographics'))
