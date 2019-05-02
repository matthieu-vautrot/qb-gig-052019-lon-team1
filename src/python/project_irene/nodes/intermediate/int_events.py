from kernelai.pipeline import node
from project_irene.de_utils.utils import *
import numpy as np
from project_irene.pipeline_global import PipelineGlobal


def int_events(raw_events_grouping, raw_aftcr_event):
    raw_aftcr_event = clean_pandas_column_names(raw_aftcr_event)
    raw_events_grouping = clean_pandas_column_names(raw_events_grouping)
    events_grouping_dedupe = raw_events_grouping.drop(
        raw_events_grouping[(raw_events_grouping.event_type == 'Aftercare: Follow up in home of origin') &
                            (raw_events_grouping.event_grouping == 'Service Events') &
                            (raw_events_grouping.domain_of_care == 'Protection')
                            ].index)
    events_grouping_dedupe = events_grouping_dedupe.drop(events_grouping_dedupe[(events_grouping_dedupe.event_type ==
                                                                                 'Aftercare: Support for transition to community') &
                                                                                (events_grouping_dedupe.event_grouping == 'Service Events') &
                                                                                (events_grouping_dedupe.domain_of_care == 'Support System')].index)
    events_grouping_dedupe = events_grouping_dedupe.drop(events_grouping_dedupe[(events_grouping_dedupe.event_type == 'Aftercare: Home Visit') &
                                                                                (events_grouping_dedupe.event_grouping == 'Service Events') &
                                                                                (events_grouping_dedupe.domain_of_care == 'Protection')].index)
    events_grouping_dedupe = events_grouping_dedupe.drop(events_grouping_dedupe[(events_grouping_dedupe.event_type == 'Aftercare: Group Session') &
                                                                                (events_grouping_dedupe.event_grouping == 'Service Events') &
                                                                                (events_grouping_dedupe.domain_of_care == 'Mental Wellbeing & Trauma Recovery')].index)
    raw_aftcr_event['event_type_lower'] = raw_aftcr_event['event_type'].str.lower()
    raw_aftcr_event['event_grouping_lower'] = raw_aftcr_event['event_grouping'].str.lower()
    events_grouping_dedupe['event_type_lower'] = events_grouping_dedupe['event_type'].str.lower()
    events_grouping_dedupe['event_grouping_lower'] = events_grouping_dedupe['event_grouping'].str.lower()
    event_merge = raw_aftcr_event.merge(events_grouping_dedupe, on=['event_type_lower', 'event_grouping_lower'], how='left')
    event_merge = (event_merge
                   .drop(columns=['event_grouping_y', 'event_type_y', 'event_type_lower', 'event_grouping_lower'])
                   .rename(index=str,  columns={'event_grouping_x': 'event_grouping', 'event_type_x': 'event_type'}))
    event_merge['event_supertype'] = np.where(event_merge.event_supertype.isnull(), event_merge.event_grouping,
                                              event_merge.event_supertype)
    return event_merge


g = PipelineGlobal()

#
# g.append_node(node(func=int_events,
#                    inputs=['raw_grp_event_type_mapping', 'raw_aftcr_event'],
#                    outputs='int_events',
#                    name='int_events'))

