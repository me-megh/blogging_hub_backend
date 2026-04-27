import os
from pathlib import Path

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',  # This must be included
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'corsheaders',

]
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Set MEDIA_URL to make it accessible via the browser

# for local 
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media' 
#DEBUG = True

# for production 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEBUG = False
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Optional: add a custom template directory
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
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for sessions
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for auth
    'django.contrib.messages.middleware.MessageMiddleware',  # Required for messages
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Make sure this is included
    'corsheaders.middleware.CorsMiddleware', 
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite database engine
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to the SQLite database file
    }
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',  # Optional, if you need basic auth
    ],
}
AUTHENTICATION_BACKENDS = [
    'blog.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    # Add any other authentication backends if needed
]
ROOT_URLCONF = 'backend.urls'
STATIC_URL = '/static/'
LOGOUT_REDIRECT_URL = '/' 
SECRET_KEY =os.environ.get('DJANGO_SECRET_KEY', 'jeg0^ihr-8+78=5zl_&1!((c0%s#w@8am==ms#hf-y(sxl)1ez'),
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000', 
    "https://blogging-hub-five.vercel.app" 
]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'https://blogging-hub-five.vercel.app/'
]
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False  # यह False रखना चाहिए जब आप डेवलपमेंट पर काम कर रहे हों
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_NAME = 'csrftoken' 
SESSION_COOKIE_SECURE = False ,
CSRF_COOKIE_SAMESITE = 'None',
ALLOWED_HOSTS = [
    'blogging-hub-backend.onrender.com',  # Your backend URL on Render
    'blogging-hub-five.vercel.app',       # Your frontend URL on Vercel
    '127.0.0.1',                         # Local development
    'localhost',                         
    '0.0.0.0',                           # Local development
]

