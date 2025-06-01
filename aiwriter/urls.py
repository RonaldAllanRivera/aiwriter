from django.contrib import admin
from django.urls import path, include
from generator.views import (
    home_view,
    generate_view,
    history_view,
    buy_credits,
    create_checkout_session,
    payment_success,
    stripe_webhook,
)

urlpatterns = [
    path("", home_view, name="home"),
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),  # AllAuth entry point
    path("generate/", generate_view, name="generate"),
    path("history/", history_view, name="history"),
    path("buy-credits/", buy_credits, name="buy_credits"),
    path("create-checkout-session/", create_checkout_session, name="create_checkout_session"),
    path("payment-success/", payment_success, name="payment_success"),
    path("stripe/webhook/", stripe_webhook, name="stripe_webhook"),
]
