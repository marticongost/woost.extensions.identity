#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from woost.models import User

translations.load_bundle("woost.extensions.identity.google.user")

User.add_member(
    schema.String("x_identity_google_user_id",
        indexed = True,
        unique = True,
        editable = schema.NOT_EDITABLE,
        listed_by_default = False,
        member_group = "administration"
    )
)

