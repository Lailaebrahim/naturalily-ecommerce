from django.contrib import admin
from .models import Cart, CartProduct, Order, OrderProduct, WishList, WishListProduct

admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(WishList)
admin.site.register(WishListProduct)
