    import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY','dev-secret')
DEBUG=os.environ.get('DEBUG','False')=='True'
ALLOWED_HOSTS=['*']
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','rest_framework','apps.gitserver']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='backend.urls'
WSGI_APPLICATION='backend.wsgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.environ.get('DB_NAME','postgres'),'USER':os.environ.get('DB_USER','postgres'),'PASSWORD':os.environ.get('DB_PASS',''),'HOST':os.environ.get('DB_HOST','localhost'),'PORT':os.environ.get('DB_PORT','5432')}}
STATIC_URL='/static/'
STATIC_ROOT=str(BASE_DIR / 'staticfiles')
FRONTEND_BUILD_DIR=str(BASE_DIR / 'frontend_build')
import os
os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(FRONTEND_BUILD_DIR, exist_ok=True)
STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'
GIT_REPOS_ROOT=os.environ.get('GIT_REPOS_ROOT', os.path.join(BASE_DIR,'repos'))
os.makedirs(GIT_REPOS_ROOT, exist_ok=True)
