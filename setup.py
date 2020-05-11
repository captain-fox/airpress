import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='airpress',
    version='0.0.1',
    author='Stan Reduta',
    author_email='stanislaw.reduta@gmail.com',
    description='A frustration-free compression tool for PKPass archives.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/captain-fox/airpress',
    packages=['airpress'],
    install_requires=['cryptography>=2.9.2'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
