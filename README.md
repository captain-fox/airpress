# airpress

[![PyPI version](https://img.shields.io/pypi/v/airpress.svg)](https://pypi.python.org/pypi/airpress)
[![PyPI version](https://img.shields.io/pypi/pyversions/airpress.svg)](https://pypi.python.org/pypi/airpress)
[![Build Status](https://travis-ci.org/captain-fox/airpress.svg?branch=master)](https://travis-ci.org/captain-fox/airpress)

Compression tool for PKPass archives.

AirPress does compression in runtime memory without creating temporary files or directories,
which is handy for server-side implementation.

## Installation
From PyPI:

`pip install airpress`

## Quickstart
```python
from airpress import PKPass

# PKPass compressor operates on `bytes` objects as input/output
p = PKPass(
    ('icon.png', bytes(...)),
    ('logo.png', bytes(...)),
    ('pass.json', bytes(...)),
    ...
)
p.sign(cert=bytes(...), key=bytes(...), password=bytes(...))  # `password` argument is optional
_ = bytes(p)  # Creates `bytes` object containing signed and compressed `.pkpass` archive
```

In most cases you're likely to return `pkpass` as `http` response and `bytes` object is exactly what you need.
It's up to you how to handle `.pkpass` archive from this point. 
`PKPass` will raise human-readable errors in case something is 
wrong with pass package you're trying to sign and compress. 

## Prepare Pass Type ID certificate

[If you don't have your pass type certificate, follow this guide to create one.](https://www.skycore.com/help/creating-pass-signing-certificate/)


Export your developer certificate as `.p12` file and convert it into a pair of cert and key `.pem` files:
 
`openssl pkcs12 -in "Certificates.p12" -clcerts -nokeys -out certificate.pem`   

`openssl pkcs12 -in "Certificates.p12" -nocerts -out key.pem`

You will be asked for an export password (or export phrase), you may leave it blank or provide a passphrase. 
It's this value that you later should supply to PKPass compressor (or leave blank).

## Example

This example shows how to read locally stored assets as `bytes` objects, compress `pkpass` archive
and save it to script's parent directory.

```python
import os
from airpress import PKPass

icon = open(os.path.join(os.path.dirname(__file__), '...your_path_to/icon.png'), 'rb').read()
icon_2x = open(os.path.join(os.path.dirname(__file__), '...your_path_to/icon@2x.png'), 'rb').read()
logo = open(os.path.join(os.path.dirname(__file__), '...your_path_to/logo.png'), 'rb').read()
logo_2x = open(os.path.join(os.path.dirname(__file__), '...your_path_to/logo@2x.png'), 'rb').read()
# It is more likely that you'll be dumping python dictionary into json file, but as an example `pass.json` is a file
pass_json = open(os.path.join(os.path.dirname(__file__), '...your_path_to/pass.json'), 'rb').read()

key = open(os.path.join(os.path.dirname(__file__), '...your_path_to/key.pem'), 'rb').read()
cert = open(os.path.join(os.path.dirname(__file__), '...your_path_to/certificate.pem'), 'rb').read()
password = bytes('your_password_123', 'utf8')

p = PKPass(
    ('icon.png', icon),
    ('icon@2x.png', icon_2x),
    ('logo.png', logo),
    ('logo@2x.png', logo_2x),
    ('pass.json', pass_json),
)
p.sign(cert=cert, key=key, password=password)

with open('pass.pkpass', 'wb') as file:
    file.write(bytes(p))
```