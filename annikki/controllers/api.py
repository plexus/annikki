import logging
from pprint import pprint

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from sqlalchemy.sql import func

from annikki.lib import remote_user
from annikki.lib.base import BaseController, render, api_call

from annikki.model import *
from annikki.model.meta import Session as s

log = logging.getLogger(__name__)


class ApiController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/api.mako')
        # or, return a response
        return 'Hello World'

    @api_call
    def studylog(self, data):
        user = remote_user(request)

        if data['deck'] and data['cards'] and data['deck_id']:
            deck = Deck.find_or_create(user.uid, data['deck_id'], data['deck'])
            for c in data['cards']:
                card = Card.find_or_create(user.uid, deck.id, c['id'], c['question'], c['answer'])
                review = Review(card.id, func.now(), c['ease'])
                s.add(review)
            s.commit()
            return {'msg': "Submitted %d reviews" % len(data['cards'])}

        #    sl = model.StudyLog(user, data['deck'], data['count'], func.now())
        #    model.meta.Session.add(sl)
        #    model.meta.Session.commit()
        #else:
        #    abort(400, "'studylog' requires parameters 'deck' and 'count'")

        pprint(data)
        return {"msg":"Bad request to studylog"}
        
    @api_call
    def test(self, data):
        print("/api/test")
        user = request.remote_user_obj()

        pprint(data)
        pprint(user)
        pprint(request.remote_user)
        print()
        return {"msg": "test called"}
