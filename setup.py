try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='debshots',
    version='0.4.13',
    description='Web application that manages screenshots of applications available in Debian',
    author='Christoph Haas',
    author_email='email@christoph-haas.de',
    url='http://debshots.workaround.org/',
    install_requires=[
        "Pylons==1.0",
        "PIL>=1.1.6",
        "SQLAlchemy==0.6.4",
        "Webhelpers>=1.0",
        #"pastescript==1.7.3",
        #"paste==1.7.3",
        #"psycopg2>=2.0.6",  # can also be deployed with sqlite - then psycopg2 is unneeded
        "formencode>=1",
        "python-memcached",
        "pygooglechart",
        ],
    scripts=['bin/debshots-update-packages',
        'bin/debshots-create-admin',
        'bin/debshots-delete-admin',
        ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'debshots': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'debshots': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = debshots.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
