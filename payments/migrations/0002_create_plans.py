from django.db import migrations

def create_default_plans(apps, schema_editor):
    SubscriptionPlan = apps.get_model("payments", "SubscriptionPlan")
    plans = [
        {"name": "Monthly", "price": 10000, "duration_days": 30},
        {"name": "Quarterly", "price": 20000, "duration_days": 90},
        {"name": "Yearly", "price": 25000, "duration_days": 365},
    ]
    for p in plans:
        SubscriptionPlan.objects.update_or_create(name=p["name"], defaults=p)

class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_plans),
    ]
