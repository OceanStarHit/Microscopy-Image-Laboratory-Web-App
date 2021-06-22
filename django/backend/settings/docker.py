from backend.settings.common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'Password1',
        'HOST': 'db',
        'PORT': 3306,
    }
}