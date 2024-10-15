from django.db import models
from UserApp.models import ShopUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    category = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = 'Categories'


class Offer(models.Model):
    offer = models.CharField(max_length=100, null=False)
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return self.offer

    class Meta:
        verbose_name_plural = 'Offers'


class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=500, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    quantity_in_stock = models.IntegerField(null=False)
    img = models.ImageField(upload_to='images/products/',
                            default='images/products/default.png')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    added_at = models.DateTimeField(auto_now_add=True)
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='products', null=True)

    def __str__(self):
        return self.name

    def getReviewsNum(self):
        return self.reviews.count()

    def get_absolute_url(self):
        return f'/product/{self.id}/'

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['-added_at']


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    shopUser = models.ForeignKey(
        ShopUser, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField(null=False)
    rating = models.IntegerField(
        null=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"review: {self.shopUser.user.username} on {self.product.name}"

    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-added_at']
