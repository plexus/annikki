from annikki.lib.base import *
from annikki.lib.error import FormError

import formencode
from formencode import validators
from formencode.validators import UnicodeString, Email, FieldsMatch

log = logging.getLogger(__name__)

class SignUpForm(formencode.Schema):
    username = formencode.compound.All(validators.Regex(regex='^[a-zA-Z][-_a-zA-Z1-9]+$'),
                                       UnicodeString(not_empty = True, min=4))
    email = Email(not_empty = True)
    password = UnicodeString(not_empty = True, min=6)
    confirm = UnicodeString(not_empty = True, min=6)

    chained_validators = [FieldsMatch('password', 'confirm')]

class UserController(BaseController):

  def signup(self):
    if request.method != 'POST':
        return render("signup.html")
    
    try:
        post = SignUpForm(filter_extra_fields = True).to_python(request.POST)
    except formencode.Invalid, e:
        return render("signup.html", form_data=request.POST, form_errors=e.error_dict)
    
    users=request.environ['authkit.users']

    # create user is picky about the dict it gets
    del post['confirm']
    
    try:
        users.create_user(**post)
    except FormError, e:
        return render("signup.html", form_data=request.POST, form_errors=e.error_dict)
    meta.Session.commit()
    
    # Sign in so the cookie auth handler will send back the right cookie
    request.environ["REMOTE_USER"] = post['username']
    request.environ['paste.auth_tkt.set_user'](userid=request.environ['REMOTE_USER']) # , user_data=self.user_data(state))
    
    h.flash("Welcome to Annikki, %(username)s!" % post)
    
    redirect(url(controller='main'))
