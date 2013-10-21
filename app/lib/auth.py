#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
#   
#   This file is part of Sageo
#   
#   Sageo is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Sageo is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Sageo.  If not, see <http://www.gnu.org/licenses/>

from functools import update_wrapper

from flask import current_app, abort
from flask.ext.login import current_user

ROLE_USER = 0
ROLE_ADMIN = 1

#from itsdangerous import URLSafeTimedSerializer

#from .config import SECRET_KEY

#login_serializer = URLSafeTimedSerializer(SECRET_KEY)


def authorized(checker):
    """Check if current user is authenticated and authorized.

    Meant to be used inside views and templates to protect part of resources.
    """
    return current_user.is_authenticated() and checker()


def require(checker):
    """
    Ensure that current user is authenticated and authorized to access the
    decorated view.  For example::

        @app.route('/protected')
        @require(Any(IsUser('root'), InGroups('admins')))
        def protected():
            pass

    """
    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            if not current_user.is_authenticated():
                return current_app.login_manager.unauthorized()
            if not checker():
                abort(403)
            return fn(*args, **kwargs)
        return update_wrapper(wrapped_function, fn)
    return decorator


class IsAdmin(object):
    """Check if current user has provided username."""

    def __init__(self):
        pass

    def __call__(self):
        return current_user.role == ROLE_ADMIN


class IsUser(object):
    """Check if current user has provided username."""

    def __init__(self, username):
        self.username = username

    def __call__(self):
        return current_user.username == self.username


class InGroups(object):
    """Check if current user belongs to provided groups."""

    def __init__(self, *args):
        self.groups = set(args)

    def __call__(self):
        # TODO check if the acl group can come here...
        return False
        return self.groups <= current_user.in_groups()


class HasPermissions(object):
    """Check if current user has provided permissions."""

    def __init__(self, *args):
        self.permissions = set(args)

    def __call__(self):
        return self.permissions <= current_user.has_permissions()


class All(object):
    """Compound checker to check if all provided checkers are true."""

    def __init__(self, *args):
        self.checkers = args

    def __call__(self):
        return all(c() for c in self.checkers)


class Any(object):
    """Compound checker to check if any of provided checkers is true."""

    def __init__(self, *args):
        self.checkers = args

    def __call__(self):
        return any(c() for c in self.checkers)
