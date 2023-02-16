import os
from dotenv import load_dotenv
import json
import stripe
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Order
from django.http import HttpResponseNotAllowed

load_dotenv()
stripe.api_key = os.environ.get('API')


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, "index.html", {"orders": orders})


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=self.request.user)
        return render(request, "cart.html", {"orders": orders})


class BuyView(View):
    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        product = stripe.Product.create(
            name=str(item.name),
            description=str(item.description),
        )
        price = stripe.Price.create(
            unit_amount=item.price,
            currency="usd",
            product=product['id'],
        )
        session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=["card"],
            line_items=[{
                "price": price['id'],
                "quantity": 1,
            }],
            success_url="http://localhost:8000/success",
            cancel_url="http://localhost:8000/cancel",
        )
        return JsonResponse({"session_id": session.id})


class ItemView(View):
    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        return render(request, "buy_item.html", {"item": item})


def checkout(request):
    stripe.api_key = os.environ.get('SECRET_KEY')
    intent = stripe.PaymentIntent.create(amount=1000, currency='usd')
    client_secret = intent.client_secret
    orders = Order.objects.filter(user=request.user)
    context = {'client_secret': client_secret, 'orders': orders}
    return render(request, 'checkout.html', context)


@csrf_exempt
def payment_intent(request):
    if request.user.is_authenticated:
        order = Order.objects.get(user=request.user)
        total = order.total_amount()
        stripe.api_key = os.environ.get('API')
        if request.method == "POST":
            data = json.loads(request.body)
            customer = stripe.Customer.create(
                name="Jenny",
                address={
                    "line1": "510 Townsend St",
                    "postal_code": "98140",
                    "city": "San Francisco",
                    "state": "CA",
                    "country": "US",
                },
            )
            intent = stripe.PaymentIntent.create(
                amount=total,
                customer=customer['id'],
                currency=data['currency'],
                metadata={'cart_id': Order.objects.get(user=request.user).id},
                description="testing "
            )
            try:
                return JsonResponse({'publishableKey':
                                         os.environ.get('PUB_KEY'), 'clientSecret': intent.client_secret})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=403)
        else:
            return HttpResponseNotAllowed(['POST'], 'Only POST requests are allowed.')


def payment_complete(request):
    if request.method == "POST":
        data = json.loads(request.POST.get("payload"))
        if data["status"] == "succeeded":
            return render(request, "payment-complete.html")
