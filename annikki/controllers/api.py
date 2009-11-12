import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from sqlalchemy.sql import func

from annikki.lib import remote_user
from annikki.lib.base import BaseController, render, api_call

from annikki import model

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

        if data['deck'] and data['count']:
            sl = model.StudyLog(user, data['deck'], data['count'], func.now())
            model.meta.Session.add(sl)
            model.meta.Session.commit()
        else:
            abort(400, "'studylog' requires parameters 'deck' and 'count'")

        return {"msg":"Added studylog"}
        
