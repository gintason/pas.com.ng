from django.contrib import admin

from .models import Payment

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['amount', 'reference', 'email', 'verified', 'created_at']


admin.site.register(Payment, PaymentAdmin)
