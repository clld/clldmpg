from setuptools import setup, find_packages


setup(
    name='clldmpg',
    version='3.2.0',
    description=(
        'Python library supporting development of CLLD apps maintained by MPI SHH'),
    long_description='',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
    ],
    keywords='web pyramid',
    author="Robert Forkel",
    author_email="forkel@shh.mpg.de",
    url="http://clld.org",
    license="Apache Software License",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld~=4.0',
        'purl',
        'clldutils~=2.0',
    ],
    extras_require={
        'test': ['mock>=2.0', 'pytest-clld', 'pytest-mock', 'coverage>=4.2', 'pytest-cov'],
        'dev': ['tox', 'flake8', 'wheel', 'twine'],
    },
    message_extractors={'src/clldmpg': [
        ('**.py', 'python', None),
        ('**.mako', 'mako', None),
        ('static/**', 'ignore', None)]},
    entry_points={
        'pyramid.scaffold': ['clldmpg_app=clldmpg.scaffolds:ClldAppTemplate'],
        'console_scripts': ['clldmpg=clldmpg.__main__:main'],
    },
)
