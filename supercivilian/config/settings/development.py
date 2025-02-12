from .base import *  # noqa: F403
from .environment import environment
from .partial.google import *  # noqa: F403

SECRET_KEY = "development-key-dont-use-this-in-production"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"] + environment(
    "ALLOWED_HOSTS", default=""
).split(",")

# Caching settings

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Security settings

CSRF_COOKIE_SECURE = False
