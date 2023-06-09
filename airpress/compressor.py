import io
import json
import zipfile
from hashlib import sha1

# from .crypto import pkcs7_sign
from .crypto2 import pkcs7_sign

# Downloaded from: https://www.apple.com/certificateauthority/
# Certificate URL: https://developer.apple.com/certificationauthority/AppleWWDRCA.cer
# Valid through 02/07/2023 21:48:47 UTC

ALLOWED_PKPASS_ASSETS = (
    "background.png",
    "background@2x.png",
    "background@3x.png",
    "footer.png",
    "footer@2x.png",
    "footer@3x.png",
    "icon.png",
    "icon@2x.png",
    "icon@3x.png",
    "logo.png",
    "logo@2x.png",
    "logo@3x.png",
    "pass.json",
    "strip.png",
    "strip@2x.png",
    "strip@3x.png",
    "thumbnail.png",
    "thumbnail@2x.png",
    "thumbnail@3x.png",
)

PKPASS_ICONS = ("icon.png", "icon@2x.png", "icon@3x.png")


class PKPass:
    """
    Compressor for pkpass files. Provides basic validation of file types and
    whether file with given name is allowed in pkpass archive.
    Compression happens entirely in memory, meaning there's no need for input, output or
    temporary paths.
    """

    def __init__(
        self,
        *assets,
        key: bytes = b"",
        cert: bytes = b"",
        password: bytes = b"",
        validate: bool = True,
    ):

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
            if not isinstance(name, str):
                raise TypeError(f"{name!r} is not a string.")
            if validate:
                assert name in ALLOWED_PKPASS_ASSETS, (
                    f"{name!r} is not on a list of supported pkpass assets: "
                    f"{ALLOWED_PKPASS_ASSETS}.\nTo add this file explicitly call "
                    "`add_to_pass_package` with `validate=False` to disable validation."
                )
            if not isinstance(data, bytes):
                raise TypeError(f"{name!r} is not a bytes object.")
            assert data, f"{name!r} cannot be empty."
            self.__assets.update({name: data})

        if hasattr(self, "_signature"):
            delattr(self, "_signature")

    def __setitem__(self, name, data):
        self.add_to_pass_package((name, data))

    def __getitem__(self, name):
        return self.__assets[name]

    def __delitem__(self, name):
        del self.__assets[name]
        if hasattr(self, "_signature"):
            delattr(self, "_signature")

    @property
    def cert(self):
        return self.__cert

    @cert.setter
    def cert(self, value):
        if not isinstance(value, bytes):
            raise TypeError("Certificate must be `bytes` object")
        self.__cert = value

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        if not isinstance(value, bytes):
            raise TypeError("Key must be `bytes` object")
        self.__key = value

    @property
    def wwdr_cert(self):
        return self.__wwdr_cert

    @wwdr_cert.setter
    def wwdr_cert(self, value):
        if not isinstance(value, bytes):
            raise TypeError("Certificate must be `bytes` object")
        self.__wwdr_cert = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        assert value is None or isinstance(value, bytes), "Password must be None or `bytes` object"
        self.__password = value

    @property
    def manifest_dict(self) -> dict:
        """
        Hash values of data stored in `.__assets`.
        :returns: manifest dictionary
        """
        assert "pass.json" in self.__assets, "Pass package must contain `pass.json`"
        if not any(item in self.__assets for item in PKPASS_ICONS):
            msg = f"Pass package must have an icon in at least one resolution: {PKPASS_ICONS}"
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
            separators=(",", ":"),
        )
        return bytes(manifest_json, "utf8")

    def sign(
        self,
        cert: bytes = None,
        key: bytes = None,
        wwdr: bytes = None,
        password: bytes = "",
    ) -> bytes:
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
        :returns: dict object containing manifest signature
        """

        cert = cert or self.cert
        key = key or self.key
        if password == "":
            password = self.password if self.password else None

        if not all([cert, key, wwdr]):
            msg = (
                "You must provide `certificate`, `key`[, `password` and `wwdr` certificate] "
                "during PKPass initialization, explicitly or as arguments to `.sign()` method."
            )
            raise AssertionError(msg)
        self._signature = pkcs7_sign(cert, key, wwdr, self.manifest, password)
        return self._signature

    @property
    def signature(self) -> bytes:
        if not hasattr(self, "_signature"):
            msg = "You must call `.sign()` before accessing `.signature`."
            raise AttributeError(msg)
        return self._signature

    @property
    def pass_package(self) -> dict:
        """
        `.manifest`, `.signature` and `.__assets` gathered into one `dict` object
        :returns: dictionary containing all components to create `.pkpass` archive
        """
        return {
            **self.__assets,
            "manifest.json": self.manifest,
            "signature": self.signature,
        }

    def __call__(self, *args, **kwargs):
        """Calls __bytes__ method and returns compressed `.pkpass` file"""
        return self.__bytes__()

    def __bytes__(self):
        """
        This is the magic.
        `.pass_package` is compressed into zip
        archive and returned as `bytes` object.
        :returns: bytes object with signed `.pkpass`
        """
        try:
            archive = io.BytesIO()
            with zipfile.ZipFile(file=archive, mode="w", compression=zipfile.ZIP_DEFLATED, allowZip64=False) as buffer:
                for name, data in self.pass_package.items():
                    buffer.writestr(name, data)
            return archive.getvalue()
        except (AssertionError, AttributeError) as e:
            msg = "Failed to zip `.pkpass` because of another exception."
            raise Exception(msg) from e
