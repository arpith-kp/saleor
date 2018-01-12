from django import template
from prices import Price

register = template.Library()


# FIXME: remove stopgap function
from saleor.prices_stopgap import gross


@register.simple_tag
def discount_as_negative(discount, html=False):
    zero = Price(0, currency=discount.amount.currency)
    return gross(zero-discount.amount, html=html)
