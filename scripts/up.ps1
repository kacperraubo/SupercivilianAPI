$env:DEBUG="True"
$env:DJANGO_SETTINGS_MODULE="supercivilian.config.settings.development"
python manage.py runserver 0.0.0.0:12345
