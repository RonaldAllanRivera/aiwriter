# 📜 CHANGELOG – AIWriter


## [0.6.0] - 2025-06-02

### Major Release — Full SaaS Payment Live System

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
