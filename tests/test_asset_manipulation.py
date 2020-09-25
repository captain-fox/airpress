import pytest


def test_should_add_valid_asset_to_pkpass_using_helper_method(pkpass):
    asset = ('pass.json', b'00001111')
    pkpass.add_to_pass_package(asset)
    assert pkpass['pass.json']


def test_should_add_valid_asset_to_pkpass_using_magic_method(pkpass):
    pkpass['pass.json'] = b'00001111'
    assert pkpass['pass.json']


def test_should_retrieve_asset_from_pkpass(pkpass):
    asset_name = 'logo.png'
    asset_content = b'00001111'
    pkpass[asset_name] = asset_content

    retrieved_asset = pkpass[asset_name]

    assert retrieved_asset == asset_content


def test_should_remove_asset_from_pkpass(pkpass):
    asset_name = 'logo.png'
    asset_content = b'11110000'
    pkpass[asset_name] = asset_content

    del pkpass[asset_name]

    with pytest.raises(KeyError):
        _ = pkpass[asset_name]


def test_should_raise_key_error_removing_non_existing_asset_from_pkpass(pkpass):
    with pytest.raises(KeyError):
        del pkpass['bobbish.xyz']


def test_should_raise_type_error_adding_asset_with_wrong_name_type(pkpass):
    asset = ('pass.json'.encode(), b'11110000')
    with pytest.raises(TypeError):
        pkpass.add_to_pass_package(asset)


def test_should_raise_type_error_adding_asset_with_wrong_content_type(pkpass):
    asset = ('pass.json', object())
    with pytest.raises(TypeError):
        pkpass.add_to_pass_package(asset)


def test_should_raise_value_error_for_asset_with_empty_content(pkpass):
    asset = ('pass.json', b'')
    with pytest.raises(ValueError):
        pkpass.add_to_pass_package(asset)


def test_should_raise_exception_adding_unsupported_asset(pkpass):
    asset = ('unknown.doc', b'11000011')
    with pytest.raises(NameError):
        pkpass.add_to_pass_package(asset)


def test_should_explicitly_add_unsupported_asset(pkpass):
    asset = ('unknown.doc', b'11000011')
    pkpass.add_to_pass_package(asset, validate=False)
