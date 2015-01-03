# -*- coding: utf-8 -*-
from . import _

DEBUG           = True
TIME_STRING     = _(u"%d.%m.%Y at %H:%M:%S")

# min value for ajax time period 
MIN_session_ping_interval = 4000

# ---- this users will not be considered
USER_ID_BLACKLIST = ['admin']

# --- sessionscontrol -----------------------
WHO_IS_ONLINE_LISTING = '@@who-is-online'

# --- WhoAmI ----------------------------
WHO_IS_ONLINE_LISTING = '@@who-am-i'
#

# Database is a list in memmory.
DATA = []
