import os
from pathlib import Path

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# CONFIGURATION DE SÉCURITÉ
# ==========================================
SECRET_KEY = 'django-insecure-votre_cle_secrete_ici_a_changer_en_production'

DEBUG = True

ALLOWED_HOSTS = ['*']


# ==========================================
# APPLICATIONS DU PROJET
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Ton application locale pour l'école
    'ecole', 
]

# ==========================================
# CONFIGURATION DE L'UTILISATEUR PERSONNALISÉ
# ==========================================
AUTH_USER_MODEL = 'ecole.Utilisateur'


# ==========================================
# MIDDLEWARES
# ==========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gestecole.urls'

# ==========================================
# TEMPLATES (LIEN AVEC TON DOSSIER TEMPLATES COMPRIS 🚀)
# ==========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # <-- ICI : Django sait maintenant où est ton dossier !
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ecole.context_processors.module_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'gestecole.wsgi.application'


# ==========================================
# BASE DE DONNÉES (DATABASE)
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================
# VALIDATION DES MOTS DE PASSE (CORRIGÉ)
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==========================================
# INTERNATIONALISATION (LANGUE & FUSEAU HORAIRE KINSHASA)
# ==========================================
LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Kinshasa'

USE_I18N = True

USE_TZ = True


# ==========================================
# GESTION DES FICHIERS STATIQUES (CSS, JS, IMAGES)
# ==========================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# CONFIGURATION PAR DÉFAUT POUR LES CLÉS PRIMAIRES
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================
# CONFIGURATION DES EMAILS POUR LE DÉVELOPPEMENT
# ==========================================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ==========================================
# REDIRECTIONS DE CONNEXION SÉCURISÉE 🔑
# ==========================================
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'