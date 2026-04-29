from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

<<<<<<< HEAD

def load_env_file(env_path):
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_env_file(BASE_DIR / '.env')


def env_value(key, default=None):
    value = os.getenv(key)
    if value is None:
        return default
    value = value.strip()
    return value if value else default

=======
>>>>>>> f81f612207979a3dec3531f73deb3ea7a70a8c73
SECRET_KEY = 'django-insecure-votre-cle-ici'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
<<<<<<< HEAD
    'accounts',
=======
>>>>>>> f81f612207979a3dec3531f73deb3ea7a70a8c73
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'DB_ECOMMERCE'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}


LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')

<<<<<<< HEAD
LOGIN_REDIRECT_URL = 'product_list'
LOGOUT_REDIRECT_URL = 'product_list'
LOGIN_URL = 'login'

if env_value('EMAIL_HOST_USER') and env_value('EMAIL_HOST_PASSWORD'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env_value('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(env_value('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = env_value('EMAIL_USE_TLS', 'true').lower() == 'true'
    EMAIL_HOST_USER = env_value('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env_value('EMAIL_HOST_PASSWORD')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = env_value('DEFAULT_FROM_EMAIL', 'no-reply@emi-shop.local')

=======
>>>>>>> f81f612207979a3dec3531f73deb3ea7a70a8c73
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
