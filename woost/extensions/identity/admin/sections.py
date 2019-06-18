"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.events import when
from cocktail.translations import translations
from woost.admin.sections.settings import Settings
from woost.admin.sections.contentsection import ContentSection

translations.load_bundle("woost.extensions.identity.admin.sections")


class IdentitySettings(Settings):
    icon_uri = (
        "woost.extensions.identity.admin.ui://"
        "images/sections/identity.svg"
    )
    members = [
        "x_identity_providers"
    ]


@when(ContentSection.declared)
def fill(e):
    e.source.append(IdentitySettings("x-identity"))

