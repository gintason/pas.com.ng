from django.shortcuts import redirect
from .models import Payment
from datetime import datetime
import uuid

def subscription_required(view_func):
    """Decorator to restrict access if subscription has expired."""
    def wrapper(request, *args, **kwargs):
        payment = Payment.objects.filter(user=request.user).order_by('-expiry_date').first()
        
        if not payment or payment.is_expired():
            return redirect("payments:pay")  # Redirect to subscription page
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def generate_reference():
    """Generates a unique reference ID for payment transactions."""
    return str(uuid.uuid4())  # Generates a unique string