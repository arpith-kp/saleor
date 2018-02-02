from django.http import HttpResponseRedirect
from instamojo_wrapper import Instamojo
from payments import PaymentStatus
from payments.core import provider_factory

from saleor.order.models import Order, Payment
from django.shortcuts import get_object_or_404, redirect


def payment_status(request, token):
    payment_request_id = request.GET.get('payment_request_id')
    gateway_payment_id = request.GET.get('payment_id')

    #orders = Order.objects.prefetch_related('groups__lines__product')
    #orders = orders.select_related('billing_address', 'shipping_address', 'user')
    #order = get_object_or_404(orders, token=token)
    #payments = order.payments.filter(status=PaymentStatus.WAITING).exists()

    payment_queryset = Payment.objects.filter(transaction_id=payment_request_id)

    if payment_queryset.exists():
        payment = payment_queryset[0]
    else:
        raise Exception("Unable to get payment details")

    provider = provider_factory(payment.variant)
    api = Instamojo(api_key=provider.public_key,
                    auth_token=provider.private_auth_token,
                    #endpoint=provider.endpoint,
                    )
    payment_confirmation = api.payment_request_status(payment.transaction_id)
    if payment_confirmation.get('payment_request',{}).get('status') == 'Completed':
        payment.captured_amount = payment.total
        payment.change_status(PaymentStatus.CONFIRMED)
        return HttpResponseRedirect(payment.get_success_url())
    else:
        return HttpResponseRedirect(payment.get_failure_url())
