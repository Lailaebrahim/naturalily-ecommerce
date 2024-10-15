from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import DetailView, CreateView
from .models import Product, Category, Review, Offer
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import ReviewForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


# view for rendring template
def ListAllProductsView(request):
    return render(request, 'ProductApp/products.html')

# api end point for listing the products
def get_products(request):
    page_number = request.GET.get('page', 1)
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)

    data = {
        'products': [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'quantity_in_stock': product.quantity_in_stock,
                'reviews': product.getReviewsNum(),
                'image_url': product.img.url,
                'offer': product.offer.offer if product.offer else None,
                'discount': str(product.offer.discount) if product.offer else None,
                'product_url': request.build_absolute_uri(product.get_absolute_url())
            }
            for product in page_obj
        ],
        'has_next': page_obj.has_next(),
        'has_prev': page_obj.has_previous(),
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    }

    return JsonResponse(data)


def ListAllCategoriesView(request):
    categories = Category.objects.all()
    return render(request, 'ProductApp/categories.html', context={"categories": categories})


def ListCategoryProductsView(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, 'ProductApp/category_products.html', context={"category": category})


def get_category_products(request, category_id):
    page_number = request.GET.get('page', 1)
    products = Product.objects.filter(category=category_id)
    paginator = Paginator(products, 4)
    page_obj = paginator.get_page(page_number)

    data = {
        'products': [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'quantity_in_stock': product.quantity_in_stock,
                'reviews': product.getReviewsNum(),
                'image_url': product.img.url,
                'offer': product.offer.offer if product.offer else None,
                'discount': str(product.offer.discount) if product.offer else None,
                'product_url': request.build_absolute_uri(product.get_absolute_url())
            }
            for product in page_obj
        ],
        'has_next': page_obj.has_next(),
        'has_prev': page_obj.has_previous(),
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    }

    return JsonResponse(data)


class ProductDetailView(DetailView):
    model = Product
    template_name = "ProductApp/product.html"
    context_object_name = "product"


def ListAllProductReviews(request, pk):
    product = Product.objects.get(pk=pk)
    reviews = product.reviews.all
    return render(request, 'ProductApp/reviews.html', context={"product": product, "reviews": reviews})


@login_required
def deleteReview(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.shopUser != review.shopUser:
        raise PermissionDenied("You are not authorized to delete this review.")
    review.delete()
    return redirect(request.META.get('HTTP_REFERER', ''))


@login_required
def createReview(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.shopUser = request.user.shopUser
            review.save()
            return redirect('product', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'ProductApp/review.html', context={"product": product, "form": form})


@login_required
def updateReview(request, review_pk, product_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user.shopUser != review.shopUser:
        raise PermissionDenied("You are not authorized to update this review.")
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product', pk=review.product.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'ProductApp/review.html', context={"product": review.product, "form": form})


def ListAllOffersView(request):
    offers = Offer.objects.all()
    return render(request, 'ProductApp/offers.html', context={"offers": offers})
