Annikki is a logbook for your Anki, the spaced repetition software.

Annikki consists of two parts : one part is the website Annikki.org where you can find how well you and others are doing.

A second part is the Annikki plugin for Anki. This little plugin will submit all cards you study to Annikki.

Both parts are still in early development.

Installation and Setup
======================

<del>Install ``annikki`` using easy_install::</del>

    <del>easy_install annikki</del>

Get 'annikki' from github::

    git clone git://github.com/arnebrasseur/annikki.git

Make a config file as follows::

    paster make-config annikki config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.

    paster serve config.ini
