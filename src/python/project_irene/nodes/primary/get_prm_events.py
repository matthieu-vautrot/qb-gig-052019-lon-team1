import pandas as pd
from kernelai.pipeline import node
import numpy as np
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal

# unique on ['unique_participant_id','unique_event_id','unique_note_id','unique_case_id']


def get_prm_events(prm_input_events, int_events, prm_demographics):

    prm_input_events = clean_pandas_column_names(prm_input_events)
    prm_input_events = prm_input_events.drop(columns=['unnamed_0', 'participants'])
    prm_events_sub = prm_input_events[(prm_input_events.unique_contact_id.notnull() |
                                       prm_input_events.unique_participant_id.notnull())]
    prm_events_sub_dedupe = (prm_events_sub.drop_duplicates(
        subset=['unique_case_id', 'unique_note_id', 'unique_event_id', 'unique_contact_id', 'unique_participant_id'],
        keep='first'))
    df_int_events = int_events[(int_events.unique_case_id.notnull()) |
                                 (int_events.unique_participant_id.notnull())]
    df_int_events = df_int_events[(int_events.unique_participant_id != " ")]
    int_events_dedupe = df_int_events.drop_duplicates(keep='first')
    join_events = int_events_dedupe.merge(prm_events_sub_dedupe, how='left',
                                        on=['unique_event_id', 'unique_case_id', 'unique_contact_id',
                                            'unique_participant_id'])
    join_events = (join_events
                   .drop(columns=['alias_name_prefix_y', 'date_of_event_y', 'event_grouping_y', 'event_type_y',
                                  'event_name_y', 'event_status_y'])
                   .rename(index=str, columns={"alias_name_prefix_x": 'field_office'})
                   .rename(index=str, columns={'date_of_event_x': 'date_of_event'})
                   .rename(index=str, columns={'event_grouping_x': 'event_grouping'})
                   .rename(index=str, columns={'event_type_x': 'event_type'})
                   .rename(index=str, columns={'event_name_x': 'event_name'})
                   .rename(index=str, columns={'event_status_x': 'event_status'})
                   )
    prm_demographics_sub = prm_demographics[['unique_case_id', 'unique_participant_id']]
    df_events_demo = join_events.merge(prm_demographics_sub, how='left', on='unique_case_id')
    df_events_demo['unique_participant_id'] = np.where(df_events_demo.unique_participant_id_x.isnull(),
                                             df_events_demo.unique_participant_id_y, df_events_demo.unique_participant_id_x)
    df_events_demo = df_events_demo.drop(columns=['unique_participant_id_y', 'unique_participant_id_x'])
    df_events_demo = df_events_demo.drop_duplicates(keep='first')
    return df_events_demo


g = PipelineGlobal()


# g.append_node(node(func=get_prm_events,
#                    inputs=['prm_input_events', 'int_events', 'prm_demographics'],
#                    outputs='prm_events',
#                    name='get_prm_events'))
