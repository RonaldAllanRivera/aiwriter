# 📜 CHANGELOG – AIWriter

## [0.3.0] - 2025-05-22
### Added
- Switched to email-only login by removing username field
- Created and integrated custom user model (CustomUser)
- Reset database and reinitialized migrations
- Protected /generate and /history views with login_required
- Added login-required redirect messages via Django messages framework
- Unified login and signup form styles with Tailwind
- Overrode allauth templates: login.html, signup.html, provider_login.html, authentication_error.html
- Implemented smart root URL logic: redirect if logged in, show welcome if not
- Styled Google login flows and confirmation states
- Logout UI now displays user email instead of username

## [0.2.0] - 2025-05-21
### Added
- Integrated django-allauth with Google login support
- Added social account templates and Tailwind styling
- Navigation auto-hides links for unauthenticated users

## [0.1.0] - 2025-05-20
### Added
- Initial Django setup with OpenAI GPT integration
- Tailwind UI, prompt templates, generation history and pagination
