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


# Create empty pass package
p = PKPass()

# Add locally stored assets
for filename in os.listdir('your_dir_with_assets'):
    with open(os.path.join(os.path.dirname(__file__), 'your_dir_with_assets', filename), 'rb') as file:
        data = file.read()
        # Add each individual asset to pass package
        p.add_to_pass_package((filename, data))

# Add locally stored credentials
with open(
        os.path.join(os.path.dirname(__file__), 'your_dir_with_credentials/key.pem'), 'rb'
) as key, open(
    os.path.join(os.path.dirname(__file__), 'your_dir_with_credentials/certificate.pem'), 'rb'
) as cert:
    # Add credentials to pass package 
    p.key = key.read()
    p.cert = cert.read()
    p.password = bytes('passpass', 'utf8')

# As we've added credentials to pass package earlier we don't need to supply them to `.sign()`
# This is an alternative to calling .sign() method with credentials as arguments. 
p.sign()
 
# Create pkpass file with pass data 
with open('your_dir_for_output/data.pkpass', 'wb') as file:
    file.write(bytes(p))
```

Hope you find this package useful!
I'd love to hear your feedback and suggestions for this tiny library as there's always room for improvement.