from kernelai.pipeline import node
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal

# UNIQUE on ['unique_participant_id', 'unique_service_id']


def get_prm_services(raw_grp_service_grouping, int_aftcr_partic_service):
    raw_grp_service_grouping = clean_pandas_column_names(raw_grp_service_grouping)
    grp_services_dedupe = raw_grp_service_grouping.sort_values('new_service').drop(
        columns=['new_service', 'msc_timeframe', 'consolidated_service_team_analysis']).drop_duplicates(
        ['aftercare_service', 'domain_of_care'], keep='last')
    services_grouped = int_aftcr_partic_service.merge(grp_services_dedupe, on=['domain_of_care', 'aftercare_service'],
                                                      how='left')
    services_grouped = services_grouped.rename(index=str, columns={"alias_name_prefix": 'field_office'})

    return services_grouped


g = PipelineGlobal()

# g.append_node(node(func=get_prm_services,
#                    inputs=['raw_grp_service_grouping', 'int_services'],
#                    outputs='prm_services',
#                    name='get_prm_services'))

