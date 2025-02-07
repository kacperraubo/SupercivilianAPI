from .base import *  # noqa: F403
from .partial.database import *  # noqa: F403
from .partial.email import *  # noqa: F403
from .partial.google import *  # noqa: F403

SECRET_KEY = "development-key-dont-use-this-in-production"

# Caching settings

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Security settings

CSRF_COOKIE_SECURE = False
