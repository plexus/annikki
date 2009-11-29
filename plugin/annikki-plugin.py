# -*- coding: utf-8 -*-
# Copyright: Arne Brasseur <arne@arnebrasseur.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
Support for the Anki-logbook website Annikki.org.
"""

from ankiqt import mw
from anki.hooks import addHook

def annikki_init():
  import annikki
  global ANNIKKI_INSTANCE
  ANNIKKI_INSTANCE = annikki.AnnikkiPlugin()

mw.registerPlugin("Annikki", None)
addHook("init", annikki_init)

