# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils import timezone

# ✅ Default expiry fallback (90 days if no plan is chosen)
def get_default_expiry():
    return now() + timedelta(days=90)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.PositiveIntegerField()  # price in Naira
    duration_days = models.PositiveIntegerField()  # e.g. 30, 90, 365

    def __str__(self):
        return f"{self.name} - ₦{self.price}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ expiry_date must point to a function, not an inline def
    expiry_date = models.DateTimeField(default=get_default_expiry)

    # ✅ link to subscription plan
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True
    )

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.amount} - Expires on {self.expiry_date}"

    def is_expired(self):
        return self.expiry_date and now() > self.expiry_date
    
    """Check if user already has an active, verified subscription"""
    def has_active_payment(user):
        return Payment.objects.filter(
            user=user,
            verified=True,
            status="success",
            expiry_date__gte=timezone.now()
        ).exists()

    def save(self, *args, **kwargs):
        # ✅ If plan is chosen and no expiry → set expiry from plan
        if self.plan and not self.expiry_date:
            self.expiry_date = now() + timedelta(days=self.plan.duration_days)

        # ✅ If no plan and no expiry → fallback to 90 days
        if not self.plan and not self.expiry_date:
            self.expiry_date = get_default_expiry()

        super().save(*args, **kwargs)