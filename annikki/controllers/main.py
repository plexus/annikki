from annikki.lib.base import *
from sqlalchemy import func, desc

log = logging.getLogger(__name__)

RANK_LIMIT=10

class MainController(BaseController):

    def index(self):
        #review_sets = s.query(ReviewSet).order_by(ReviewSet.timestamp)
        #print dir(review_sets)
        #return render("main/index.html", extra_vars = {"review_sets": review_sets})
        reviews, users, decks = [s.query(m).count() for m in [Review, User, Deck]]

        user_rank = s.query(User.username, func.count(User.uid).label('count')). \
            join(ReviewSet). join(Review). group_by(User.uid). order_by(desc('count')).limit(RANK_LIMIT)

        deck_rank = s.query(Deck.name, func.count(User.uid).label('count')). \
            join(Card). join(Review). group_by(Deck.id). order_by(desc('count')).limit(RANK_LIMIT)

        return render("main/index.html", extra_vars = {'counters': {'reviews': reviews,
                                                                    'decks': decks,
                                                                    'users': users} ,
                                                       'user_rank': user_rank,
                                                       'deck_rank': deck_rank
                                                       })
