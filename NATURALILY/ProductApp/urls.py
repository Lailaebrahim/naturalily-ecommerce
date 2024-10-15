from django.urls import path
from . import views

urlpatterns = [
    path("all/", views.ListAllProductsView, name="collection"),
    path("categories/", views.ListAllCategoriesView, name="categories"),
    path("category/<int:category_id>/",
         views.ListCategoryProductsView, name="category_products"),
    path('<int:pk>/', views.ProductDetailView.as_view(), name="product"),
    path('<int:pk>/reviews/', views.ListAllProductReviews, name="reviews"),
    path('<int:pk>/review/create/', views.createReview, name="review_create"),
    path('<int:product_pk>/review/<int:review_pk>/update/',
         views.updateReview, name="review_update"),
    path('offers/', views.ListAllOffersView, name="offers"),
    path('api/review/<int:pk>/delete', views.deleteReview, name="review_delete"),
    path('api/products/', views.get_products, name='get_products'),
    path('api/categoryProducts/<int:category_id>/', views.get_category_products,
         name="get_category_products"),
]
