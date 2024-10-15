from django.urls import path
from . import views

urlpatterns = [
    path('api/add-to-cart/', views.AddToCart, name='add_to_cart'),
    path('api/add-to-wishlist/', views.AddToWishList, name='add_to_wishlist'),
    path('api/get-count/', views.getUserCounts, name="get_count"),
    path('api/inc-check/', views.incCheckQuantity, name="inc_check_quantity"),
    path('api/dec-check/', views.decCheckQuantity, name="dec_check_quantity"),
    path('api/remove-from-cart/', views.removeCartItem, name="remove_from_cart"),
    path('api/remove-from-wishlist/', views.removeWish,
         name="remove_from_wishlist"),
    path('create-checkout-session/', views.createCheckoutSessionView.as_view(),
         name="create_checkout_session"),
    path('', views.placeOrder, name="place_order"),
    path('api/order-accepted/', views.orderAccepted, name="order_accepted"),
    path('details/<int:pk>/',  views.orderDetailView.as_view(), name="order_details"),
    path('history/',  views.orderHistoryView.as_view(), name="orders_history"),

]
