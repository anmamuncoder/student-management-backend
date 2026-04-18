from datetime import timedelta
from pathlib import Path
import environ
import os

# -------------------------------
# Base Directory
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------
# Initialize environment variables
# -------------------------------
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# -------------------------------
# Security Settings
# -------------------------------
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)


# Allow all hosts during development
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])
CSRF_TRUSTED_ORIGINS = [
    # Add your frontend URLs here
    "http://localhost:5173",    # For development with Vite React
    "http://127.0.0.1:5173",    # For development with Vite React
    
    # Add production frontend & backend URL when deploying
     
]
CORS_ALLOW_ALL_ORIGINS = True # Allow all origins for development; change to False in production
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])


# Email Settings
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = env('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = "no-reply@example.com"

# -------------------------------
# Installed Apps
# -------------------------------
DJANGO_APPS = [
    # 'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework.authtoken",
    "django_filters",
    
    "drf_spectacular",
     
    # "channels"      # For real-time features (WebSockets)

]

CUSTOM_APPS = [
    'apps.accounts',
    'apps.rbac',
    'apps.student',
    'apps.course',
    'apps.exam',
    'apps.time_table',


]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS


# -------------------------------
# Middleware
# -------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at the top
    'django.middleware.common.CommonMiddleware',

    # Static files (CSS,JS,images) when using Daphne or any ASGI server, because they don’t serve static files by default. 
    # After adding this middleware, remember to run: `python manage.py collectstatic 
    'whitenoise.middleware.WhiteNoiseMiddleware',

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Custom middleware to capture current user for audit fields in models
    'kernel.middleware.current_user.CurrentUserMiddleware',
    # Middleware to enforce role-based permissions and access control (RBAC)
    'kernel.middleware.permissions_middleware.RBACMiddleware',

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

# -------------------------------
# URLs & WSGI/ASGI
# -------------------------------
AUTH_USER_MODEL = "accounts.User" # Custom user model
ROOT_URLCONF = 'engine.urls'
WSGI_APPLICATION = 'engine.wsgi.application' 
# ASGI_APPLICATION = 'engine.asgi.application'    # For real-time features (WebSockets)


# -------------------------------
# Registration
# -------------------------------
AUTO_LOGIN_AFTER_REGISTRATION = True # If True, user is automatically logged in after registration; otherwise, login is required manually

# -------------------------------
# OTP Base Login 
# -------------------------------
# If True, send OTP on every login; if False, send OTP only once after registration for initial email verification.
AUTH_OTP_ENABLED = False

OTP_EXPIRY_TIME = 300  # OTP expiry time in minutes
OTP_RESEND_COOLDOWN = 60 # if otp created then again after 1 minute will be generate otp

# -------------------------------
# Forget Password Process
# -------------------------------
RESET_OTP_EXPIRY = 300
RESET_TOKEN_EXPIRY = 600
OTP_RESEND_COOLDOWN = 60  


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add your templates directory here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# -------------------------------
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# -------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': env('POSTGRES_ENGINE'),
#         'NAME': env('POSTGRES_NAME'),
#         'USER': env('POSTGRES_USER'),
#         'PASSWORD': env('POSTGRES_PASSWORD'),
#         'HOST': env('POSTGRES_HOST', default='db'),  # db service in docker-compose
#         'PORT': env('POSTGRES_PORT', default='5432'),
#     }
# }


# -------------------------------
# Password Validators
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# -------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -------------------------------
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# -------------------------------

LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')
TIME_ZONE = env('TIME_ZONE', default='Asia/Dhaka')
USE_I18N = True
USE_TZ = True


# -------------------------------
# Static & Media (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
# -------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -------------------------------
# Django REST Framework 
# ------------------------------- 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'apps.accounts.authentication.PasswordAwareJWTAuthentication', # custome extended
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Custom exception handler to standardize error responses
    "EXCEPTION_HANDLER": "kernel.exceptions.custom_exception_handler",

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/day',
        'user': '500/day',
        # 'forgot_password': '1/minute', 
    },
    
    # OpenAPI Schema Generation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Versioning ; "api/<str:version>/endpoint/" in urls, request.version == "v1" in views
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
}
 

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    
    'AUTH_HEADER_TYPES': ("Bearer",), 
    'USER_ID_FIELD': "id",
    'USER_ID_CLAIM': "id",
    'ROTATE_REFRESH_TOKENS': True, # Issue a new refresh token every time the old one is used
    'BLACKLIST_AFTER_ROTATION': True, # Old refresh token is blacklisted immediately after rotation
}



# -------------------------------
# Celery Configuration
# Run windows Terminal: celery -A core worker --loglevel=INFO -P solo
# -------------------------------
# CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://redis:6379/0')
# CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://redis:6379/1')
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes per task


# -------------------------------
# Cache (Redis)
# -------------------------------

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique",
    }
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": env('REDIS_URL', default='redis://redis:6379/2'),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }


# -------------------------------
# Security Headers
# -------------------------------
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_REFERRER_POLICY = "same-origin"


# -------------------------------
# Logging
# -------------------------------
os.makedirs(BASE_DIR / "logs", exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {message}', 'style': '{'},
        'simple': {'format': '{levelname} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': True},
        # 'rbac': {
        #     'handlers': ['console'],
        #     'level': 'WARNING',
        # },
    },
}


# -------------------------------
# Jazzmin Admin
# -------------------------------
# JAZZMIN_SETTINGS = {
#     "site_title": "Base Project Admin",
#     "site_header": "Base Project",
#     "site_brand": "BaseProject",
#     "welcome_sign": "Welcome to Base Project Admin",
#     "copyright": "Base Project © 2026",
#     "show_ui_builder": True,
# }


