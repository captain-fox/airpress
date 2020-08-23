import pytest


def test_checks_signed_pass_package_contains_assets_manifest_and_signature(
        pkpass_with_assets, cert, key
):
    pkpass_with_assets.sign(cert=cert, key=key)
    assert 'icon.png' in pkpass_with_assets.pass_package
    assert 'pass.json' in pkpass_with_assets.pass_package
    assert 'manifest.json' in pkpass_with_assets.pass_package
    assert 'signature' in pkpass_with_assets.pass_package


def test_should_compress_signed_pass_package_into_pkpass_archive_using_bytes_method(
        pkpass_with_assets, cert, key
):
    pkpass_with_assets.sign(cert=cert, key=key)
    pkpass_archive = bytes(pkpass_with_assets)
    assert pkpass_archive
    assert type(pkpass_archive) is bytes


def test_should_compress_signed_pass_package_into_pkpass_archive_as_callable(
        pkpass_with_assets, cert, key
):
    pkpass_with_assets.sign(cert=cert, key=key)
    pkpass_archive = pkpass_with_assets()
    assert pkpass_archive
    assert type(pkpass_archive) is bytes


def test_should_fail_to_compress_pass_package_if_another_exception_occurs(pkpass_with_assets):
    with pytest.raises(Exception):
        _ = bytes(pkpass_with_assets)
