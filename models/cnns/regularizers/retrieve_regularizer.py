from typing import Dict
from models.cnns.regularizers.tdv.tdv import TDVRegularizer
from models.cnns.regularizers.tnrd.tnrd import TNRDRegularizer
from models.cnns.regularizers.tv.tv import TVRegularizer
from models.cnns.regularizers.dncnn.dncnn import DnCNNRegularizer


def retrieve_regularizer(config: Dict):
    """Retrieves regularizer model based on name

    Parameters
    ----------
    config: (Dict) - Full configuration for regularizer with name key

    Returns
    -------
    Regularizer keras model

    """
    if config['name'] == 'TV':
        return TVRegularizer(config)
    elif config['name'] == 'TNRD':
        return TNRDRegularizer(config)
    elif config['name'] == 'TDV':
        return TDVRegularizer(config)
    elif config['name'] == 'DnCNN':
        return DnCNNRegularizer(config)
    else:
        raise NotImplementedError