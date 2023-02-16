from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ItemView, BuyView,CartView, payment_intent, checkout

app_name = 'payment'

urlpatterns = [
    path("buy/<int:item_id>/", BuyView.as_view(), name="buy"),
    path("item/<int:item_id>/", ItemView.as_view(), name="item"),
    path('checkout/', checkout, name='checkout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('intent/', payment_intent, name='payment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)