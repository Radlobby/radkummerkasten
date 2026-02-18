#!/usr/bin/env python3


"""Authenticate users via tokens sent to their e-mail."""


import datetime
# import hashlib
# import hmac
# import secrets

import flask

from ..database import Database
from ..database.models import (
    User,
    Token,
)
from ..utilities.mail import Mail

__all__ = ["PasswordlessAuthentication"]


class PasswordlessAuthentication:
    """Authenticate users via tokens sent to their e-mail."""

    # secret_key = None

    # def __init__(self, secret_key=None):
    #     """Authenticate users via tokens sent to their e-mail."""
    #     if secret_key is None:
    #         self.secret_key = secrets.token_hex(32)
    #     else:
    #         self.secret_key = secret_key

    @property
    def database(self):
        """Retrieve a radkummerkasten.database.Database instance."""
        database = flask.current_app.extensions[Database.EXTENSION_NAME]
        return database

    @property
    def mail(self):
        """Retrieve a radkummerkasten.utilities.mail.Mail instance."""
        mail = flask.current_app.extensions[Mail.EXTENSION_NAME]
        return mail

    # def _hash_token(self, token):
    #     token_hash = hmac.new(
    #         self.secret_key.encode(),
    #         token.encode(),
    #         hashlib.sha256,
    #     ).hexdigest()
    #     return token_hash

    def send_magic_link(self, email, next_url=None):
        """Send an email with a magic link."""
        if next_url is None:
            next_url = flask.url_for("radkummerkasten.radkummerkasten")
        with self.database.session.begin() as session:
            user = session.find(User, email_address=email)
            if user is None:
                user = User(email_address=email)
            token = Token(user=user, next_url=next_url)
            token_ = token.token
            session.add(user)
            session.add(token)
            session.commit()

        mail = flask.current_app.extensions["mail"]
        mail.send_message(
            subject="Radkummerkasten: login link",
            recipients=[email,],
            body=flask.render_template(
                "magic_link_email.txt.jinja",
                token=token_,
            )
        )

    def verify_magic_link(self, token):
        """Check a submitted token."""
        with self.database.session.begin() as session:
            token = session.find(
                Token,
                token=token,
                used=None,
            )
            if (
                token is not None
                and token.expires > datetime.datetime.now()
            ):
                flask.session["user"] = token.user.id
                token.used = datetime.datetime.now()
                session.add(token)
                session.commit()
                return True
            else:
                return False
