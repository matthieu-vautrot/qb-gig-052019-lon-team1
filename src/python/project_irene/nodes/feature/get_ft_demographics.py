from kernelai.pipeline import node
from project_irene.de_utils.utils import *
from project_irene.pipeline_global import PipelineGlobal


def get_ft_demographics(prm_demographics):
    prm_demographics = clean_pandas_column_names(prm_demographics)

    return prm_demographics


g = PipelineGlobal()

g.append_node(node(func=get_ft_demographics,
                   inputs='prm_demographics',
                   outputs='ft_demographics',
                   name='get_ft_demographics'))

