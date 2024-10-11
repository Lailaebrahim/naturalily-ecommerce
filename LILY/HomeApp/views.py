from django.shortcuts import render
from ProductApp.models import Product


def home(request):
    recentProducts = Product.objects.order_by('-added_at')[:6]
    lessthanProducts = Product.objects.filter(price__lt=200)
    return render(request, 'home/home.html', context={"recentProducts": recentProducts,  "lessthanProducts": lessthanProducts})
