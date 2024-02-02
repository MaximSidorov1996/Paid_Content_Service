import os

import stripe
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from content_app.models import Payment
from content_app.services import create_product, create_price
from users.forms import UserRegisterForm, UserLoginForm
from users.models import User

stripe.api_key = os.getenv('STRIPE_API_KEY')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm

    def get_success_url(self):
        return reverse_lazy('content_app:home')

    def form_valid(self, form):
        product = create_product('ContentPlus')
        price = create_price(product, 200)
        self.object = form.save()
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": price,
                    "quantity": 1,
                },
            ],
            metadata={
                "user_id": self.object.id
            },
            mode="subscription",
            success_url=os.getenv('YOUR_DOMAIN') + '/users/success/',
            cancel_url=os.getenv('YOUR_DOMAIN') + '/users/cancel/',
        )
        Payment.objects.create(user_id=self.object.id, session_id=session['id'])
        form.save()
        return redirect(session['url'])


class SuccessView(TemplateView):
    template_name = 'users/success.html'

    def post(self, request):
        try:
            phone_number = request.POST.get('number_phone')
            try:
                user = User.objects.get(phone_number=phone_number)
            except Exception:
                return redirect('users:cancel')
            session_id = Payment.objects.get(user_id=user.id).session_id
            session = stripe.checkout.Session.retrieve(
                    session_id,
                )
            if session['payment_status']:
                user.is_active = True
                user.save()
                payment = Payment.objects.get(user=user)
                payment.success = True
                payment.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return reverse_lazy('users:cancel')
        except KeyError:
            return redirect('content_app:home')

    def get_success_url(self):
        return reverse_lazy('content_app:home')


class CancelView(TemplateView):
    template_name = "cancel.html"


class CustomLoginView(LoginView):
    model = User
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('content_app:home')



