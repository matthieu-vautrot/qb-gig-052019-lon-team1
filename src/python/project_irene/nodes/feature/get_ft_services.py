from kernelai.pipeline import node
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal


def get_ft_services(prm_services):
    prm_services = prm_services.replace({'domain_of_care': ['Mental Wellbeing & Trauma Recovery']}, 'Mental Wellbeing')
    prm_services_agg = prm_services.pivot_table(values='aftercare_service', index=['unique_participant_id'],
                                                columns=['domain_of_care'], aggfunc='count').reset_index()
    prm_services_agg = (prm_services_agg
                        .rename(index=str, columns={'Economic Empowerment & Education':
                                                        'economic_empowerment_and_education_services_count'})
                        .rename(index=str, columns={'Health': 'health_services_count'})
                        .rename(index=str, columns={'Housing': 'housing_services_count'})
                        .rename(index=str, columns={'Mental Wellbeing': 'mental_wellbeing_services_count'})
                        .rename(index=str, columns={'Protection': 'protection_services_count'})
                        .rename(index=str, columns={'Support System': 'support_system_services_count'})
                        )
    prm_services_agg = prm_services_agg.drop(columns=['Program Management', 'Other'])
    return prm_services_agg


g = PipelineGlobal()

g.append_node(node(func=get_ft_services,
                   inputs='prm_services',
                   outputs='ft_services',
                   name='get_ft_services'))
