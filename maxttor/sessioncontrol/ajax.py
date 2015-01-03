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
from zope.app.component.hooks import getSite
from ZODB.POSException import ConflictError
from datetime import datetime, timedelta, date
from operator import itemgetter
from plone.memoize.instance import memoize

from maxttor.sessioncontrol import _
from maxttor.sessioncontrol.sessionControlTool import sessionTool

logger = logging.getLogger('maxttor.sessioncontorl')

class sessionscontrolUtils():
    """small utils"""

    def jsonResponse(self, context, data):
        """ Returns Json Data in Callback function
        """
        request = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)


class AjaxSessionsControlOnline(BrowserView):
    """ AJAX Trigger for sessions
    """

    def __call__(self):
        """Triggers sessionscontrol
        """
        try:
            toolcfg = sessionTool.getConfig()
            if toolcfg.enabled:            
                context = aq_inner(self.context)
                session = sessionTool.addUserSession(context=context, request=self.request)
                wu = sessionscontrolUtils() 
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
            wu = sessionscontrolUtils() 
            return wu.jsonResponse(context, {'result': 'ok'} )
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception, detail:
            # Avoid render errors to improve performance
            logger.error('%s (Ajax), Traceback: \n%s' %(detail, '\n'.join(traceback.format_exception(*sys.exc_info()))))
            return "error: %s"%detail
