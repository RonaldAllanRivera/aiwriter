# generator/views.py
from django.shortcuts import render, redirect
from django.conf import settings
import openai
from openai import APIConnectionError, RateLimitError, AuthenticationError, OpenAIError
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from users.models import UserProfile, CustomUser

import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from .models import GenerationLog, TrialSessionLog, PurchaseLog
from .constants import STRIPE_CREDIT_PACKS



# Webhook handling for Stripe (disabled in development)
import json


stripe.api_key = settings.STRIPE_SECRET_KEY

# Initialize OpenAI client with your API key
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def home_view(request):
    if request.user.is_authenticated:
        # Reset guest session data
        request.session.pop("guest_credits", None)
        return redirect('generate')
    return render(request, "home.html")


def login_required_with_message(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access this page.")
            return redirect(f"/accounts/login/?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper

# Helper to get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def generate_view(request):
    output = ""
    prompt = ""
    selected_template = ""
    error = ""

    ip_address = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    is_guest = not request.user.is_authenticated

    # Reset guest session data if authenticated
    if request.user.is_authenticated:
        request.session.pop("guest_credits", None)
        trial_session = TrialSessionLog.objects.filter(ip_address=ip_address).first()
        if trial_session:
            trial_session.linked_user = request.user
            trial_session.registered = True
            trial_session.save()
    else:
        # Get or create trial session
        trial_session, _ = TrialSessionLog.objects.get_or_create(ip_address=ip_address)

        # Only flag incognito if trial_uses already exists        
        if trial_session.trial_uses > 0 and not trial_session.is_incognito:
            trial_session.is_incognito = True
            trial_session.abuse_score += 1
            trial_session.save()
            print("🚩 Incognito likely detected after previous usage.")  


        # First-time session setup
        if "guest_credits" not in request.session:
            if trial_session.trial_uses >= 3:
                request.session["guest_credits"] = 0
            else:
                request.session["guest_credits"] = 3

        if request.session["guest_credits"] <= 0:
            trial_session.abuse_flag = True
            trial_session.abuse_score += 1
            trial_session.save()
            messages.warning(request, "🎉 You’ve used your 3 free credits! Create a free account to unlock 10 more credits and save your content history.")
            return render(request, "generator/generate.html", {
                "prompt": "",
                "output": "",
                "selected_template": "",
                "error": "",
                "guest_credits": 0,
                "trial_ended": True,
            })

    # POST (Generate request)
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        selected_template = request.POST.get("template")

        if request.user.is_authenticated:
            profile = request.user.userprofile
            if profile.credits <= 0:
                messages.error(request, "❌ You’ve run out of credits. Please upgrade your plan.")
                return redirect("buy_credits")
        else:
            guest_credits = request.session.get("guest_credits", 0)
            if guest_credits <= 0:
                trial_session.abuse_score += 1
                trial_session.abuse_flag = True
                trial_session.save()
                messages.warning(request, "🎉 You’ve used your 3 free credits! Create a free account to unlock 10 more credits and save your content history.")
                return render(request, "generator/generate.html", {
                    "prompt": prompt,
                    "output": "",
                    "selected_template": selected_template,
                    "error": "",
                    "guest_credits": 0,
                    "trial_ended": True,
                })

        # Compose prompt based on template
        prompt_map = {
            "blog": f"Write a friendly blog post introduction about: {prompt}",
            "product": f"Create an SEO product description for: {prompt}",
            "caption": f"Write a catchy Instagram caption for: {prompt}",
            "ad": f"Write a high-converting Google ad headline and description for: {prompt}",
            "title": f"Write a compelling product title for: {prompt}",
            "bullets": f"List 5 Amazon-style bullet features for: {prompt}",
            "faq": f"Generate 3 frequently asked questions and answers about: {prompt}",
            "outline": f"Give a blog post outline for a post about: {prompt}",
            "newsletter": f"Write a friendly email newsletter about: {prompt}",
            "testimonial": f"Write a customer testimonial for a product like: {prompt}",
        }
        final_prompt = prompt_map.get(selected_template, prompt)

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": final_prompt}]
            )
            output = response.choices[0].message.content

            # Deduct credit and save
            if request.user.is_authenticated:
                profile.credits -= 1
                profile.save()
                GenerationLog.objects.create(user=request.user, prompt=final_prompt, output=output)
            else:
                request.session["guest_credits"] -= 1
                trial_session.trial_uses += 1
                trial_session.user_agent = user_agent
                # trial_session.is_incognito preserved from earlier detection
                if trial_session.trial_uses >= 3:
                    trial_session.abuse_score += 1
                trial_session.save()

                if request.session["guest_credits"] <= 0:
                    messages.warning(request, "🎉 You’ve used your 3 free credits! Create a free account to unlock 10 more credits and save your content history.")

        except APIConnectionError:
            error = "⚠️ Oops! You're offline or OpenAI servers are unreachable."
        except RateLimitError:
            error = "⚠️ Too many requests. Please wait a moment and try again."
        except AuthenticationError:
            error = "⚠️ Invalid API key. Please check your credentials."
        except OpenAIError:
            error = "⚠️ OpenAI returned an unexpected error. Please try again."
        except Exception:
            error = "⚠️ An unknown error occurred. Please try again later."

    return render(request, "generator/generate.html", {
        "prompt": prompt,
        "output": output,
        "selected_template": selected_template,
        "error": error,
        "guest_credits": request.session.get("guest_credits") if is_guest else None,
        "trial_ended": request.session.get("guest_credits") == 0 if is_guest else False
    })



@login_required_with_message
def history_view(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    logs = GenerationLog.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(logs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "generator/history.html", {"page_obj": page_obj})


def buy_credits(request):
    return render(request, "generator/buy_credits.html", {
        "credit_packs": STRIPE_CREDIT_PACKS
    })


@csrf_exempt
def create_checkout_session(request):
    if request.method != "POST":
        return redirect("buy_credits")

    pack = request.POST.get("pack")
    pack_data = STRIPE_CREDIT_PACKS.get(pack)

    if not pack_data:
        return redirect("buy_credits")

    # ✅ Here is your fully dynamic URL based on settings.SITE_URL
    success_url = f"{settings.SITE_URL}/payment-success/?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{settings.SITE_URL}/buy-credits/"

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": int(pack_data["price"] * 100),
                "product_data": {"name": f"CopySpark {pack.capitalize()} Plan"},
            },
            "quantity": 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "credits": pack_data["credits"],
            "pack": pack,
            "user_id": request.user.id
        },
        customer_email=request.user.email
    )

    PurchaseLog.objects.create(
        user=request.user,
        stripe_session_id=session.id,
        credits=pack_data['credits'],
        amount=pack_data['price'],
        status="pending"
    )

    return redirect(session.url)



def payment_success(request):
    session_id = request.GET.get("session_id")

    if not session_id:
        messages.error(request, "Missing session information.")
        return redirect("buy_credits")

    try:
        # Fetch the session data from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        credits = int(session.metadata.get("credits", 0))
    except Exception as e:
        messages.error(request, f"Failed to retrieve payment: {e}")
        return redirect("buy_credits")

    profile = request.user.userprofile
    profile.credits += credits
    profile.save()

    messages.success(request, f"✅ {credits} credits added successfully!")
    return render(request, 'generator/payment_success.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    if settings.ENVIRONMENT == "production":
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)
        except Exception:
            return HttpResponse(status=400)
    else:
        # In dev mode, skip verification (for testing only)
        try:
            event = json.loads(payload)
        except Exception:
            return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        metadata = session.get("metadata", {})

        try:
            user = CustomUser.objects.get(id=metadata.get("user_id"))
            credits = int(metadata.get("credits", 0))

            # Avoid double credit if already processed
            log, created = PurchaseLog.objects.get_or_create(
                user=user,
                stripe_session_id=session_id,
                defaults={
                    "credits": credits,
                    "amount": session["amount_total"] / 100,
                    "status": "completed"
                }
            )

            if not created and log.status != "completed":
                user.userprofile.credits += credits
                user.userprofile.save()
                log.status = "completed"
                log.save()

        except Exception as e:
            print("Webhook processing error:", str(e))
            return HttpResponse(status=500)

    return HttpResponse(status=200)


