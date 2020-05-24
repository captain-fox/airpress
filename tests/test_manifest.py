from unittest import TestCase
from airpress.compressor import PKPass


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
