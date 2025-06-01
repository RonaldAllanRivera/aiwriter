# 📝 AIWriter – AI Content SaaS

AIWriter is a fully SaaS-ready Django web app powered by OpenAI and Stripe. It allows small business owners to generate high-quality content like blog posts, FAQs, product descriptions, and ads using AI.


## 🚀 Features
- ⚙ Dynamic environment config (ENVIRONMENT switch: development / production)
- 🏷 Dynamic SaaS branding with SITE_NAME variable
- 💳 SaaS-ready payment system via Stripe Checkout + Webhooks
- 📦 Credit Packs: flexible pricing via constants.py
- 🎯 SEO-optimized homepage with CTA funnel
- 🔒 Trial system with abuse detection + incognito tracking
- 📬 Admin email notifications for abuse alerts
- 🔑 Email-only login via django-allauth (username fully removed)
- 🔐 Google OAuth fast login integration
- 🧠 OpenAI GPT-3.5 Turbo AI content generation
- 🗂 Template system: blogs, ads, FAQs and more
- 📚 Personal generation history with pagination
- 🎨 Fully styled UI with Tailwind CSS + Alpine.js
- ✅ Deployment-ready on Render, Railway, Fly.io


---

## 🛠 Tech Stack

- **Backend**: Django 5, Python 3.13
- **Frontend**: Tailwind CSS (CDN) + Alpine.js
- **AI API**: OpenAI GPT-3.5 (via ChatCompletion)
- **Auth**: django-allauth (email + Google login)

---

## 🔧 Local Setup

```bash
git clone https://github.com/your-username/aiwriter.git
cd aiwriter
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API key and SMTP config
python manage.py migrate
python manage.py runserver
```

---

## 📁 Environment Variables (.env)
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ENVIRONMENT=development
SITE_URL=http://127.0.0.1:8000
SITE_NAME=CopySpark

OPENAI_API_KEY=your-openai-key

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-password

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
ALLOWED_HOSTS=127.0.0.1,localhost

STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

DEFAULT_FROM_EMAIL=noreply@copyspark.com
DEFAULT_ADMIN_EMAIL=your-admin@email.com


```

---

## 📄 License

MIT – feel free to modify and use.
© 2025 Allan Rivera
