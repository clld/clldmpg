from setuptools import setup, find_packages


install_requires = [
    'clld>=3.1.0',
    'purl',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pep8',
    'mock',
]

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface',
]

testing_extras = tests_require + [
    'nose',
    'coverage',
    'virtualenv',  # for scaffolding tests
]

setup(
    name='clldmpg',
    version='2.2.0',
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
    author="Robert Forkel, MPI SHH",
    author_email="forkel@shh.mpg.de",
    url="http://clld.org",
    license="Apache Software License",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={'testing': testing_extras, 'docs': docs_extras},
    tests_require=tests_require,
    test_suite="clldmpg.tests",
    message_extractors={'clldmpg': [
        ('**.py', 'python', None),
        ('**.mako', 'mako', None),
        ('static/**', 'ignore', None)]},
    entry_points="""\
        [pyramid.scaffold]
        clldmpg_app=clldmpg.scaffolds:ClldAppTemplate
    """)
