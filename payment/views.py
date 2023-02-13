import stripe
from django.http import JsonResponse
from django.shortcuts import render
from .models import Item

stripe.api_key = "sk_test_51MaywVCTiAKboEl7zP73fHSS23ruhPmJjLiruBp9O99ZKxd5xDQaqJDCfUABtPPT5cvihrIWfKacsLqnR1Xmv4fz007NZxxfNG"


def buy_item(request, item_id):
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


def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, "item_detail.html", {"item": item})
