from setuptools import setup, find_packages

setup(
    name='homelife',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Flask',
        'gunicorn',
        'cryptography',
        'requests',
        'dependency-injector',
        'pymongo'
    ],
)
