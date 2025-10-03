# views.py
import hashlib
import hmac
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
import json
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Payment,  SubscriptionPlan
import requests 
import random
from django.contrib import messages
import string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .utils import generate_reference  # Assume this function generates a unique reference
from payments.utils import generate_reference
from django.views.decorators.http import require_POST
import logging
from django.utils import timezone
from django.contrib import messages



logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()


def generate_reference():
    """Generate a unique reference for the transaction"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=12))


@login_required
def initialize_payment(request):
    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            messages.error(request, "Invalid subscription plan selected.")
            return redirect("payments:payment_page")

        # 🔒 Check if user already has ANY active verified subscription
        active_payment = Payment.objects.filter(
            user=request.user,
            verified=True,
            status="success",
            expiry_date__gte=timezone.now()
        ).first()

        if active_payment:
            messages.warning(
                request,
                f"🚫 You already have an active {active_payment.plan.name} plan "
                f"until {active_payment.expiry_date:%Y-%m-%d}."
            )
            return redirect("pasApp:levels")  # redirect where user should continue

        # ✅ No active subscription → proceed with Paystack init
        amount = plan.price  # in Naira
        email = request.user.email
        amount_in_kobo = amount * 100
        reference = generate_reference()

        # Expiry based on selected plan
        expiry_date = timezone.now() + timedelta(days=plan.duration_days)

        # Save payment with plan
        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            reference=reference,
            email=email,
            expiry_date=expiry_date,
            plan=plan
        )

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_LIVE_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": amount_in_kobo,
            "reference": reference,
            "callback_url": request.build_absolute_uri(reverse("payments:success")),
        }

        response = requests.post(
            settings.PAYSTACK_INITIALIZE_PAYMENT_URL, json=data, headers=headers
        )
        response_data = response.json()

        if response_data["status"]:
            return redirect(response_data["data"]["authorization_url"])
        else:
            return JsonResponse({"error": "Payment initialization failed"}, status=400)

    # ✅ Pass plans to template
    plans = SubscriptionPlan.objects.all()

    active_payment = Payment.objects.filter(
        user=request.user,
        verified=True,
        status="success",
        expiry_date__gte=timezone.now()
    ).first()

    return render(request, "payments/payment_page.html", {"plans": plans,  "active_payment": active_payment, })


@login_required
def verify_payment(request):
    reference = request.GET.get("reference")

    if not reference:
        return redirect("payments:cancelled")  # If no reference, treat it as failed

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_LIVE_SECRET_KEY}"
    }

    response = requests.get(f"{settings.PAYSTACK_VERIFY_URL}{reference}", headers=headers)
    response_data = response.json()

    if response_data.get("status") and response_data["data"].get("status") == "success":
        try:
            payment = Payment.objects.get(reference=reference)
            payment.verified = True
            payment.status = "success"
            payment.save()
            return redirect("payments:payment_success")  # Redirect to success page
        except Payment.DoesNotExist:
            return redirect("payments:cancelled")  # Fallback if payment not found
    else:
        try:
            # Optional: mark it as failed
            payment = Payment.objects.get(reference=reference)
            payment.status = "failed"
            payment.save()
        except Payment.DoesNotExist:
            pass  # It's okay if payment record wasn't created
        return redirect("payments:cancelled")
    

def success_view(request):
    # Retrieve the stored product ID from the session
    product_id = request.session.get('product_id')

    # Verify payment using Paystack
    reference = request.GET.get('reference')
    if reference:
        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            messages.error(request, "Payment record not found.")
        else:
            # Verify with Paystack
            headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_LIVE_SECRET_KEY}"
            }
            verify_url = f"{settings.PAYSTACK_VERIFY_URL}{reference}"

            response = requests.get(verify_url, headers=headers)
            data = response.json()

            if data['status'] and data['data']['status'] == "success":
                payment.verified = True
                payment.status = "success"
                payment.save()
                messages.success(request, "Payment verified successfully!")
            else:
                payment.status = "failed"
                payment.save()
                messages.error(request, "Payment verification failed.")

    context = {'product_id': product_id}
    return render(request, 'payments/success.html', context)


def payment_cancelled(request):
    
    return render(request, "payments/cancelled.html")

@csrf_exempt
@require_POST
def paystack_webhook(request):
    """Handles Paystack webhook events with security validation"""
    secret_key = settings.PAYSTACK_LIVE_SECRET_KEY.encode()
    signature = request.headers.get("X-Paystack-Signature")

    payload = request.body
    computed_signature = hmac.new(secret_key, payload, hashlib.sha512).hexdigest()

    if signature != computed_signature:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    try:
        data = json.loads(payload)
        event = data.get("event")

        if event == "charge.success":
            reference = data["data"]["reference"]
            if Payment.objects.filter(reference=reference).exists():
                payment = Payment.objects.get(reference=reference)
                if not payment.verified:  # Prevent duplicate verification
                    payment.verified = True
                    payment.status = 'success'
                    payment.save()
                    logger.info(f"Payment verified via webhook: {reference}")
                return JsonResponse({"message": "Payment verified successfully"}, status=200)

        return JsonResponse({"message": "Event received"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)


@login_required
def dashboard(request):
    user = request.user
    
    # If user is admin, skip payment check
    if user.is_superuser or user.is_staff:
        return render(request, "pasApp/interview_levels.html", {"admin_access": True})

    # Normal users → check for active payment
    active_payment = Payment.objects.filter(
        user=user, 
        is_active=True
    ).first()

    if not active_payment:
        return redirect("pasApp:home")

    return render(request, "pasApp/interview_levels.html", {"active_payment": active_payment})