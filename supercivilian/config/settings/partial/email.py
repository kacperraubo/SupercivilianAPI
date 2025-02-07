from ..environment import environment

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = environment("EMAIL_HOST")
EMAIL_PORT = environment("EMAIL_PORT")
EMAIL_HOST_USER = environment("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = environment("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = environment("EMAIL_USE_TLS") == "True"
EMAIL_USE_SSL = environment("EMAIL_USE_SSL") == "True"
