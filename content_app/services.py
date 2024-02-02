from pprint import pprint

import stripe
import os

from django.core.mail import send_mail
from dotenv import load_dotenv

from config.settings import BASE_DIR


def create_paymentintent(amount):
    paymentinrtent = stripe.PaymentIntent.create(
      amount=amount,
      currency="usd",
      automatic_payment_methods={"enabled": True},
    )
    pprint(paymentinrtent)


def retrieve_paymentintent(paymentintent: dict) -> dict:
    paymentintent = stripe.PaymentIntent.retrieve(
        paymentintent['id'],
    )
    return paymentintent


def create_product(product_name):
    product = stripe.Product.create(name=product_name)
    return product


def create_price(product: dict, amount: int) -> dict:
    price = stripe.Price.create(
        unit_amount=amount*100,
        currency="usd",
        recurring={"interval": "month"},
        product=product['id'],
    )
    return price


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price['id'],
                "quantity": 1,
            },
        ],
        mode="subscription",
    )
    return session


def create_paymentmethod(card):
    payment_method = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": card['number'],
            "exp_month": card['exp_month'],
            "exp_year": card['exp_year'],
            "cvc": card['cvc'],
        },
    )
    return payment_method



if __name__ == '__main__':
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    product = create_product('Лёха-plus')
    price = create_price(product, 200)
    session = create_session(price)
    pprint(session['url'])
    card = {
        'number': '424242424242',
        'exp_month': 12,
        'exp_year': 2030,
        'cvc': '122'
    }
    payment_method = create_paymentmethod(card)
