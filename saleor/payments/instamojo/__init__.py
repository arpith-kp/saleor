
import logging

from django.contrib.sites.models import Site
from django.utils.translation import pgettext_lazy
from django.contrib import messages

from instamojo_wrapper import Instamojo

from payments import PaymentStatus, RedirectNeeded
from payments.core import BasicProvider

from saleor.payments.instamojo.environment import Environment

logger = logging.getLogger(__name__)


class InstaMojoProvider(BasicProvider):

    def __init__(self,  public_key, private_auth_token,sandbox="True",
                 endpoint='instamojo.com/api/1.1/', **kwargs):

        self.public_key = public_key
        self.private_auth_token = private_auth_token
        self.sandbox = sandbox

        if sandbox == 'True':
            self.endpoint = 'https://test.' + endpoint
        else:
            self.endpoint = 'https://www.' + endpoint

        super(InstaMojoProvider, self).__init__(**kwargs)

    def _get_links(self, payment):
        api = Instamojo(api_key=self.public_key,
                        auth_token=self.private_auth_token,
                        endpoint=self.endpoint)
        current_site = Site.objects.get_current()
        insta_response = api.payment_request_create(
            buyer_name=payment.order.user.get_full_name(),
            phone=payment.order.billing_address.phone.as_e164,
            amount=payment.total,
            send_email=True,
            email=payment.order.user.email,
            redirect_url='http://' + current_site.domain + '/payment/' + payment.order.token + '/gateway/status',
            purpose='Payment'
        )
        transaction_id = insta_response.get('payment_request', {}).get('id')
        if not insta_response.get("success") or transaction_id is None:
            raise Exception("Unable to contact payment gateway")
        payment.transaction_id = transaction_id
        extra_data = {'links': {
            'approval_url': {'href': insta_response.get('payment_request', {}).get('longurl')},
        }}
        links = extra_data.get('links', {})
        return links

    def get_form(self, payment, data=None):
        if not payment.id:
            payment.save()

        links = self._get_links(payment)
        redirect_to = links.get('approval_url')
        payment.change_status(PaymentStatus.WAITING)
        raise RedirectNeeded(redirect_to['href'])
