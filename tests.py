from unittest import (
    main,
    skip,
    TestCase,
)
from airpress.compressor import PKPass


class PKPassAssetTestCase(TestCase):

    def setUp(self) -> None:
        self.pkpass = PKPass()

    def test_should_add_valid_asset_to_pkpass_using_helper_method(self):
        asset = ('pass.json', b'00001111')
        self.pkpass.add_to_pass_package(asset)

    def test_should_add_valid_asset_to_pkpass_using_magic_method(self):
        self.pkpass['pass.json'] = b'00001111'

    def test_should_retrieve_asset_from_pkpass(self):
        asset_name = 'logo.png'
        asset_content = b'00001111'
        self.pkpass[asset_name] = asset_content

        retrieved_asset = self.pkpass[asset_name]

        self.assertEqual(retrieved_asset, asset_content)

    def test_should_remove_asset_from_pkpass(self):
        asset_name = 'logo.png'
        asset_content = b'11110000'
        self.pkpass[asset_name] = asset_content

        del self.pkpass[asset_name]

        with self.assertRaises(KeyError):
            self.pkpass[asset_name]

    def test_should_raise_assertion_error_for_asset_with_wrong_name_type(self):
        asset = ('pass.json'.encode(), b'11110000')
        with self.assertRaises(AssertionError):
            self.pkpass.add_to_pass_package(asset)

    def test_should_raise_assertion_error_for_asset_with_wrong_content_type(self):
        asset = ('pass.json', object())
        with self.assertRaises(AssertionError):
            self.pkpass.add_to_pass_package(asset)

    def test_should_raise_assertion_error_for_asset_with_empty_content(self):
        asset = ('pass.json', b'')
        with self.assertRaises(AssertionError):
            self.pkpass.add_to_pass_package(asset)

    def test_should_raise_assertion_error_adding_unsupported_asset(self):
        asset = ('unknown.doc', b'11000011')
        with self.assertRaises(AssertionError):
            self.pkpass.add_to_pass_package(asset)

    def test_should_explicitly_add_unsupported_asset(self):
        asset = ('unknown.doc', b'11000011')
        self.pkpass.add_to_pass_package(asset, validate=False)


class PKPassManifestTestCase(TestCase):

    def setUp(self) -> None:
        self.pkpass = PKPass()

    def test_should_raise_assertion_error_calling_manifest_without_mandatory_assets(self):
        with self.assertRaises(AssertionError):
            self.pkpass.manifest_dict

    def test_should_raise_assertion_error_calling_manifest_with_incomplete_pkpass(self):
        self.pkpass.add_to_pass_package(('pass.json', b'11110000'))
        with self.assertRaises(AssertionError):
            self.pkpass.manifest_dict

    def test_should_create_manifest_dictionary(self):
        self.pkpass.add_to_pass_package(
            ('icon.png', b'00001111'),
            ('pass.json', b'11110000')
        )

        expected_manifest_dict = {
            'icon.png': '8c4b5ab6514ff51b44d020b0006746152a53583e',
            'pass.json': 'eec94a882caaf36c8840ff10ed115f63c1d4ab99'
        }

        self.assertIsInstance(self.pkpass.manifest_dict, dict)
        self.assertEqual(expected_manifest_dict, self.pkpass.manifest_dict)

    def test_should_generate_manifest_bytes_object(self):
        self.pkpass.add_to_pass_package(
            ('icon.png', b'00001111'),
            ('pass.json', b'11110000')
        )

        self.assertIsInstance(self.pkpass.manifest, bytes)
        self.assertTrue(self.pkpass.manifest)


class PKPassSignatureTestCase(TestCase):

    def setUp(self) -> None:
        self.pkpass = PKPass(
            ('icon.png', b'00001111'),
            ('pass.json', b'11110000'),
        )

    def test_should_raise_assertion_error_trying_access_signature_of_unsigned_pkpass(self):
        with self.assertRaises(AssertionError):
            self.pkpass.signature

    @skip
    def test_should_sign_pkpass_given_credentials_were_supplied_explicitly(self):
        # TODO test `sign` method passing credentials directly
        self.fail()

    @skip
    def test_should_sign_pkpass_given_credentials_were_supplied_implicitly(self):
        # TODO test `sign` method given credentials were set earlier as attributes
        self.fail()


class PKPassCompressionTestCase(TestCase):

    def setUp(self) -> None:
        pass

    @skip
    def test_should_compress_signed_pass_package_into_pkpass_archive(self):
        # TODO test pass package compression
        self.fail()


if __name__ == '__main__':
    main()
