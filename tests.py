from unittest import (
    main,
    skip,
    TestCase,
)
from airpress.compressor import PKPass


class PKPassInitializerTestCase(TestCase):

    def test_should_initialize_pkpass_without_assets(self):
        pkpass = PKPass()
        self.assertTrue(pkpass)

    def test_should_initialize_pkpass_with_assets(self):
        pkpass = PKPass(
            ('icon.png', b'00001111'),
            ('pass.json', b'11110000'),
        )
        self.assertTrue(pkpass['icon.png'])
        self.assertTrue(pkpass['pass.json'])

    def test_should_raise_type_error_during_initialization_with_invalid_assets(self):
        with self.assertRaises(TypeError):
            _ = PKPass(
                ('pass.json', object())
            )

    def test_should_raise_assertion_error_during_initialization_with_unsupported_asset(self):
        with self.assertRaises(AssertionError):
            _ = PKPass(
                ('unknown.doc', b'11001100')
            )

    def test_should_explicitly_initialize_pkpass_with_unsupported_asset(self):
        pkpass = PKPass(
            ('unknown.doc', b'11001100'),
            validate=False
        )
        self.assertTrue(pkpass['unknown.doc'])


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
            _ = self.pkpass[asset_name]

    def test_should_raise_key_error_removing_non_existing_asset_from_pkpass(self):
        with self.assertRaises(KeyError):
            del self.pkpass['bobbish.xyz']

    def test_should_raise_type_error_adding_asset_with_wrong_name_type(self):
        asset = ('pass.json'.encode(), b'11110000')
        with self.assertRaises(TypeError):
            self.pkpass.add_to_pass_package(asset)

    def test_should_raise_type_error_adding_asset_with_wrong_content_type(self):
        asset = ('pass.json', object())
        with self.assertRaises(TypeError):
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
            _ = self.pkpass.manifest_dict

    def test_should_raise_assertion_error_calling_manifest_with_incomplete_pkpass(self):
        self.pkpass.add_to_pass_package(('pass.json', b'11110000'))
        with self.assertRaises(AssertionError):
            _ = self.pkpass.manifest_dict

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

    def test_should_generate_non_empty_manifest_bytes_object(self):
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

    def test_should_raise_attribute_error_trying_to_access_signature_of_unsigned_pkpass(self):
        with self.assertRaises(AttributeError):
            _ = self.pkpass.signature

    def test_should_raise_assertion_error_if_credentials_were_not_supplied(self):
        with self.assertRaises(AssertionError):
            _ = self.pkpass.sign()

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
        self.pkpass = PKPass(
            ('icon.png', b'00001111'),
            ('pass.json', b'11110000'),
        )

    @skip
    def test_should_compress_signed_pass_package_into_pkpass_archive(self):
        # TODO test pass package compression
        self.fail()


if __name__ == '__main__':
    main()
