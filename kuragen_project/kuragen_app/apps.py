from django.apps import AppConfig
from django.db.models.signals import post_migrate



class KuragenAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kuragen_app'

    def ready(self):
        from .models import set_default_data
        post_migrate.connect(set_default_data, sender=self)

