from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import PaymentForm
from django.conf import settings
from .models import Payment
from django.contrib import messages

# Create your views here.


def initiate_payment(request):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, "make_payments.html", {'payment': payment,
                                                          'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = PaymentForm()
    return render(request, "initiate_payments.html", {'payment_form': payment_form})


def verify_payment(request, ref: str):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification Successful")
    else:
        messages.error(request, "Verification Failed")
    return redirect('initiate-payment')