import os
import pytest
from airpress.compressor import PKPass


@pytest.fixture
def pkpass():
    return PKPass()


@pytest.fixture
def pkpass_with_assets():
    p = PKPass(
        ("icon.png", b"00001111"),
        ("pass.json", b"11110000"),
    )
    return p


@pytest.fixture
def key():
    with open(
        os.path.join(os.path.dirname(__file__), "credentials/unprotected_dummy_key.pem"),
        "rb",
    ) as k:
        key = k.read()
    return key


@pytest.fixture
def cert():
    with open(
        os.path.join(os.path.dirname(__file__), "credentials/unprotected_dummy_cert.pem"),
        "rb",
    ) as c:
        cert = c.read()
    return cert
