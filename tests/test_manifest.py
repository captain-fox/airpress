import pytest


def test_should_raise_key_error_calling_manifest_without_mandatory_assets(pkpass):
    with pytest.raises(KeyError):
        _ = pkpass.manifest_dict


def test_should_raise_key_error_calling_manifest_with_incomplete_pkpass(pkpass):
    pkpass.add_to_pass_package(('pass.json', b'11110000'))
    with pytest.raises(KeyError):
        _ = pkpass.manifest_dict


def test_should_create_manifest_dictionary(pkpass):
    pkpass.add_to_pass_package(
        ('icon.png', b'00001111'),
        ('pass.json', b'11110000')
    )

    expected_manifest_dict = {
        'icon.png': '8c4b5ab6514ff51b44d020b0006746152a53583e',
        'pass.json': 'eec94a882caaf36c8840ff10ed115f63c1d4ab99'
    }

    assert isinstance(pkpass.manifest_dict, dict)
    assert pkpass.manifest_dict == expected_manifest_dict


def test_should_generate_non_empty_manifest_bytes_object(pkpass):
    pkpass.add_to_pass_package(
        ('icon.png', b'00001111'),
        ('pass.json', b'11110000')
    )
    expected_manifest_bytes = (b'{\n    "icon.png":"8c4b5ab6514ff51b44d020b0006746152a53583e",'
                               b'\n    "pass.json":"eec94a882caaf36c8840ff10ed115f63c1d4ab99"\n}')

    assert isinstance(pkpass.manifest, bytes)
    assert pkpass.manifest == expected_manifest_bytes
