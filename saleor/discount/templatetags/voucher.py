from django import template
from django_prices.templatetags import prices_i18n
from prices import Amount, Price

register = template.Library()


@register.simple_tag
def discount_as_negative(discount, html=False):
    zero = Amount(0, currency=discount.amount.currency)
    return prices_i18n.amount(zero - discount.amount,
                              'html' if html else 'text')
