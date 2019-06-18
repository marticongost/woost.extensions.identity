"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.persistence import migration_step


@migration_step
def import_woost2_data(e):

    from woost.models import Configuration, User

    config = Configuration.instance

    try:
        providers = config._identity_providers
    except AttributeError:
        pass
    else:
        del config._identity_providers
        for provider in providers:
            del provider._Configuration_identity_providers
        config.x_identity_providers = list(providers)

    for user in User.select():
        for provider in "facebook", "google":
            key = provider + "_user_id"
            old_key = "_" + key
            new_key = "x_identity_" + key
            try:
                value = getattr(user, old_key)
            except AttributeError:
                pass
            else:
                delattr(user, old_key)
                setattr(user, new_key, value)

