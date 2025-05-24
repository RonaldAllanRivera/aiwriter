from django.shortcuts import render
from django.conf import settings
import openai
from openai import APIConnectionError, RateLimitError, AuthenticationError, OpenAIError
from .models import GenerationLog
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


# Initialize OpenAI client with your API key
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def home_view(request):
    if request.user.is_authenticated:
        return redirect('generate')  # or "/generate/"
    return render(request, "home.html")


def login_required_with_message(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access this page.")
            return redirect(f"/accounts/login/?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_with_message
def generate_view(request):
    output = ""
    prompt = ""
    selected_template = ""
    error = ""

    if request.method == "POST":
        prompt = request.POST.get("prompt")
        selected_template = request.POST.get("template")

        try:
            # Apply template logic
            if selected_template == "blog":
                final_prompt = f"Write a friendly blog post introduction about: {prompt}"
            elif selected_template == "product":
                final_prompt = f"Create an SEO product description for: {prompt}"
            elif selected_template == "caption":
                final_prompt = f"Write a catchy Instagram caption for: {prompt}"
            elif selected_template == "ad":
                final_prompt = f"Write a high-converting Google ad headline and description for: {prompt}"
            elif selected_template == "title":
                final_prompt = f"Write a compelling product title for: {prompt}"
            elif selected_template == "bullets":
                final_prompt = f"List 5 Amazon-style bullet features for: {prompt}"
            elif selected_template == "faq":
                final_prompt = f"Generate 3 frequently asked questions and answers about: {prompt}"
            elif selected_template == "outline":
                final_prompt = f"Give a blog post outline for a post about: {prompt}"
            elif selected_template == "newsletter":
                final_prompt = f"Write a friendly email newsletter about: {prompt}"
            elif selected_template == "testimonial":
                final_prompt = f"Write a customer testimonial for a product like: {prompt}"
            else:
                final_prompt = prompt  # fallback


            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": final_prompt}]
            )

            output = response.choices[0].message.content

            # Log it
            GenerationLog.objects.create(user=request.user, prompt=final_prompt, output=output)

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

