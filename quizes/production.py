from .settings import *  # noqa
from .settings import env  # noqa


DATABASES = {"default": env.db()}
