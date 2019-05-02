from kernelai.pipeline import node
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal


def get_ft_events(prm_events):
    int_events = prm_events.replace({'domain_of_care': ['Mental Wellbeing & Trauma Recovery']}, 'Mental Wellbeing')
    int_events_agg = int_events.pivot_table(values='unique_event_id', index=['unique_participant_id'],
                                            columns=['domain_of_care'], aggfunc='count').reset_index()
    int_events_agg = (int_events_agg
                      .rename(index=str, columns={'Economic Empowerment & Education':
                                                  'economic_empowerment_and_education_events_count'})
                      .rename(index=str, columns={'Health': 'health_events_count'})
                      .rename(index=str, columns={'Housing': 'housing_events_count'})
                      .rename(index=str, columns={'Mental Wellbeing': 'mental_wellbeing_events_count'})
                      .rename(index=str, columns={'Protection': 'protection_events_count'})
                      .rename(index=str, columns={'Support System': 'support_system_events_count'})
                      )
    int_events_agg = int_events_agg.drop(columns=['Program Management', 'Other'])

    return int_events_agg


g = PipelineGlobal()

g.append_node(node(func=get_ft_events,
                   inputs='prm_events',
                   outputs='ft_events',
                   name='get_ft_events'))
