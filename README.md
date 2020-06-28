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


p = PKPass()

for filename in os.listdir(os.getcwd()):
    with open(os.path.join(os.cwd(), filename), 'rb') as f:
    asset = f.read()
    p.add_to_pass_package((filename, asset))

with open(os.path.join(os.path.dirname(__file__), '...your_path_to/key.pem'), 'rb') as f:
    key = f.read()
with open(os.path.join(os.path.dirname(__file__), '...your_path_to/certificate.pem'), 'rb') as f:
    cert = f.read()
    

p.sign(cert=cert, key=key, password=bytes('your_password_123', 'utf8'))

with open('pass.pkpass', 'wb') as file:
    file.write(bytes(p))
```