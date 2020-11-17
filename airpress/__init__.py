__version__ = '1.0.3'

import warnings

from .compressor import PKPass as _PKPass
from .factories import *


class PKPass(_PKPass):

    def __init__(self, *args, **kwargs):
        message = (
            '`PKPass` direct reference will be dropped in version 1.1.0.\nUse `pkpass()` '
            'factory function instead or import `PKPass` from `compressor` module'
        )
        warnings.warn(DeprecationWarning(message))
        super(PKPass, self).__init__(*args, **kwargs)
