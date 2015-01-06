# -*- coding: utf-8 -*-
from . import _

DEBUG           = True
TIME_STRING     = _(u"%d.%m.%Y at %H:%M:%S")

# min value for ajax time period 
MIN_session_ping_interval = 4000
# show inactive int he last 24 hours 
REMOVEINACTIVE_SECONDS = 86400
#TESTRR
REMOVEINACTIVE_SECONDS = 3600

# ---- this users will not be considered
USER_ID_BLACKLIST = ['admin']

# --- sessionscontrol -----------------------
WHO_IS_ONLINE_LISTING = '@@who-is-online'

# --- WhoAmI ----------------------------
WHO_IS_ONLINE_LISTING = '@@who-am-i'
#

# Database is a list in memmory.
DATA = []
COOKIE_NAME = 'maxttor_sc'
