import os

from unittest import TestCase
from airpress.compressor import PKPass


class PKPassCompressionTestCase(TestCase):

    def setUp(self) -> None:
        self.pkpass = PKPass(
            ('icon.png', b'00001111'),
            ('pass.json', b'11110000'),
        )
        with open(
                os.path.join(os.path.dirname(__file__), 'credentials/unprotected_dummy_key.pem'),
                'rb'
        ) as k:
            self.key = k.read()
        with open(
                os.path.join(os.path.dirname(__file__), 'credentials/unprotected_dummy_cert.pem'),
                'rb'
        ) as c:
            self.cert = c.read()

    def test_checks_signed_pass_package_contains_assets_manifest_and_signature(self):
        self.pkpass.sign(cert=self.cert, key=self.key)
        self.assertIn('icon.png', self.pkpass.pass_package)
        self.assertIn('pass.json', self.pkpass.pass_package)
        self.assertIn('manifest.json', self.pkpass.pass_package)
        self.assertIn('signature', self.pkpass.pass_package)

    def test_should_compress_signed_pass_package_into_pkpass_archive(self):
        self.pkpass.sign(cert=self.cert, key=self.key)
        pkpass_archive = bytes(self.pkpass)
        self.assertTrue(pkpass_archive)
        self.assertIs(type(pkpass_archive), bytes)

    def test_should_fail_to_compress_pass_package_if_another_exception_occurs(self):
        with self.assertRaises(Exception):
            _ = bytes(self.pkpass)
