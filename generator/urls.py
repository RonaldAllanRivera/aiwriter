from django.urls import path
from .views import generate_view, history_view, buy_credits, create_checkout_session, payment_success


urlpatterns = [
    path("generate/", generate_view, name="generate"),
    path("history/", history_view, name="history"),
    path('buy-credits/', buy_credits, name='buy_credits'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('payment/success/', payment_success, name='payment_success'),    
]