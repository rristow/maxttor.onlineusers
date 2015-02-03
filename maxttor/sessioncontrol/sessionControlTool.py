# -*- coding: utf-8 -*-
import uuid
from Products.CMFCore.utils import getToolByName 
from zope.component import getUtility
from Acquisition import aq_inner
from datetime import datetime, timedelta, date
from plone.registry.interfaces import IRegistry
from maxttor.sessioncontrol.interfaces import ISessionsControlSettings
from maxttor.sessioncontrol.dbapi import db
from maxttor.sessioncontrol.utils import getCookie, setCookie
from maxttor.sessioncontrol.config import DEBUG, REMOVEINACTIVE_SECONDS
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite
import logging

logger = logging.getLogger('maxttor.sessioncontorl')

#TODO
maxSessions = 3
    
class sessionControlTool(object):
    """ Online Users Tool """

    def getConfig(self):
        """
        Returns True if te tool is site-wide enabled.
        """
        ru =  getUtility(IRegistry)
        return ru.forInterface(ISessionsControlSettings)

    def isActive(self, context):
        """ is the session control active """
        mt = getToolByName(context,"portal_membership")
        ret = self.getConfig().enabled and not mt.isAnonymousUser()
        return ret            

    def addUserSession(self, context, request):
        """ Add or update the existing user and session in the sessioncontrol"""
    
        context = aq_inner(context)
        mt = getToolByName(context,"portal_membership")
        member = mt.getAuthenticatedMember()

        if member.getId():
            sdm = context.session_data_manager
            # DB conflicts using sessions
            #session = sdm.getSessionData(create=True)
            #session_id = sdm.getBrowserIdManager().getBrowserId(create=False)

            session_id = getCookie(request)
            if not session_id:
                # Generate a uuid to represent the session
                session_id = uuid.uuid4().hex
                setCookie(request, session_id)

            session_ip = request.get('HTTP_X_FORWARDED_FOR') or request.get('REMOTE_ADDR',None)
            session = db.AddUserSession(member, maxSessions, session_id, session_ip)
            
            return session


    def deleteUserSession(self, context=None, user_id=''):
        """ Remove the user from the sessioncontrol"""
        
        if not user_id:
            if context:
                context = aq_inner(context)
                mt = getToolByName(context,"portal_membership")
                member = mt.getAuthenticatedMember()
                user_id = member.getId();

        if user_id:
            return db.deleteUserSession(user_id)

    def deleteSession(self, session_id):
        """ Remove the session from sessioncontrol"""
        return db.deleteSession(session_id)

    def deleteInactiveSessions(self, inactiveTimeout=REMOVEINACTIVE_SECONDS):
        """ Remove inactive sessions """
        return db.deleteInactiveSessions(inactiveTimeout)

    def deepclean(self):
        """ Remove alte sessions """
        return db.deepclean()

    def get_sessiondata(self):
        return db.DATA

    def get_sessions_active(self, user_id):
        """ Return all active sessions for this user """
        user = db.getSessionUser(user_id)
        if user:
            return [s for s in user.sessions if s.isActive()]
        else:
            return []
sessionTool = sessionControlTool()

def clear_session_on_logout(event):
    """
    Logout event handler.
    """
    session_id = "UNDEFINED"
    try:
        request = event.object.REQUEST    
        session_id = getCookie(request)
        sessionTool.deleteSession(session_id)
        setCookie(request, "")
        if DEBUG:
            logger.warning("Session '%s' deleted on logout"%session_id)
    except:
        logger.error("It was not possible to clear the session '%s' on logout"%session_id)
