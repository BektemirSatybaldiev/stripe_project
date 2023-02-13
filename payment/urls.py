from django.urls import path
from . import views

app_name = "item"

urlpatterns = [
    path("buy/<int:item_id>/", views.buy_item, name="buy_item"),
    path("item/<int:item_id>/", views.item_detail, name="item_detail"),
]