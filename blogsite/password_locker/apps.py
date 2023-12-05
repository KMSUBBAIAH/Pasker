from django.apps import AppConfig


class PasswordLockerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'password_locker'

    def ready(self):
        import password_locker.signals