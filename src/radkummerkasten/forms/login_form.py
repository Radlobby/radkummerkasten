#!/usr/bin/env python3


"""A login form."""

import wtforms


class LoginForm(wtforms.Form):
    """A login form."""

    email_address = wtforms.StringField(
        "E-mail address",
        validators=[wtforms.validators.Email()],
    )
