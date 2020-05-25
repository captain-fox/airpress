import os

from unittest import TestCase
from airpress.compressor import PKPass


class PKPassSignatureTestCase(TestCase):

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

    def test_should_raise_attribute_error_trying_to_access_signature_of_unsigned_pkpass(self):
        with self.assertRaises(AttributeError):
            _ = self.pkpass.signature

    def test_should_raise_assertion_error_trying_to_sign_pkpass_without_credentials(self):
        with self.assertRaises(AssertionError):
            self.pkpass.sign()

    def test_should_raise_assertion_error_trying_to_sign_pkpass_without_certificate(self):
        with self.assertRaises(AssertionError):
            self.pkpass.sign(key=self.key)

    def test_should_raise_assertion_error_trying_to_sign_pkpass_without_key(self):
        with self.assertRaises(AssertionError):
            self.pkpass.sign(key=self.cert)

    def test_should_raise_assertion_error_trying_to_sign_pkpass_without_wwdr_certificate(self):
        with self.assertRaises(AssertionError):
            self.pkpass.sign(wwdr=b'')

    def test_sign_method_returns_signature_as_bytes_object(self):
        signature = self.pkpass.sign(cert=self.cert, key=self.key)
        self.assertTrue(signature)
        self.assertIs(type(signature), bytes)

    def test_should_sign_pkpass_with_credentials_supplied_explicitly(self):
        self.pkpass.sign(cert=self.cert, key=self.key)
        self.assertTrue(self.pkpass.signature)

    def test_should_sign_pkpass_with_credentials_supplied_implicitly(self):
        self.pkpass.cert = self.cert
        self.pkpass.key = self.key

        self.pkpass.sign()

        self.assertTrue(self.pkpass.signature)

    def test_should_reset_signature_if_asset_was_added_after_signing(self):
        self.pkpass.cert = self.cert
        self.pkpass.key = self.key
        self.pkpass.sign()

        self.pkpass['icon@2x.png'] = b'11000011'

        with self.assertRaises(AttributeError):
            _ = self.pkpass.signature

    def test_should_reset_signature_if_asset_was_removed_after_signing(self):
        self.pkpass['icon@2x.png'] = b'11000011'
        self.pkpass.cert = self.cert
        self.pkpass.key = self.key
        self.pkpass.sign()

        del self.pkpass['icon@2x.png']

        with self.assertRaises(AttributeError):
            _ = self.pkpass.signature
