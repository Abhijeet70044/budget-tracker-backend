from django.apps import AppConfig
from django.db.utils import OperationalError

class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'

    def ready(self):
        from .models import Category
        try:
            if not Category.objects.filter(name="Income").exists():
                Category.objects.create(name="Income")
            if not Category.objects.filter(name="Expense").exists():
                Category.objects.create(name="Expense")
        except OperationalError:
            # Database not ready yet (e.g. during migrations)
            pass
