"""
Stopgap for making old code run with new django_prices

Temp dev util, not to use in long run
"""

from django_prices.templatetags.prices_i18n import amount


def net(price, html=False, normalize=False):
    return amount(price.net, 'html' if html else 'text')


def gross(price, html=False, normalize=False):
    return amount(price.gross, 'html' if html else 'text')
