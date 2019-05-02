import pandas as pd
from kernelai.pipeline import node
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal

# unique on ['unique_participant_id', 'aso_subdomain_points', 'data_collection_point']


def get_prm_aso(raw_aftcr_partic_aso_assmt, raw_aftcr_partic_aso_assmt_2018, raw_aftcr_partic_aso_domain,
            raw_aftcr_partic_aso_domain_2018):
    """
    Combine raw ASO assessment and ASO domain files together
    Args:
        raw_aso_assmnt (pandas dataframe): raw aso assessment file
        raw_aso_assmnt_2018 (pandas dataframe): raw aso assessment 2018 file
        raw_aso_domain (pandas dataframe): raw aso domain scores file
        raw_aso_domain_2018 (pandas dataframe): raw aso domain scores 2018 file

    Returns:
        pandas dataframe : dataframe with aso scores for assessment and domain for each participant.
        Domains are cleaned from raw file to have only 7 domains.
        Each record is unique on [unique_participant_id, aso_subdomain_points, data_collection_point]
    """

    raw_aftcr_partic_aso_assmt = clean_pandas_column_names(raw_aftcr_partic_aso_assmt)
    raw_aftcr_partic_aso_domain = clean_pandas_column_names(raw_aftcr_partic_aso_domain)
    raw_aftcr_partic_aso_assmt_2018 = clean_pandas_column_names(raw_aftcr_partic_aso_assmt_2018)
    raw_aftcr_partic_aso_domain_2018 = clean_pandas_column_names(raw_aftcr_partic_aso_domain_2018)

    raw_aftcr_partic_aso_assmt = raw_aftcr_partic_aso_assmt.rename(index=str, columns={
        "unique_participant_id_": "unique_participant_id"})
    raw_aftcr_partic_aso_assmt_2018 = raw_aftcr_partic_aso_assmt_2018.rename(index=str, columns={
        "unique_participant_id_": "unique_participant_id"})
    assmnt_union = raw_aftcr_partic_aso_assmt_2018.append(raw_aftcr_partic_aso_assmt)
    domain_union = raw_aftcr_partic_aso_domain_2018.append(raw_aftcr_partic_aso_domain)

    aso_assmt = assmnt_union.sort_values("assessment_date", ascending=False).drop_duplicates(
        ['unique_participant_id', 'data_collection_point'], keep='first')

    domain_union_modif = (domain_union
                          .replace({'domain_of_care': ['Community Involvement', 'Community Support', 'Support System']},
                                   'Social Support')
                          .replace({'domain_of_care': ['Economic Empowerment & Education', 'Education']},
                                   'Economic Empowerment and Education')
                          .replace({'domain_of_care': ['Mental Wellbeing & Trauma Recovery']}, 'Mental Wellbeing')
                          .replace({'domain_of_care': ['Legal Protection', 'Safety']}, 'Protection')
                          )
    df_assmnt_domain_merged = pd.merge(aso_assmt, domain_union_modif, how='left', on='unique_aso_id')
    df_assmnt_domain_merged = df_assmnt_domain_merged.drop(
        columns=['case_type_y', 'unique_case_id_y', 'unique_participant_id_y'])
    df_assmnt_domain_merged = df_assmnt_domain_merged.rename(index=str, columns={"case_type_x": "case_type",
                                                                                 "unique_case_id_x": "unique_case_id",
                                                                                 "unique_participant_id_x": "unique_participant_id"
                                                                                 })
    df_assmnt_domain_merged = df_assmnt_domain_merged.drop_duplicates(keep='first')
    df_assmnt_domain_merged = df_assmnt_domain_merged.drop(columns=['alias_name_prefix'])

    return df_assmnt_domain_merged


g = PipelineGlobal()

# g.append_node(node(func=get_prm_aso,
#                    inputs=['raw_aftcr_partic_aso_assmt', 'raw_aftcr_partic_aso_assmt_2018',
#                             'raw_aftcr_partic_aso_domain', 'raw_aftcr_partic_aso_domain_2018'],
#                    outputs='prm_aso',
#                    name='get_prm_aso'))
