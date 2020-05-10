# pylint: disable=protected-access, invalid-name, too-many-locals
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.bindings.openssl.binding import Binding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

copenssl = Binding.lib
cffi = Binding.ffi


# SMIME isn't supported by pyca/cryptography:
# https://github.com/pyca/cryptography/issues/1621
def pkcs7_sign(certcontent: bytes,
               keycontent: bytes,
               wwdr_certificate: bytes,
               data: bytes,
               key_password=None,
               flag=copenssl.PKCS7_BINARY | copenssl.PKCS7_DETACHED):

    """
    Sign data with PKCS#7.
    :param certcontent: (bytes) Content of pem file certificate
    :param keycontent: (bytes) Content of key file
    :param wwdr_certificate: (bytes) Content of Intermediate cert file
    :param data: (bytes) Data to be signed
    :param key_password: (bytes, optional) key file passwd. Defaults to None.
    :param flag: (int, optional) Flags to be passed to PKCS7_sign C lib.
    Defaults to copenssl.PKCS7_BINARY|copenssl.PKCS7_DETACHED.
    :return: pkcs7 signature of data
    """

    backend = default_backend()

    # Load cert and key
    pkey = load_pem_private_key(keycontent, key_password, backend=backend)
    cert = x509.load_pem_x509_certificate(certcontent, backend=backend)

    # Load intermediate cert and push it into < Cryptography_STACK_OF_X509 * >
    intermediate_cert = x509.load_der_x509_certificate(
        wwdr_certificate,
        backend,
    )
    certs_stack = copenssl.sk_X509_new_null()
    # https://www.openssl.org/docs/man1.1.1/man3/sk_TYPE_push.html
    # int sk_TYPE_push(STACK_OF(TYPE) *sk, const TYPE *ptr);
    # return amount of certs into certs_stack, -1 on error
    _count = copenssl.sk_X509_push(certs_stack, intermediate_cert._x509)

    bio = backend._bytes_to_bio(data)
    # From
    # pyca/cryptography/src/_cffi_src/openssl/pkcs7.py
    # PKCS7 *PKCS7_sign(X509 *, EVP_PKEY *, Cryptography_STACK_OF_X509 *, BIO *, int);
    # signing-time attr is automatically added:
    # https://www.openssl.org/docs/man1.1.1/man3/PKCS7_sign.html
    pkcs7 = copenssl.PKCS7_sign(
        cert._x509,
        pkey._evp_pkey,
        certs_stack,
        bio.bio,
        flag,
    )

    bio_out = backend._create_mem_bio_gc()
    copenssl.i2d_PKCS7_bio(bio_out, pkcs7)

    signed_pkcs7 = backend._read_mem_bio(bio_out)
    return signed_pkcs7
