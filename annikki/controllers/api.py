from pprint import pprint
from sqlalchemy.sql import func
from annikki.lib.base import *

from annikki.lib.timex import datetime_from_str

log = logging.getLogger(__name__)


class ApiController(BaseController):
    """
    Controller to handle calls from the Anki plugin
    """

    @api_call
    def studylog(self, data):
        pprint(data)

        user = remote_user(request)

        if data['deck'] and data['cards'] and data['time']:
            deck = Deck.find_or_create(user_id = user.uid,                                        
                                       name = data['deck'])
            reviewset = ReviewSet(timestamp = datetime_from_str(data['time']), user_id=user.uid)
            s.add(reviewset)
            for c in data['cards']:
                card = Card.find_or_create(user.uid, deck.id, c['id'], c['question'], c['answer'])
                review = Review(card.id, func.now(), c['ease'])
                review.review_set = reviewset
                s.add(review)
            s.commit()
            return {'msg': "Submitted %d reviews" % len(data['cards'])}

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
