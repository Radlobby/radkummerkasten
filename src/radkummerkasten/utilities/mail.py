#!/usr/bin/env python3


"""Wrap flask_mail’s public API, send async in separate thread."""


import threading

import flask
import flask_mail
from flask_mail import Attachment, Connection, Message, email_dispatched

__all__ = [
    "Attachment",
    "Connection",
    "email_dispatched",
    "Mail",
    "Message",
]


def _send_async(application, message):
    with application.app_context():
        mail = flask.current_app.extensions["mail"]
        mail.send(message, sync=True)


def _send_message_async(application, *args, **kwargs):
    with application.app_context():
        mail = flask.current_app.extensions["mail"]
        message = Message(*args, **kwargs)
        mail.send(message, sync=True)


class _Mail(flask_mail._Mail):
    """Wrap flask_mail._Mail, send async in separate thread."""

    def send(self, message, sync=False):
        """
        Send a single message instance.

        If TESTING is True the message will not actually be sent.
        Asynchronous by default, pass sync=True to send in same thread.

        Arguments
        ---------
        message : flask_mail.Message
            The message to send.
        sync : bool
            Whether to send the message in the current thread
            (default: False).
        """
        if sync:  # pragma: no cover
            super().send(message)
        else:
            application = flask.current_app._get_current_object()
            thread = threading.Thread(
                target=_send_async,
                args=(application, message),
            )
            thread.start()

    def send_message(self, *args, sync=False, **kwargs):
        """
        Send a single message.

        Arguments
        ---------
        message : flask_mail.Message
            The message to send.
        """
        if sync:  # pragma: no cover
            super().send_message(*args, **kwargs)
        else:
            application = flask.current_app._get_current_object()
            thread = threading.Thread(
                target=_send_message_async,
                args=(application, *args),
                kwargs=kwargs,
            )
            thread.start()


class Mail(flask_mail.Mail):
    """Wrap flask_mail.Mail, send async in separate thread."""

    def init_mail(self, config, debug=False, testing=False):
        """Initialise mail extension."""
        return _Mail(
            config.get("MAIL_SERVER", "127.0.0.1"),
            config.get("MAIL_USERNAME"),
            config.get("MAIL_PASSWORD"),
            config.get("MAIL_PORT", 25),
            config.get("MAIL_USE_TLS", False),
            config.get("MAIL_USE_SSL", False),
            config.get("MAIL_DEFAULT_SENDER"),
            int(config.get("MAIL_DEBUG", debug)),
            config.get("MAIL_MAX_EMAILS"),
            config.get("MAIL_SUPPRESS_SEND", testing),
            config.get("MAIL_ASCII_ATTACHMENTS", False),
        )
