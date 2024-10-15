from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Cart, CartProduct, WishList, WishListProduct, Order, OrderProduct
from django.http import JsonResponse
from ProductApp.models import Product
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect


@login_required
def AddToCart(request):
    product_pk = request.GET.get('productPk')
    cart, created = Cart.objects.get_or_create(shopUser=request.user.shopUser)

    if not product_pk:
        return JsonResponse({'status': '404', 'message': 'Product not specified'})

    product = get_object_or_404(Product, pk=product_pk)

    if product.quantity_in_stock == 0:
        return JsonResponse({'status': '400', 'message': 'Product out of stock'})

    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_product.quantity + 1 > product.quantity_in_stock:
            return JsonResponse({'status': '400', 'message': 'Product out of stock'})
        cart_product.quantity += 1

    cart_product.save()
    cart_count = cart.products.count()
    cart_total = sum([product.total_price for product in cart.products.all()])

    return JsonResponse({
        'status': '201',
        'message': 'Product added to cart successfully',
        'quantity': cart_product.quantity,
        'cart_count': cart_count,
        'cart_total': cart_total,
    })


@login_required
def AddToWishList(request):
    product_pk = request.GET.get('productPk')
    wishList, created = WishList.objects.get_or_create(
        shopUser=request.user.shopUser)

    if not product_pk:
        return JsonResponse({'status': '404', 'message': 'Product not specified'})

    product = get_object_or_404(Product, pk=product_pk)

    wishList_product, created = WishListProduct.objects.get_or_create(
        wishList=wishList,
        product=product,
    )

    if not created:
        return JsonResponse({'status': '200', 'message': 'already in wishlist'})

    wishList_product.save()

    wishlist_count = wishList.products.count()

    return JsonResponse({
        'status': '201',
        'message': 'Product added to WishList successfully',
        'wishlist_count': wishlist_count,
    })


def getUserCounts(request):
    try:
        if request.user.shopUser:
            cart, _ = Cart.objects.get_or_create(
                shopUser=request.user.shopUser)
            wishlist, _ = WishList.objects.get_or_create(
                shopUser=request.user.shopUser)
            cart_count = cart.products.count()
            wishlist_count = wishlist.products.count()
            cart_total = sum(
                [product.total_price for product in cart.products.all()])
            return JsonResponse({'cart_count': cart_count, 'wishlist_count': wishlist_count, 'cart_total': cart_total})
    except:
        return JsonResponse({'cart_count': 0, 'wishlist_count': 0, 'cart_total': 0})


@login_required
def incCheckQuantity(request):
    product_pk = request.GET.get('productPk')
    if not product_pk:
        return JsonResponse({'status': '404', 'message': 'Product not specified'})

    cart = get_object_or_404(Cart, shopUser=request.user.shopUser)
    product = get_object_or_404(Product, pk=product_pk)
    cart_product = get_object_or_404(
        CartProduct, cart=cart, product=product)

    if product.quantity_in_stock == 0 or product.quantity_in_stock < cart_product.quantity + 1:
        return JsonResponse({'status': '400', 'message': 'No more stock available'})

    cart_product.quantity += 1
    cart_product.save()

    cart_count = cart.products.count()
    cart_total = sum([product.total_price for product in cart.products.all()])

    return JsonResponse({
        'status': '200',
        'message': 'Product quantity increased successfully',
        'quantity': cart_product.quantity,
        'cart_count': cart_count,
        'cart_total': cart_total,
    })


@login_required
def decCheckQuantity(request):
    product_pk = request.GET.get('productPk')
    if not product_pk:
        return JsonResponse({'status': '404', 'message': 'Product not specified'})

    cart = get_object_or_404(Cart, shopUser=request.user.shopUser)
    product = get_object_or_404(Product, pk=product_pk)
    cart_product = get_object_or_404(
        CartProduct, cart=cart, product=product)

    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
        cart.save()
        quantity = cart_product.quantity
    else:
        cart_product.delete()
        quantity = 0

    cart_count = cart.products.count()
    cart_total = sum([product.total_price for product in cart.products.all()])

    return JsonResponse({
        'status': '200',
        'message': 'Product quantity decreased successfully',
        'quantity': quantity,
        'cart_count': cart_count,
        'cart_total': cart_total,
    })


@login_required
def removeWish(request):
    product_pk = request.GET.get('productPk')
    if not product_pk:
        return JsonResponse({'status': '404', 'message': 'Product not specified'})

    wishlist = get_object_or_404(WishList, shopUser=request.user.shopUser)
    product = get_object_or_404(Product, pk=product_pk)
    wishlist_product = get_object_or_404(
        WishListProduct, wishList=wishlist, product=product)

    wishlist_product.delete()
    wishlist.save()
    wishlist_count = wishlist.products.count()
    return JsonResponse({'status': '200', 'message': 'Product removed from wishlist', 'wishlist_count': wishlist_count})


@login_required
def removeCartItem(request):
    product_pk = request.GET.get('productPk')
    if not product_pk:
        return JsonResponse({'status': '404', 'message': 'Product not specified'})

    cart = get_object_or_404(Cart, shopUser=request.user.shopUser)
    product = get_object_or_404(Product, pk=product_pk)
    cart_product = get_object_or_404(CartProduct, cart=cart, product=product)

    cart_product.delete()
    cart.save()
    cart_count = cart.products.count()
    return JsonResponse({'status': '200', 'message': 'Product removed from cart', 'cart_count': cart_count, 'cart_total': sum([product.total_price for product in cart.products.all()])})


@login_required
def placeOrder(request):
    cart = get_object_or_404(Cart, shopUser=request.user.shopUser)
    cart_products = cart.products.all()
    total_price = sum([product.total_price for product in cart_products])
    return render(request, 'OrderApp/place_order.html', {'cart_products': cart_products, 'total_price': total_price})

@login_required
def orderAccepted(request):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    addresse = request.POST.get("addresse")
    phone = request.POST.get("phone")
    payment_method = request.POST.get("payment_method")
    cart = get_object_or_404(Cart, shopUser=request.user.shopUser)
    order = Order.objects.create(
        shopUser=request.user.shopUser,
        firstname=firstname,
        lastname=lastname,
        delivery_destination=addresse,
        phone=phone,
        payment_method=payment_method,
        total_price=sum([product.total_price for product in cart.products.all()])
    )

    for cart_product in cart.products.all():
        order_product = OrderProduct.objects.create(
            order=order, product=cart_product.product)
        order.products.add(order_product)
        cart_product.delete()

    cart.delete()
    order.save()

    return redirect('order_details', pk=order.pk)

    
class orderDetailView(DetailView, LoginRequiredMixin):
    model = Order
    template_name = "OrderApp/order_details.html"


class orderHistoryView(ListView, LoginRequiredMixin):
    model = Order
    template_name = "OrderApp/order_history.html"
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(shopUser=self.request.user.shopUser).order_by('-ordered_at')
    