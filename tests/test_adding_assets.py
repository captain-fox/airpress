from unittest import TestCase
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
