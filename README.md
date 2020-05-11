# airpress

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
# `password` argument is optional
p.sign(cert=bytes(...), key=bytes(...), password=bytes(...))
# Calling `bytes()` on signed `PKPass` will compress it into zip archive and return its `bytes` representation.
_ = bytes(p) 
```

In most cases you're likely to return `pkpass` as `http` response and `bytes` object is exactly what you need.
It's up to you how to handle `.pkpass` archive from this point. 
`PKPass` will raise human-readable errors in case something is 
wrong with pass package you're trying to sign and compress. 

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