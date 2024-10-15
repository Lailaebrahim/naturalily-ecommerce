from django.db import models
from UserApp.models import ShopUser


class Cart(models.Model):
    shopUser = models.OneToOneField(
        'UserApp.ShopUser', on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"{self.shopUser.user.username}'s cart"


class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('ProductApp.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in {self.cart.shopUser.user.username}'s cart"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ['cart', 'product']


class Order(models.Model):
    shopUser = models.ForeignKey(
        ShopUser, on_delete=models.CASCADE, related_name='orders')
    ordered_at = models.DateTimeField(auto_now_add=True)
    delivery_destination = models.TextField(max_length=200, null=False)
    STATE_CHOICES = [('In-Progress', 'In-Progress'),
                     ('In-Delivery', 'In-Delivery'),
                     ('Delivered', 'Delivered')]
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default='In-Progress')
    PAYMENT_CHOICES = [('cashOnDelivery', 'cashOnDelivery'),
                       ('creditCard', 'creditCard')]
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default='cashOnDelivery')
    total_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=False)
    firstname = models.CharField(max_length=150, null=False)
    lastname = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return f"{self.shopUser.user.username}'s order {self.pk}"

    class Meta:
        ordering = ['-ordered_at']


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('ProductApp.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in {self.order.shopUser.user.username}'s order {self.order.pk}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ['order', 'product']


class WishList(models.Model):
    shopUser = models.OneToOneField(
        ShopUser, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"{self.shopUser.user.username}'s wish list"


class WishListProduct(models.Model):
    wishList = models.ForeignKey(
        WishList, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('ProductApp.Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.wishList.shopUser.user.username}'s wish list"
