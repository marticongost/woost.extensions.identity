#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from woost.models import add_setting, Configuration
from .identityprovider import IdentityProvider

translations.load_bundle("woost.extensions.identity.settings")

add_setting(
    schema.Collection(
        "x_identity_providers",
        items=schema.Reference(type=IdentityProvider),
        integral=True,
        bidirectional=True
    ),
    scopes = (Configuration,)
)

