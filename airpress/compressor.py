import io
import json
import zipfile
from hashlib import sha1

from .crypto import pkcs7_sign

WWDR_CA = b'0\x82\x04"0\x82\x03\n\xa0\x03\x02\x01\x02\x02\x08\x01\xde\xbc\xc49m\xa0\x100\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x000b1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x130\x11\x06\x03U\x04\n\x13\nApple Inc.1&0$\x06\x03U\x04\x0b\x13\x1dApple Certification Authority1\x160\x14\x06\x03U\x04\x03\x13\rApple Root CA0\x1e\x17\r130207214847Z\x17\r230207214847Z0\x81\x961\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x130\x11\x06\x03U\x04\n\x0c\nApple Inc.1,0*\x06\x03U\x04\x0b\x0c#Apple Worldwide Developer Relations1D0B\x06\x03U\x04\x03\x0c;Apple Worldwide Developer Relations Certification Authority0\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\xca8T\xa6\xcbV\xaa\xc8$9H\xe9\x8c\xee\xec_\xb8\x7f&\x91\xbc4Sz\xce|c\x80awd^\xa5\x07#\xb69\xfeP-\x15VXp-~\xc4n\xc1J\x85>/\xf0\xde\x84\x1a\xa1W\xc9\xaf{\x18\xffj\xfa\x15\x12I\x15\x08\x19\xac\xaa\xdb*2\xed\x96chR\x15=\x8c\x8a\xec\xbfk\x18\x95\xe0\x03\xac\x01}\x97\x05g\xce\x0e\x85\x957j\xed\t\xb6\xaeg\xcdQd\x9f\xc6\\\xd1\xbcWng5\x80v6\xa4\x87\x81n8\x8f\xd8+\x15N{%\xd8Z\xbfN\x83\xc1\x8d\xd2\x93\xd5\x1aq\xb5`\x9c\x9d3NU\xf9\x12X\x0c\x86\xb8\x16\r\xc1\xe5wE\x8dPH\xba+-\xe4\x94\x85\xe1\xe8\xc4\x9d\xc6h\xa5\xb0\xa3\xfcg~p\xba\x02YKwB\x919\xb9\xf5\xcd\xe1L\xef\xc0;H\x8c\xa6\xe5!]\xfdjj\xbb\xa7\x165`\xd2\xe6\xad\xf3F)\xc9\xe8\xc3\x8b\xe9y\xc0jag\x15\xb2\xf0\xfd\xe5h\xbcb_n\xcf\x99\xdd\xef\x1bc\xfe\x92e\xab\x02\x03\x01\x00\x01\xa3\x81\xa60\x81\xa30\x1d\x06\x03U\x1d\x0e\x04\x16\x04\x14\x88\'\x17\t\xa9\xb6\x18`\x8b\xec\xeb\xba\xf6GY\xc5RT\xa3\xb70\x0f\x06\x03U\x1d\x13\x01\x01\xff\x04\x050\x03\x01\x01\xff0\x1f\x06\x03U\x1d#\x04\x180\x16\x80\x14+\xd0iG\x94v\t\xfe\xf4k\x8d.@\xa6\xf7GM\x7f\x08^0.\x06\x03U\x1d\x1f\x04\'0%0#\xa0!\xa0\x1f\x86\x1dhttp://crl.apple.com/root.crl0\x0e\x06\x03U\x1d\x0f\x01\x01\xff\x04\x04\x03\x02\x01\x860\x10\x06\n*\x86H\x86\xf7cd\x06\x02\x01\x04\x02\x05\x000\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x00\x03\x82\x01\x01\x00O\xcf\xefY\xbe,\xf5\xb2l/\x8f\xee\x13\x872\xe8\x055\xa8n\x8b}\xc9i\x0c\xb9\xd9\x17\xbcw,\xd4g\xe2\xfd\x9am:Y\\\xdf\x83\x01\xbd\xb2\xae*ar\xb1\xaf\xcd\xc3E0\x8f\xa3\x83\r\xce\x1dG\xb4\xf1\x93\x8a\xa3t\x9b\xa4\xc3\x98r\x87;>\xafE\x0b\x92T\xb92\xbb\x90\x18Sk\nN\x10\xb6\xd9\x1dPl!\x80\n\x89NW\x8ck[<=\xa6\xfd\xde\xf7\r#\x1d\x0bJ&\x87?\xba\x91\x92L\xa4\x19\x12\x19mW\xf5zX\x87{h\x8a\xe4\x86\x8cJ\xeb\xe2I\x14\xaa\xa5\xddU\x00\xa9\xae\xbbK0\xae\xe1\xa0\xb1\xbc)\x80\xe6\tw\xe5\xbe4\xa2\x01\xca\x7f\xdc\xe2\n\xe6;\xb8\xbb\xec\xbab\x95\xf3\x05cA\x82\xcd\x0f;\x1dL\x95\xa4\xdb\xab\xf9\xc9\x95\xe9O\xe4M\xe7&\x99\x81\xe9\xbc\xf9\xb4)\xd2\x01zf\xe1.\x8c\xf6!\x8a\xc5\xf8x\xe1\x81\xae\xbf\xd3\x90\x9d\xa9\xad\xf3\xaf\xfd8\x1a\x96g0\x1cQ\xa5\\\xecq\x8a\x82\xb4l\x0f\x0c\x15\x1f'

ALLOWED_PKPASS_ASSETS = (
    'background.png',
    'background@2x.png',
    'background@3x.png',
    'footer.png',
    'footer@2x.png',
    'footer@3x.png',
    'icon.png',
    'icon@2x.png',
    'icon@3x.png',
    'logo.png',
    'logo@2x.png',
    'logo@3x.png',
    'pass.json',
    'strip.png',
    'strip@2x.png',
    'strip@3x.png',
    'thumbnail.png',
    'thumbnail@2x.png',
    'thumbnail@3x.png',
)

REQUIRED_PKPASS_ASSETS = (
    'icon.png',
    'icon@2x.png',
    'icon@3x.png'
)


class PKPass:
    """
    Compressor for pkpass files. Provides basic validation of file types and
    whether file with given name is allowed in pkpass archive.
    Compression happens entirely in memory, meaning there's no need for input, output or
    temporary paths.
    """

    def __init__(self,
                 *assets,
                 key: bytes = b'',
                 cert: bytes = b'',
                 password: bytes = b'',
                 validate: bool = True):

        self.__assets = dict()
        self.key = key
        self.cert = cert
        self.password = password
        self.add_to_pass_package(*assets, validate=validate)

    def add_to_pass_package(self, *assets, validate=True) -> None:
        """
        Adds/updates asset(s) to pass package.
        Adding asset(s) after pass was signed will delete `._signature` attribute and
        require to sign it again.
        :param assets: arbitrary number of pair arguments where element at index [0] is
        the name of the asset, element at index [1] is `bytes` object with file content
        :param validate: decides whether to check if supplied filename is on the list
        of allowed assets
        """
        for name, data in assets:
            assert isinstance(name, str), f'{name!r} is not a string.'
            if validate:
                assert name in ALLOWED_PKPASS_ASSETS, (
                    f'{name!r} is not on a list of supported pkpass assets: '
                    f'{ALLOWED_PKPASS_ASSETS}.\nTo add this file explicitly call '
                    '`add_to_pass_package` with `validate=False` to disable validation.'
                )
            assert isinstance(data, bytes), f'{name!r} is not a bytes object.'
            self.__assets.update({name: data})

        if hasattr(self, '_signature'):
            delattr(self, '_signature')

    def __setitem__(self, name, data):
        self.add_to_pass_package((name, data))

    def __getitem__(self, name):
        return self.__assets[name]

    def __delitem__(self, name):
        item = self.__assets.pop(name, False)
        if item:
            if hasattr(self, '_signature'):
                delattr(self, '_signature')

    @property
    def cert(self):
        return self.__cert

    @cert.setter
    def cert(self, value):
        assert isinstance(value, bytes), 'Certificate must be `bytes` object'
        self.__cert = value

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        assert isinstance(value, bytes), 'Key must be `bytes` object'
        self.__key = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        assert value is None or isinstance(value, bytes), 'Password must be None or `bytes` object'
        self.__password = value

    @property
    def manifest_dict(self) -> dict:
        """
        Hash values of data stored in `.__assets`.
        :return: manifest dictionary
        """
        assert 'pass.json' in self.__assets, 'Pass package must contain `pass.json`'
        if not any(item in self.__assets for item in REQUIRED_PKPASS_ASSETS):
            msg = (
                f'Pass package must have an icon in at least '
                f'one resolution: {REQUIRED_PKPASS_ASSETS}'
            )
            raise AssertionError(msg)
        return {name: sha1(data).hexdigest() for name, data in self.__assets.items()}

    @property
    def manifest(self) -> bytes:
        """
        PKPass manifest containing `.manifest_dict` dumped
        into json and encoded as bytes object.
        :return: bytes object containing manifest.json
        """
        manifest_json = json.dumps(
            self.manifest_dict,
            sort_keys=True,
            indent=4,
            ensure_ascii=False,
            separators=(',', ':')
        )
        return bytes(manifest_json, 'utf8')

    def sign(self, cert: bytes = None, key: bytes = None,
             wwdr: bytes = WWDR_CA, password: bytes = '') -> dict:
        """
        Signs `.manifest`.
        :param cert: bytes object containing developer certificate
        :param key: bytes object containing developer key
        :param wwdr: bytes object containing wwrd certificate
        :param password: (optional) bytes object containing
        key password; because key does not necessarily require
        password this value defaults to `''` instead of `None`,
        this allows to pass `None` as explicitly empty password
        and override value stored in `._password` attribute.
        :return: dict object containing manifest signature
        """

        cert = cert or self.cert
        key = key or self.key
        if password == '':
            password = self.password if self.password else None

        if not all([cert, key, wwdr]):
            msg = (
                'You must provide `certificate`, `key`, [optionally] `password` and `wwdr` '
                'certificate during PKPass initialization, explicitly or as arguments to '
                '`.sign()` method.'
            )
            raise AssertionError(msg)
        self._signature = pkcs7_sign(cert, key, wwdr, self.manifest, password)
        return self._signature

    @property
    def signature(self) -> bytes:
        if not hasattr(self, '_signature'):
            msg = 'You must call `.sign()` before accessing `.signature`.'
            raise AssertionError(msg)
        return self._signature

    @property
    def pass_package(self) -> dict:
        """
        `.manifest`, `.signature` and `.__assets` gathered into one `dict` object
        :return: dict containing all parts to create pkpass
        """
        return {**self.__assets, 'manifest.json': self.manifest, 'signature': self.signature}

    def __bytes__(self):
        """
        `.pass_package` compressed into zip archive.
        :return: signed pkpass compressed as zip archive
        """
        try:
            archive = io.BytesIO()
            with zipfile.ZipFile(
                    file=archive,
                    mode='w',
                    compression=zipfile.ZIP_DEFLATED,
                    allowZip64=False
            ) as buffer:
                for name, data in self.pass_package.items():
                    buffer.writestr(name, data)
            return archive.getvalue()
        except AssertionError as e:
            msg = 'Failed to zip pkpass because of exception.'
            raise AssertionError(msg) from e
