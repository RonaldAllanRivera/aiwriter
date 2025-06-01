# 📝 AIWriter – AI Content Generator for Small Businesses

AIWriter is a Django-based web app powered by OpenAI. It helps small businesses generate high-quality content like blog posts, product descriptions, and ads.

---

## 🚀 Features
- 🔧 Environment-driven authentication flow (email verification based on production mode)
- 🏷 Dynamic SaaS branding with SITE_NAME environment variable (supports CopySpark and future rebrands)
- 💳 Stripe payments with production-ready webhook support (PurchaseLog tracking)
- 🕵️ Intelligent trial system with incognito mode detection and abuse tracking
- 🔐 Email-only authentication with django-allauth
- 🔁 Social login via Google (fast login experience)
- 🧠 AI-powered content generation using GPT-3.5
- 🧾 Prompt templates (blog, FAQ, product intro, etc.)
- 📚 Personal generation history with pagination
- 🎨 Fully styled UI with Tailwind + Alpine.js
- 💡 Login-required views with helpful messages
- 🏠 Smart root URL: redirects or shows welcome page
- 🔐 Secure custom user model with no username field
- ✅ Ready for deployment on Render, Heroku, etc.

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

## 📁 Environment Variables (.env)

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ENVIRONMENT=development
SITE_URL=http://127.0.0.1:8000

OPENAI_API_KEY=your-openai-api-key

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=your-password

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
ALLOWED_HOSTS=127.0.0.1,localhost

STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key

```

---

## 📄 License

MIT – feel free to modify and use.
© 2025 Allan Rivera
