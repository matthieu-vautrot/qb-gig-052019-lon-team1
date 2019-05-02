from kernelai.pipeline import node
import pandas as pd
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal


def _closure_func(row):
    if row["case_type"] == "Forced Labor Trafficking":
        return row['closure_456d_aftercare_initiated_date']
    elif row["case_type"] == "Land Rights Violations":
        return row['closure_1278d_aftercare_initiated_date']
    elif row["case_type"] == "CSA":
        return row['closure_1460d_aftercare_initiated_date']
    elif ((row["case_type"] == "Bonded Labor") | (row["case_type"] == "CSX") | (row["case_type"] == "OSEC") | (
            row["case_type"] == "Police Abuse of Power")):
        return row['closure_912d_aftercare_initiated_date']
    return row['closure_912d_aftercare_initiated_date']


def assign_cluster(row):
    if (row["closure_aftercare_initiated_date"] >= 0) and (pd.isnull(row["cluster"])):
        if row["case_type"] == "Forced Labor Trafficking":
            return 'flt_na'
        elif row["case_type"] == "Land Rights Violations":
            return 'lrv_na'
        elif row["case_type"] == "CSA":
            return 'csa_na'
        elif row["case_type"] == "Bonded Labor":
            return 'bl_na'
        elif row["case_type"] == "CSX":
            return 'csx_na'
        elif row["case_type"] == "OSEC":
            return 'osec_na'
        else:
            return 'pap_na'
    else:
        return row['cluster']


def get_model_input(ft_demographics, ft_services, ft_events, ft_aso, ft_clo_912d_AI,
                    ft_clo_456d_AI, ft_clo_1278d_AI, ft_clo_1460d_AI, ft_journey_clusters, prm_target):
    ft_aso = clean_pandas_column_names(ft_aso)
    ft_clo_456d_AI = clean_pandas_column_names(ft_clo_456d_AI)
    ft_clo_912d_AI = clean_pandas_column_names(ft_clo_912d_AI)
    ft_clo_1278d_AI = clean_pandas_column_names(ft_clo_1278d_AI)
    ft_clo_1460d_AI = clean_pandas_column_names(ft_clo_1460d_AI)
    df_closure = (ft_demographics
                  .merge(ft_clo_456d_AI, on='unique_participant_id', how='left')
                  .merge(ft_clo_912d_AI, on='unique_participant_id', how='left')
                  .merge(ft_clo_1278d_AI, on='unique_participant_id', how='left')
                  .merge(ft_clo_1460d_AI, on='unique_participant_id', how='left')
                  )
    df_closure['closure_aftercare_initiated_date'] = df_closure.apply(_closure_func, axis=1)
    df_closure_sub = df_closure.query('case_type!="Other"')
    df_closure_sub = df_closure_sub.drop(
        columns=['closure_456d_aftercare_initiated_date', 'closure_912d_aftercare_initiated_date',
                 'closure_1278d_aftercare_initiated_date', 'closure_1460d_aftercare_initiated_date'])
    df_closure_aso = df_closure_sub.merge(ft_aso, on='unique_participant_id', how='left')

    df_clo_aso_serv = df_closure_aso.merge(ft_services, on='unique_participant_id', how='left')

    df_clo_aso_serv_event = df_clo_aso_serv.merge(ft_events, on='unique_participant_id', how='left')

    ft_journey_clusters = clean_pandas_column_names(ft_journey_clusters)
    df_clo_aso_serv_event_clus = df_clo_aso_serv_event.merge(ft_journey_clusters, on='unique_participant_id',
                                                             how='left')
    df_clo_aso_serv_event_clus['cluster_new'] = df_clo_aso_serv_event_clus.apply(assign_cluster, axis=1)
    df_clo_aso_serv_event_clus = df_clo_aso_serv_event_clus.drop(columns=['cluster']).rename(index=str, columns={
        'cluster_new': 'cluster'})
    df_clo_aso_serv_event_clus['target'] = df_clo_aso_serv_event_clus['closure_aftercare_initiated_date']
    df_clo_aso_serv_event_clus = df_clo_aso_serv_event_clus.drop(columns=['closure_aftercare_initiated_date',
                                                                          'education', 'case_role',
                                                                          'aft_participant_type',
                                                                          'avg_documented_ownership_score_intake',
                                                                          'avg_savings_score_intake'])
    df_clo_aso_serv_event_clus = (df_clo_aso_serv_event_clus.rename(index=str,
                                                                    columns={'alias_name_prefix': 'field_office',
                                                                             'vr_date': 'victim_relief_date',
                                                                             'cluster': 'journey_cluster'}))

    col_list = list(df_clo_aso_serv_event_clus.columns)
    col_list.pop(col_list.index('unique_participant_id'))
    df_clo_aso_serv_event_clus = df_clo_aso_serv_event_clus[['unique_participant_id'] + col_list]
    prm_target = prm_target.drop(columns=['Unnamed: 0'])

    model_input = df_clo_aso_serv_event_clus.merge(prm_target, on='unique_participant_id', how='left')
    model_input = model_input.drop(columns=['target'])

    return model_input


g = PipelineGlobal()

g.append_node(node(func=get_model_input,
                   inputs=['ft_demographics', 'ft_services', 'ft_events', 'ft_aso', 'ft_clo_912d_AI',
                           'ft_clo_456d_AI', 'ft_clo_1278d_AI', 'ft_clo_1460d_AI', 'ft_journey_clusters',
                           'prm_target'],
                   outputs='model_input',
                   name='get_model_input'))



