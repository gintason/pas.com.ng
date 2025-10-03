from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class PaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payments"

    def ready(self):
        from .models import SubscriptionPlan  # ✅ Correct model name

        plans = [
            {"name": "One Month", "duration_days": 30, "price": 10000},
            {"name": "Three Months", "duration_days": 90, "price": 20000},
            {"name": "Yearly", "duration_days": 365, "price": 25000},
        ]

        try:
            for plan in plans:
                SubscriptionPlan.objects.get_or_create(
                    name=plan["name"],
                    defaults={
                        "duration_days": plan["duration_days"],
                        "price": plan["price"],
                    },
                )
        except (OperationalError, ProgrammingError):
            # This prevents errors during `migrate` when the table doesn’t exist yet
            pass
