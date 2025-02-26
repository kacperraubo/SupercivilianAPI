from .base import *  # noqa: F403
from .environment import environment
from .partial.google import *  # noqa: F403

SECRET_KEY = environment("SECRET_KEY")
ALLOWED_HOSTS = environment("ALLOWED_HOSTS").split(",")

# Caching settings

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "supercivilian",
    }
}

# Security settings

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 60
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True  # For http protocol it has to be set to False
CSRF_COOKIE_SECURE = True  # For http protocol it has to be set to False
CSRF_TRUSTED_ORIGINS = [f"https://{origin}" for origin in ALLOWED_HOSTS]
X_FRAME_OPTIONS = "DENY"
