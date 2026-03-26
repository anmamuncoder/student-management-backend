from django.apps import AppConfig

class RbacConfig(AppConfig):
    name = 'apps.rbac'
    verbose_name = 'Role-Based Access Control'

    def ready(self):
        import apps.rbac.signals
