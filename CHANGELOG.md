# 📜 CHANGELOG – AIWriter

## [1.3.0] — 2025-06-02

### Added

- Full SaaS Deployment Refactor for Render cloud platform
- Automated deployment via `render.yaml` and `build.sh`
- Fully cleaned settings.py with ENVIRONMENT switching and database flexibility
- Static file serving via WhiteNoise in production
- requirements.txt updated with production-safe dependencies
- Deployment-ready for PostgreSQL in production, SQLite in development
- Improved .env structure for local/prod separation


## [1.2.0] — 2025-06-01

### Added

- Abuse Alert system fully integrated
- Admin email notification when abuse threshold is reached
- ENVIRONMENT-safe: abuse emails only sent in production mode
- Abuse scoring dynamically monitored inside guest trial logic
- Dynamic SITE_NAME used in alert email subject

---

## [1.1.0] — 2025-06-01

### Added

- Fully stable SaaS Stripe Payment System
- Webhook verification added for Stripe `checkout.session.completed`
- PurchaseLog model to track user Stripe purchases
- Stripe metadata protection for credits, user ID, and pack purchased
- Dynamic SITE_URL for multi-environment flexibility
- SEO-optimized homepage with conversion-first CTA
- SaaS-ready URL structure finalized

### Fixed

- Circular import issues with generator.urls removed
- AllAuth URLs restored to prevent account_login errors
- payment-success rendering path fixed for templates

---

## [1.0.0] — 2025-06-01

### Added

- Django-Allauth email login system (username fully removed)
- Google OAuth login support
- Guest trial system with IP tracking
- Incognito detection via session analysis
- Stripe full SaaS integration: buy credits, webhook, user credit update
- ENVIRONMENT-driven payment and webhook toggles for dev/prod separation
- Full SaaS production-ready credit logic
- Secure OpenAI integration with GPT-3.5 Turbo API

## [0.6.0] - 2025-06-01

### Added
- Fully cleaned views.py with final SaaS structure (home, generate, Stripe payments, webhook)
- Stripe Webhook integration (checkout.session.completed synced to backend)
- Metadata protection inside Stripe Checkout Sessions (user ID, credits, pack)
- Final payment flow with safe double-credit prevention
- ENVIRONMENT switch (production vs development) controlling webhook validation
- SEO-optimized homepage template added (home.html with Tailwind design)
- Trial system refactor to better isolate guest users
- Full URL structure polished with clean generator.urls removal
- Dynamic SITE_URL used for all Stripe callback URLs

### Fixed
- Corrected circular imports when including generator.urls
- Correct account_login NoReverseMatch errors by restoring allauth.urls include
- Resolved payment-success rendering issues due to template search path
- Cleaned Stripe metadata handling after payment completion



## [0.5.2] - 2025-06-01

### Added
- Dynamic SITE_URL environment variable for flexible Stripe URL handling (local & prod safe)
- Stripe success/cancel URL logic fully moved to environment-driven config
- Securely retrieve Stripe session_id from success URL for credit allocation
- PurchaseLog now fully records credits and amounts accurately post-purchase
- SaaS payment flow now fully production-ready after Stripe metadata cleanup

### Fixed
- Corrected success URL string formatting for Stripe session redirection
- Fixed multiple edge cases with credits not properly being applied after checkout


## [0.5.1] - 2025-05-31
### Changed
- Switched ACCOUNT_EMAIL_VERIFICATION logic to use ENVIRONMENT instead of DEBUG
- Added SITE_NAME environment variable for dynamic SaaS branding
- Templates and checkout sessions now fully use SITE_NAME dynamically
- Cleaner SaaS-ready environment separation for authentication flows

## [0.5.0] - 2025-05-30
### Added
- PurchaseLog model to track user Stripe purchases
- PurchaseLog admin panel support for easy monitoring
- Stripe webhook integration with ENVIRONMENT toggle
- Webhooks safely disabled in development environment
- Automatic status update of purchases via checkout.session.completed

## [0.4.0] - 2025-05-29
### Added
- Intelligent guest trial tracking with abuse score and incognito detection
- Admin panel enhancements: incognito flag, linked user, registered status
- Patched generate view to record trials early and robustly
- Added fallback incognito detection logic with session cookie checks

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
