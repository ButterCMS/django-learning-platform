from butter_cms import ButterCMS
from django.conf import settings

from .exceptions import MissingButterCMSToken

if settings.BUTTER_CMS_TOKEN is None:
    raise MissingButterCMSToken("BUTTER_CMS_TOKEN must be set")

client = ButterCMS(settings.BUTTER_CMS_TOKEN)
