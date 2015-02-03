# -*- coding: utf-8 -*-
import sys
import traceback
import json
import logging

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName 
from zope.component import getUtility
from Acquisition import aq_inner
from ZODB.POSException import ConflictError
from datetime import datetime, timedelta, date
from operator import itemgetter
from plone.memoize.instance import memoize
from maxttor.onlineusers import _
from maxttor.onlineusers.sessionControlTool import sessionTool
from maxttor.onlineusers.utils import JsonDump
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

logger = logging.getLogger('maxttor.sessioncontorl')

class AjaxSessionsControlOnline(BrowserView):
    """ AJAX Trigger for sessions
    """

    def __call__(self):
        """Triggers sessionscontrol
        """
        try:
            toolcfg = sessionTool.getConfig()
            wu = JsonDump() 
            if toolcfg.enabled:            
                context = aq_inner(self.context)
                session = sessionTool.addUserSession(context=context, request=self.request)
                if session:
                    #logger.warning("AjaxSessionsControlOnline finished (session: %s)"%session.session_id)
                    return wu.jsonResponse(context, {'result': 'ok', 'session_id' : session.session_id, 'enabled': toolcfg.enabled, 'session_ping_interval': toolcfg.session_ping_interval, } )
                else:
                    #logger.warning("AjaxSessionsControlOnline finished with errors ")
                    return wu.jsonResponse(context, {'result': 'error', 'session_id' : 'None', 'enabled': False, 'session_ping_interval': 60, })
            else:
                return wu.jsonResponse(context, {'result': 'error', 'session_id' : 'None', 'enabled': False, 'session_ping_interval': 60, })                
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception, detail:
            # Avoid render errors to improve performance
            logger.error('%s (Ajax), Traceback: \n%s' %(detail, '\n'.join(traceback.format_exception(*sys.exc_info()))))
            return "error: %s"%detail

class AjaxSessionsControlOffline(BrowserView):
    """AJAX Trgger for sessionscontrol - offline
    """

    def __call__(self):
        """Triggers sessionscontrol
        """
        logger.warning("AjaxSessionsControlOffline")
        try:
            context = aq_inner(self.context)
            sessionTool.deleteUserSession(context=context)
            wu = JsonDump() 
            return wu.jsonResponse(context, {'result': 'ok'} )
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception, detail:
            # Avoid render errors to improve performance
            logger.error('%s (Ajax), Traceback: \n%s' %(detail, '\n'.join(traceback.format_exception(*sys.exc_info()))))
            return "error: %s"%detail
