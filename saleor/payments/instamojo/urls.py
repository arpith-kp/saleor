from django.conf.urls import url

from saleor.core import TOKEN_PATTERN
from . import views


urlpatterns = [
    url(r'^%s/gateway/status$' % (TOKEN_PATTERN,),
        views.payment_status, name='payment-status')
]
