# airpress

[![PyPI version](https://img.shields.io/pypi/v/airpress.svg)](https://pypi.python.org/pypi/airpress)
[![PyPI version](https://img.shields.io/pypi/pyversions/airpress.svg)](https://pypi.python.org/pypi/airpress)
[![Build Status](https://travis-ci.org/captain-fox/airpress.svg?branch=master)](https://travis-ci.org/captain-fox/airpress)

AirPress lets you create, sign and zip PKPass archives for Apple Wallet in runtime memory without a need for temporary files or directories.

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
`PKPass` will raise human-readable errors in case something is 
wrong with pass package you're trying to sign and compress. 

## Manage assets in pass package
Accessing `PKPass` assets that are already added to pass package is as easy as working with dictionary.

Retrieve asset: 
```python
icon = p['icon.png']
``` 

It can also be used as alternative to add/update asset:

```python
p['icon.png'] = bytes(...)
```

Remove asset from pass package:
```python
del p['logo.png']
```


## Prepare Pass Type ID certificate

[If you don't have your pass type certificate, follow this guide to create one.](https://www.skycore.com/help/creating-pass-signing-certificate/)


Export your developer certificate as `.p12` file and convert it into a pair of cert and key `.pem` files:
 
`openssl pkcs12 -in "Certificates.p12" -clcerts -nokeys -out certificate.pem`   

`openssl pkcs12 -in "Certificates.p12" -nocerts -out key.pem`

You will be asked for an export password (or export phrase), you may leave it blank or provide a passphrase. 
It's this value that you later should supply to PKPass compressor (or leave blank).

## Example with local files

In case you'd like to play around with locally stored files, or your server keeps assets in the same file storage
as source code, this example shows you how to read locally stored assets as `bytes` objects, compress `pkpass` archive
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