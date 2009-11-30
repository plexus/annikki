# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='annikki',
    version='0.1.1',
    description=u'Annikki (暗日記) is an on-line diary for Anki.',
    author=u'Arne Brasseur',
    author_email=u'arne@arnebrasseur.net',
    url=u'http://www.annikki.org',
    install_requires=[
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5",
        "Genshi>=0.4",
        "AuthKit>=0.4.5"
    ],
    license=u"GPLv3",
    long_description=u"Annikki (暗日記) is an on-line diary for Anki. Share your efforts with the world. The web application runs at www.annikki.org, while user stats are gathered through a plugin for Anki.",
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'annikki': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'annikki': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=True,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main_app = annikki.config.middleware:make_main_app
    api_app = annikki.config.middleware:make_api_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [authkit.method]
    json = annikki.lib.authkitx:make_json_auth_handler
    """,
)
