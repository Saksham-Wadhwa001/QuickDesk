
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.auth',
    'users',
    'tickets',
    'corsheaders'
]

CORS_ALLOWED_ORIGINS = ['http://localhost:3000']