from annikki.lib.base import *

log = logging.getLogger(__name__)


class MainController(BaseController):

    def index(self):
        vars = {}
        vars['review_sets'] = s.query(ReviewSet).order_by(ReviewSet.timestamp)
        vars['top_users'] = s.query(User)
        return render("main/index.html", extra_vars = vars)

    def user(self, name):
        User.find(
)
    
