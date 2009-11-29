from annikki import model

from authkit.users.sqlalchemy_driver import UsersFromDatabase as AuthKitUsersFromDatabase
from paste.util.import_string import eval_import


def remote_user(request):
    name = request.environ['REMOTE_USER']
    return model.meta.Session.query(model.User).filter_by(username=name).first()

class UsersFromDatabase(AuthKitUsersFromDatabase):
    def __init__(self, model, encrypt=None):
        if encrypt is None:
            def encrypt(password):
                return password
        self.encrypt = encrypt
        if isinstance(model, (str, unicode)):
            model = eval_import(model)
        if hasattr(model, 'authkit_initialized'):
            self.model = model
            self.meta = self.model.meta
        else:
            self.model = self.update_model(model)
            self.meta = self.model.meta        
            model.authkit_initialized = True
