from django.conf import settings

from django_prices import Price


def get_price_from_amount(amount, tax=None):
    try:
        price = Price(net=amount, gross=amount)
        if not settings.PRICES_INCLUDE_TAX:
            pass
        return price 
    except AttributeError:
        return amount
