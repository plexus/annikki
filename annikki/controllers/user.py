from annikki.lib.base import *

import formencode
from formencode import validators
from formencode.validators import UnicodeString, Email, FieldsMatch

log = logging.getLogger(__name__)

class SignUpForm(formencode.Schema):
    username = UnicodeString(not_empty = True, min=4)
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

    del post['confirm']
    users.create_user(**post)
    
    h.flash("Welcome to Annikki, %(username)s!" % post)

    redirect(url(controller='main'))

    #return render("signup.html", form_data=post)
