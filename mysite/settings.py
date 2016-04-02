# -*- coding: utf-8 -*-

import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + [
    'django.core.context_processors.request',
    ]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bo8uxkig3$q5v!9t^#6-xe72wt1na9xtsz+!3w#9s%^83_i8)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]

SUIT_CONFIG = {
    'ADMIN_NAME': '运维管理系统',
    'SHOW_REQUIRED_ASTERISK': True,
    'SEARCH_URL': '/admin/managEng/hosts',


    'MENU': (
        '-',
#--------
        {'label': u'主机管理','icon':'icon-cog', 'models': 
        (
            {'label': u'主机', 'url': '/admin/managEng/devices'},
            {'label': u'虚拟机', 'url': '/admin/managEng/hosts'},
        ) 
        },
 #-------------       
        {'label': u'IP资源', 'icon':'icon-globe', 'models': 
        (
            {'label': u'IP段', 'url': '/admin/managEng/ipsub'},
            {'label': u'IP列表', 'url': '/admin/managEng/ip',},
        )
        },

 #-------------       
        {'label': u'网安数据中心',  'models': 
        (
            {'label': u'办公区入网信息', 'url': '/admin/managEng/allownet'},
            {'label': u'无线上网设备', 'url': '/admin/managEng/wireless',},
            {'label': u'打印机', 'url': '/admin/managEng/print',},
            {'label': u'部门管理', 'url': '/admin/managEng/dept',},
        )
        },

 #-------------       
        {'label': u'项目', 'icon':'icon-file',  'url': '/admin/managEng/projects'},
#-------
        '-',
        {'label': u'DNS解析','icon':'icon-cog', 'models': 
        (
            {'label': u'域', 'url': '/admin/mybind/zones'},
            # {'label': u'解析', 'url': '/admin/mybind/records'},
        ) 
        },
#------
        '-',
         {'app': 'auth', 'icon':'icon-user', 'models': ('user', 'group')},
        
        ),
}
# # Application definition




INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'managEng',
    'mybind',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), 
        ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'PORT': '',
        'NAME': 'managEng',
        'USER': 'root',
        'PASSWORD' : '123456',
    }
}

##邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.126.com'
EMAIL_PORT = 25
# EMAIL_HOST_USER = 'wuchencm@126.com'
# EMAIL_HOST_PASSWORD = 'wudalong2016,./'
# DEFAULT_FROM_EMAIL = 'wudalong <wuchencm@126.com>'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE =  'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console':{
#             'level':'DEBUG',
#             'class':'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#     }
# }
