from .compressor import PKPass

__all__ = ['pkpass']


def pkpass(*assets, validate: bool = True, **kwargs):
    return PKPass(*assets, validate=validate, **kwargs)
