#generator/views.py
from django.shortcuts import render
from django.conf import settings
import openai
from openai import APIConnectionError, RateLimitError, AuthenticationError, OpenAIError
from .models import GenerationLog
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from users.models import UserProfile

import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import GenerationLog, TrialSessionLog



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

    # Clear guest credit display if authenticated
    if request.user.is_authenticated:
        request.session.pop("guest_credits", None)

    # Guest Trial Enforcement
    else:
        trial_log, created = TrialSessionLog.objects.get_or_create(ip_address=ip_address)

        # Initialize session trial counter
        if "guest_credits" not in request.session:
            # First time — allow 3 credits unless already blocked
            if trial_log.trial_uses >= 3:
                request.session["guest_credits"] = 0
                trial_log.abuse_flag = True
                trial_log.save()
            else:
                request.session["guest_credits"] = 3

        if request.session["guest_credits"] <= 0:
            trial_log.abuse_flag = True
            trial_log.save()
            messages.warning(request, "🎉 You’ve used your 3 free credits! Create a free account to unlock 10 more credits and save your content history.")
            return render(request, "generator/generate.html", {
                "prompt": "",
                "output": "",
                "selected_template": "",
                "error": "",
                "guest_credits": 0,
                "trial_ended": True,
            })

    # POST handling (Generate Request)
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        selected_template = request.POST.get("template")

        # Credit Check
        if request.user.is_authenticated:
            profile = request.user.userprofile
            if profile.credits <= 0:
                messages.error(request, "❌ You’ve run out of credits. Please upgrade your plan.")
                return redirect("buy_credits")
            
            # Optional: If user previously had a trial session from same IP
            ip_address = get_client_ip(request)
            trial_session = TrialSessionLog.objects.filter(ip_address=ip_address).first()
        else:
            guest_credits = request.session.get("guest_credits", 3)
            if guest_credits <= 0:
                messages.warning(request, "🎉 Trial ended. Please create a free account to continue.")
                return render(request, "generator/generate.html", {
                    "prompt": prompt,
                    "output": "",
                    "selected_template": selected_template,
                    "error": "",
                    "guest_credits": 0,
                    "trial_ended": True,
                })

        try:
            # Template Conversion
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

            # OpenAI Generation
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": final_prompt}]
            )
            output = response.choices[0].message.content

            # Credit Deduction
            if request.user.is_authenticated:
                profile.credits -= 1
                profile.save()
                GenerationLog.objects.create(user=request.user, prompt=final_prompt, output=output)
            else:
                request.session["guest_credits"] -= 1
                trial_log.trial_uses += 1
                trial_log.user_agent = user_agent

                # Add this to log abuse
                if trial_log.trial_uses >= 3:
                    trial_log.abuse_score += 1

                trial_log.save()

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


# For Stripe Payment
def buy_credits(request):
    return render(request, "generator/buy_credits.html", {
    "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY
})



@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        credit_amount = int(request.POST.get("credits"))
        price_in_cents = credit_amount * 100  # $1 = 1 credit

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f"{credit_amount} AIWriter Credits"},
                    'unit_amount': price_in_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payment/success/') + "?credits=" + str(credit_amount),
            cancel_url=request.build_absolute_uri('/buy-credits/'),
            metadata={'user_id': request.user.id}
        )
        return JsonResponse({'id': checkout_session.id})

def payment_success(request):
    credits = int(request.GET.get("credits", 0))
    profile = request.user.userprofile
    profile.credits += credits
    profile.save()
    messages.success(request, f"✅ {credits} credits added successfully!")
    return redirect("generate")
