import pytest
from airpress.compressor import PKPass


def test_should_initialize_pkpass_without_assets():
    pkpass = PKPass()
    assert len(pkpass) == 0


def test_should_initialize_pkpass_with_assets():
    pkpass = PKPass(
        ('icon.png', b'00001111'),
        ('pass.json', b'11110000'),
    )
    assert pkpass['icon.png']
    assert pkpass['pass.json']


def test_should_raise_type_error_during_initialization_with_assets_of_wrong_type():
    with pytest.raises(TypeError):
        _ = PKPass(
            ('pass.json', object())
        )


def test_should_raise_assertion_error_during_initialization_with_unsupported_asset():
    with pytest.raises(AssertionError):
        _ = PKPass(
            ('unknown.doc', b'11001100')
        )


def test_should_explicitly_initialize_pkpass_with_unsupported_asset():
    pkpass = PKPass(
        ('unknown.doc', b'11001100'),
        validate=False
    )
    assert pkpass['unknown.doc']
