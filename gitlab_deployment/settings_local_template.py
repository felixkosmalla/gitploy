from settings import SITE_ROOT
import os

DEBUG = False

TEMPLATE_DEBUG = DEBUG



STATIC_ROOT = "/home/gitploy/document_root/static/"

REPOSITORY_ROOT = "/home/gitploy/repositories/"				# WITH TRAILING SLASH!

GITLAB_URL = "http://git.your-company.org"

DEPLOY_KEY = "ssh-rsa ......"


ALLOWED_HOSTS = [
	".your-company.org"
]

