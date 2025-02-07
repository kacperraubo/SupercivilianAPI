from ..environment import environment

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environment("DB_NAME"),
        "USER": environment("DB_USER"),
        "PASSWORD": environment("DB_PASSWORD"),
        "HOST": environment("DB_HOST"),
        "PORT": environment("DB_PORT"),
    }
}
