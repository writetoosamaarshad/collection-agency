from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the 'accounts' application.

    This class is used to configure some of the settings for the 'accounts' app,
    such as the default auto field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

