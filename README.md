# 📝 AIWriter – AI Content Generator for Small Businesses

AIWriter is a Django-based web app that uses OpenAI's ChatGPT API to help small business owners generate high-quality content like product descriptions, blog posts, and ad copy.

## 🚀 Features

- Simple and clean Tailwind-powered UI (via CDN)
- OpenAI GPT-3.5 content generation
- Prompt input + result rendering
- Database logging of generated content
- Django admin panel for viewing generation logs

## 📦 Tech Stack

- Backend: Django 5.x, Python 3.x
- Frontend: Tailwind CSS via CDN
- AI API: OpenAI GPT-3.5 (ChatCompletion endpoint)
- Database: SQLite (for dev), PostgreSQL recommended for production
- Deployment target: Render.com

## 🔧 Local Setup

```bash
git clone https://github.com/your-username/aiwriter.git
cd aiwriter
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then add your OpenAI API key
python manage.py migrate
python manage.py runserver
```

## 🧪 Demo Usage

1. Go to `/generate/`
2. Enter a prompt (e.g., "Write a product description for a handmade candle")
3. Submit and wait for the output
4. Log into `/admin/` to view generation history

## 📄 License

MIT – feel free to build on this.

---
© 2025 Allan Rivera
