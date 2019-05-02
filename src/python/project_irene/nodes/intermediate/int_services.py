from kernelai.pipeline import node
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal


def int_services(raw_aftcr_partic_service, raw_aftcr_partic_service_new):
    raw_aftcr_partic_service = clean_pandas_column_names(raw_aftcr_partic_service)
    raw_aftcr_partic_service_new = clean_pandas_column_names(raw_aftcr_partic_service_new)
    raw_aftcr_partic_service_new = (raw_aftcr_partic_service_new
                                    .replace(
                                        {'case_type': {'FLT': 'Forced Labor Trafficking', 'BNL': 'Bonded Labor',
                                                       'CSX': 'Commercial Sex Trafficking',
                                                       'OSX': 'Online Sexual Exploitation of Children',
                                                       'CSA': 'Child Sexual Assault',
                                                       'LRV': 'Land Rights Violations',
                                                       'PAP': 'Police Abuse of Power'}
                                         }))
    services_merged = raw_aftcr_partic_service.merge(raw_aftcr_partic_service_new,
                                                     on=list(raw_aftcr_partic_service.columns), how='outer')
    services_merged = services_merged.rename(index=str, columns={
        "unique_participant_id_": "unique_participant_id"})

    return services_merged


g = PipelineGlobal()

# g.append_node(node(func=int_services,
#                    inputs=['raw_aftcr_partic_service', 'raw_aftcr_partic_service_new'],
#                    outputs='int_services',
#                    name='int_services'))
