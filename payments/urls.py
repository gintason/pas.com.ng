from django.urls import path
from .views import paystack_webhook

from . import views
app_name = 'payments'

urlpatterns = [
   
    path('pay/', views.initialize_payment, name='pay'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('success/', views.success_view, name='success'), #new
    path("paystack/webhook/", paystack_webhook, name="paystack_webhook"),
    path("payment-cancelled/", views.payment_cancelled, name="cancelled"),
     
]
