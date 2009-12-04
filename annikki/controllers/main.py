from annikki.lib.base import *

log = logging.getLogger(__name__)


class MainController(BaseController):

    def index(self):
        review_sets = s.query(ReviewSet).order_by(ReviewSet.timestamp)
        print dir(review_sets)
        return render("main/index.html", extra_vars = {"review_sets": review_sets})
