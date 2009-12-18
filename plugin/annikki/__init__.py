#
# Annikki : log your Anki activity on Annikki.org
# Author : Arne Brasseur <arne@arnebrasseur.net>

VERSION='0.1.0'

import time

try:
    from httplib import HTTPConnection
except ImportError:
    #Python 3
    from http.client import HTTPConnection

import simplejson as json

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox

from anki.hooks import wrap, addHook
from anki.deck import Deck

import ankiqt
from ankiqt.ui.main import AnkiQt
from ankiqt import mw

from httpx import *

from . import gui, config
from annikki.timex import datetime_as_str
from datetime import datetime as dt

HOST='localhost'
PORT=5000

# A few callables used to hook into Anki

class AnkiQt_moveToState:
    def __init__(self, annikki):
        self.annikki = annikki

    def __call__(self, ankiqt, state):
        if state == "studyScreen" or state == "deckFinished":
            self.annikki.api.studied(ankiqt.deck, self.annikki.cards_answered)
            self.annikki.cards_answered = []

class Deck_answerCard:
    def __init__(self, annikki):
        self.annikki = annikki

    def __call__(self, deck, card, ease):
        self.annikki.cardAnswered(deck, card, ease)

# The main plugin class

class AnnikkiPlugin(object):
    def __init__(self):
        AnkiQt.moveToState = wrap(AnkiQt.moveToState, AnkiQt_moveToState(self), "before")
        Deck.answerCard = wrap(Deck.answerCard, Deck_answerCard(self), "after")
        self.config = config.Config(mw.config)
        self.api = AnnikkiClient(self, self.config)
        self.setup_ui()
        self.cards_answered = []

    def setup_ui(self):
        self.actionConfigure = QtGui.QAction(mw)
        self.actionConfigure.setObjectName("configureAnnikki")
        self.actionConfigure.setText("&Annikki Preferences")
        mw.mainWin.menu_Settings.addAction(self.actionConfigure)
        mw.connect(self.actionConfigure, QtCore.SIGNAL("triggered()"), self.show_config_dialog)

    def show_config_dialog(self):
        if 'config_dialog' in self.__dict__:
            self.config_dialog.show()
        else:
            self.config_dialog = gui.ConfigDialog(self.config)
            
    def cardAnswered(self, deck, card, ease):
        c = {}
        for key in ('id','question','answer'):
            c[key] = getattr(card, key)
        c['ease'] = ease
        c['time'] = datetime_as_str(dt.utcnow())
        self.cards_answered.append(c)

# The HTTP client with support for the various Annikki API entry points

class AnnikkiClient(HTTPClient):
    def __init__(self, annikki, config):
        HTTPClient.__init__(self, HTTPConnection(HOST, PORT))
        self.config = config
        self.annikki = annikki
        self.initialized()

    def _request(self, method, path_info, body, headers = {}):
        headers['Content-Type'] = 'application/json; charset=UTF-8'
        headers['Accept'] = 'application/json'
        headers['Accept-Charset'] = 'UTF-8'
        try:
            return HTTPClient._request(self, method, path_info, body, headers)
        except Unauthorized:
            self.annikki.show_config_dialog()

    def studied(self, deck, cards):
        try:
            reply = self.post('/api/studylog', 
                              {"deck":     deck.name(),
                               "syncName": deck.syncName, 
                               "cards":    cards, 
                               "time":     datetime_as_str(dt.utcnow())
                               })
        #TODO : improve error handling/messages
        except ClientError, e:
            QMessageBox.warning(mw, "Annikki has a problem", "Submitting to Annikki failed.\n\n%s" % e.msg)
        except  ServerError, e:
            if e.status == 503:
                QMessageBox.warning(mw, "Annikki has a problem", "The Annikki site is currently unavailable.")
            else:
                QMessageBox.warning(mw, "Annikki has a problem", "Submitting to Annikki failed\n\n%s." % e.msg)

        except HTTPError, e:
            QMessageBox.warning(mw, "Annikki has a problem", "Submitting to Annikki failed.\n\n%s" % e.msg)

    def initialized(self):
        pass
        print self.post('/api/test', {"msg": "initialized"})

    def marshal(self, data):
        data["v"] = VERSION
        data["user"] = self.config.username
        data["pwd"] = self.config.password
        return json.dumps(data)

    def unmarshal(self, body):
        if body == None:
            return {}
        data = json.loads(body)
        if data.has_key("msg"):
            mw.mainWin.statusbar.showMessage(data["msg"], 3000)
            

