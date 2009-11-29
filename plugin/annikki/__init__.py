import time

try:
    from httplib import HTTPConnection
except ImportError:
    #Python 3
    from http.client import HTTPConnection

import simplejson as json

from ankiqt.ui.main import AnkiQt
from anki.hooks import wrap, addHook
from anki.deck import Deck

from annikki.httpx import HTTPClient

USER='plexus'
PWD ='plexuspass'
HOST='localhost'
PORT=8080

class AnnikkiPlugin:
    def __init__(self):
        # ankiqt.ui.main.AnkiQt#moveToState
        def moveToState(ankiqt, state):
            #print "moveToState", state
            if state == "studyScreen" or state == "deckFinished":
                self.api.studied(ankiqt.deck.cardsInLastSession(), ankiqt.deck.name())

        AnkiQt.moveToState = wrap(AnkiQt.moveToState, moveToState, "before")
        print "Annikki support initialized"
        self.api = AnnikkiClient()


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
        print self.post('/', {"msg": "initialized"})

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


