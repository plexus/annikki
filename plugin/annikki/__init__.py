import time

try:
    from httplib import HTTPConnection
except ImportError:
    #Python 3
    from http.client import HTTPConnection

import simplejson as json

from PyQt4 import QtGui, QtCore

from anki.hooks import wrap, addHook
from anki.deck import Deck

import ankiqt
from ankiqt.ui.main import AnkiQt
from ankiqt import mw

from httpx import HTTPClient
import gui


USER='foo'
PWD ='bar'
HOST='localhost'
PORT=5000

class AnnikkiPlugin(object):
    def __init__(self):
        def moveToState(ankiqt, state): # ankiqt.ui.main.AnkiQt
            if state == "studyScreen" or state == "deckFinished":
                self.api.studied(ankiqt.deck.cardsInLastSession(), ankiqt.deck.name())

        AnkiQt.moveToState = wrap(AnkiQt.moveToState, moveToState, "before")
        self.api = AnnikkiClient()
        self.setup_ui()

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
            self.config_dialog = gui.ConfigDialog()


class AnnikkiClient(HTTPClient):
    def __init__(self):
        HTTPClient.__init__(self, HTTPConnection(HOST, PORT))
        self.user = USER
        self.pwd = PWD
        self.initialized()

    def _request(self, method, path_info, body, headers = {}):
        headers['Content-Type'] = 'application/json; charset=UTF-8'
        headers['Accept'] = 'application/json'
        headers['Accept-Charset'] = 'UTF-8'
        return HTTPClient._request(self, method, path_info, body, headers)

    def studied(self, cards, deck):
        #print "You studied %d cards of '%s', good on you!" % (cards, name)
        try:
            print self.post('/api/studied', {"deck": deck, "cards": cards})
        except HTTPError as err:
            #TODO
            raise err

    def initialized(self):
        pass
        #print self.post('/api/test', {"msg": "initialized"})

    def marshal(self, data):
        data["user"] = self.user
        data["pwd"] = self.pwd
        return json.dumps(data)

    def unmarshal(self, body):
        return json.loads(body)

############################################################
# anki.deck.Deck

def cardsInLastSession(self):
    limit = self.sessionTimeLimit
    start = self.sessionStartTime or time.time() - limit
    return self.s.scalar(
        "select count(*) from reviewHistory where time >= :t",
        t=start)

Deck.cardsInLastSession = cardsInLastSession


