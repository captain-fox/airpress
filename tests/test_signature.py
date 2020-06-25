import pytest


def test_should_raise_attribute_error_trying_to_access_signature_of_unsigned_pkpass(pkpass_with_assets):
    with pytest.raises(AttributeError):
        _ = pkpass_with_assets.signature


def test_should_raise_assertion_error_trying_to_sign_pkpass_without_credentials(pkpass_with_assets):
    with pytest.raises(AssertionError):
        pkpass_with_assets.sign()


def test_should_raise_assertion_error_trying_to_sign_pkpass_without_certificate(pkpass_with_assets, key):
    with pytest.raises(AssertionError):
        pkpass_with_assets.sign(key=key)


def test_should_raise_assertion_error_trying_to_sign_pkpass_without_key(pkpass_with_assets, cert):
    with pytest.raises(AssertionError):
        pkpass_with_assets.sign(key=cert)


def test_should_raise_assertion_error_trying_to_sign_pkpass_without_wwdr_cert(pkpass_with_assets, cert, key):
    with pytest.raises(AssertionError):
        pkpass_with_assets.sign(cert=cert, key=key, wwdr=None)


def test_sign_method_returns_signature_as_bytes_object(pkpass_with_assets, cert, key):
    signature = pkpass_with_assets.sign(cert=cert, key=key)
    assert signature
    assert type(signature) is bytes


def test_should_sign_pkpass_with_credentials_supplied_explicitly(pkpass_with_assets, cert, key):
    pkpass_with_assets.sign(cert=cert, key=key)
    assert pkpass_with_assets.signature


def test_should_sign_pkpass_with_credentials_supplied_implicitly(pkpass_with_assets, cert, key):
    pkpass_with_assets.cert = cert
    pkpass_with_assets.key = key

    pkpass_with_assets.sign()

    assert pkpass_with_assets.signature


def test_should_reset_signature_if_asset_was_added_after_signing(pkpass_with_assets, cert, key):
    pkpass_with_assets.cert = cert
    pkpass_with_assets.key = key
    pkpass_with_assets.sign()

    pkpass_with_assets['icon@2x.png'] = b'11000011'

    with pytest.raises(AttributeError):
        _ = pkpass_with_assets.signature


def test_should_reset_signature_if_asset_was_removed_after_signing(pkpass_with_assets, cert, key):
    pkpass_with_assets['icon@2x.png'] = b'11000011'
    pkpass_with_assets.cert = cert
    pkpass_with_assets.key = key
    pkpass_with_assets.sign()

    del pkpass_with_assets['icon@2x.png']

    with pytest.raises(AttributeError):
        _ = pkpass_with_assets.signature
