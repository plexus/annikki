"""Setup the annikki application"""
import logging

from annikki.lib import UsersFromDatabase
from authkit.users import AuthKitError

from annikki.config.environment import load_environment
from annikki.model import meta

from annikki import model

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup annikki here"""
    load_environment(conf.global_conf, conf.local_conf)

    # AuthKit
    log.info("Adding the AuthKit model...")
    users = UsersFromDatabase(model)

    # Create the tables if they don't already exist
    log.info("Creating tables")
    meta.metadata.create_all(bind=meta.engine)
    log.info("Successfully setup")

    # base users
    try:
        users.group_create("user")
        users.group_create("admin")

        #users.role_create("delete")
        #users.user_create("foo", password="bar", group="admin")
        #users.user_create("admin", password="opensesame")
        #users.user_add_role("admin", role="delete")
    except AuthKitError, e:
        pass

    try:
        meta.Session.flush()
        meta.Session.commit()
    finally:
        meta.Session.close()


