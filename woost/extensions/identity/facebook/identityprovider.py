# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
from urllib.parse import urlencode

from cocktail import schema
from cocktail.controllers import get_request_url

from woost.extensions.identity.identityprovider import IdentityProvider


class FacebookIdentityProvider(IdentityProvider):
    provider_name = "Facebook"
    user_identifier = "x_identity_facebook_user_id"

    members_order = [
        "client_id",
        "client_secret",
        "scope"
    ]

    client_id = schema.String(
        required=True,
        text_search=False
    )

    client_secret = schema.String(
        required=True,
        text_search=False
    )

    scope = schema.Collection(
        min=1,
        default=schema.DynamicDefault(lambda: ["public_profile", "email"]),
        items=schema.String()
    )

    def get_auth_url(self, target_url = None):
        return (
            "/facebook_oauth/%d/step1?%s" % (
                self.id,
                urlencode({
                    "target_url": target_url or get_request_url()
                })
            )
        )

