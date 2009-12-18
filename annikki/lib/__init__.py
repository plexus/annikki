from annikki import model
from annikki.lib.error import FormError
from sqlalchemy.exc import IntegrityError

from authkit.users.sqlalchemy_driver import UsersFromDatabase as AuthKitUsersFromDatabase
from paste.util.import_string import eval_import
from pylons.controllers.util import Request

from sqlalchemy import *
from sqlalchemy.orm import *

from authkit.users import *


def remote_user(self):
    name = self.environ['REMOTE_USER']
    return model.meta.Session.query(model.User).filter_by(username=name).first()

Request.remote_user_obj = remote_user

#Override some methods from the basic Autkit/SQLalchemy class
class UsersFromDatabase(AuthKitUsersFromDatabase):

    # Because we have two WSGI apps (one for the API one regular)
    # the user model gets initialized twice. The normal Authkit version
    # of this class raises an exception.
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


    # Our User has an email field extra, perhaps move these
    # classes to our own model definitions in the future?
    def update_model(self, model):
        
        metadata = model.meta.metadata
        
        class User(object):
            def __init__(
                self,
                username,
                uid=None,
                password=None,
                group_uid=None,
                email=None
            ):
                self.id         = id
                self.username   = username
                self.password   = password
                self.email      = email
                self.group_uid  = group_uid
            def __repr__(self):
                return "User(%(username)s)" % self.__dict__

        class Group(object):
            def __init__(self, name=None):
                self.name = name
            def __repr__(self):
                return "Group(%(name)s)" % self.__dict__
                
        class Role(object):
            def __init__(self, name=None):
                self.name = name
            def __repr__(self):
                return "Role(%(name)s)" % self.__dict__
                
        # Tables
        groups_table = Table(
            "groups",
            metadata,
            Column("uid",        Integer,        primary_key=True),
            Column("name",       String(255),    unique=True,    nullable=False),
        )
        roles_table = Table(
            "roles",
            metadata,
            Column("uid",        Integer,        primary_key=True),
            Column("name",       String(255),    unique=True,    nullable=False),
        )
        users_table = Table(
            "users",
            metadata,
            Column("uid",        Integer,        primary_key=True),
            Column("username",   String(255),    unique=True,    nullable=False),
            Column("password",   String(255),    nullable=False),
            Column("email",      String(255),    unique=True,    nullable=False),
            Column("group_uid",  Integer,        ForeignKey("groups.uid")),
        )
        users_roles_table = Table(               # many:many relation table
            "users_roles",
            metadata,
            Column("user_uid",   Integer,        ForeignKey("users.uid")),
            Column("role_uid",   Integer,        ForeignKey("roles.uid")),
        )

        # Uses the mapper as part of the Session
        mapper(
            Group,
            groups_table,
            properties={
                "users": relation(User)
            }
        )
        mapper(
            User,
            users_table,
            properties={
                "roles": relation(Role, lazy=True, secondary=users_roles_table),
                "group": relation(Group),
            }
        )
        mapper(
            Role,
            roles_table,
            properties={
                "users": relation(User, lazy=True, secondary=users_roles_table)
            }
        )

        model.User = User
        model.Group = Group
        model.Role = Role
        return model

       
    # Create Methods
    def user_create(self, username, password, email, group=None):
        """
        Create a new user with the username, password and group name specified.
        """
        if group is None:
            new_user = self.model.User(
                username=username.lower(), 
                password=self.encrypt(password),
                email=email
            )
        else:
            if not self.group_exists(group):
                raise AuthKitNoSuchGroupError(
                    "There is no such group %r"%group
                )
            new_user = self.model.User(
                username=username.lower(), 
                password=self.encrypt(password), 
                group_uid=self.meta.Session.query(self.model.Group).\
                    filter_by(name=group.lower()).first().uid,
                email=email
            )
        self.meta.Session.add(new_user)
        try:
            self.meta.Session.flush()
        except IntegrityError, e:
            self.meta.Session.rollback()
            errors={}
            if self.user_exists(username):
                errors['username'] = 'This username is already taken.'
            if self.email_exists(email):
                errors['email'] = 'This e-mail is already registered.'
            if errors:
                raise FormError(**errors)
            raise e

    #more natural alias
    create_user = user_create

    def email_exists(self, email):
        user = self.meta.Session.query(self.model.User).filter_by(
            email=email.lower()).first()
        if user is not None:
            return True
        return False
