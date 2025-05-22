from django.shortcuts import render
from django.conf import settings
import openai
from .models import GenerationLog


# Initialize OpenAI client with your API key
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_view(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content

        # Save to database
        GenerationLog.objects.create(prompt=prompt, output=output)

        return render(request, "generator/generate.html", {
            "prompt": prompt,
            "output": output
        })

    return render(request, "generator/generate.html")