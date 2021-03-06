from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy

__all__ = ['build_metric']


def build_metric(config):
    from .det_metric import DetMetric
    from .rec_metric import RecMetric
    from .cls_metric import ClsMetric
    from .e2e_metric import E2EMetric

    support_dict = ['DetMetric', 'RecMetric', 'ClsMetric', 'E2EMetric']

    config = copy.deepcopy(config)
    module_name = config.pop('name')
    assert module_name in support_dict, Exception(
        'metric only support {}'.format(support_dict))
    module_class = eval(module_name)(**config)
    return module_class
