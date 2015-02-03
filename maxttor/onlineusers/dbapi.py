# -*- coding: utf-8 -*-
import logging
import hashlib
import os
import time

from zope.component import getUtility
from datetime import datetime, timedelta
from maxttor.onlineusers.config import DEBUG, USER_ID_BLACKLIST, REMOVEINACTIVE_SECONDS
from plone.registry.interfaces import IRegistry
from maxttor.onlineusers.interfaces import ISessionsControlSettings
logger = logging.getLogger('maxttor.sessioncontorl')

class UserSession(object):
    session_id      = u""
    timestamp_login = 0
    timestamp       = 0
    ip              = u""

    def formattime(self, pdate):
        diff_sec = abs(time.mktime(datetime.now().timetuple()) - time.mktime(pdate.timetuple()))
        if diff_sec < 60:
            return "%s sec."%diff_sec
        else:
            return "%2.2f min."%(diff_sec/60)

    def time_online(self):
        return self.formattime(self.timestamp_login)

    def time_lastrefresh(self):
        return self.formattime(self.timestamp)

    def checkTimeout(self, ptimeout):
        """ Check if a session is older than ptimeout (seconds) """
        now = datetime.now()
        timeout =  now  - timedelta(seconds=ptimeout)
        return self.timestamp < timeout

    def isActive(self):
        """ Check if a session is older than the configured session timeout  """
        ru =  getUtility(IRegistry)
        session_timeout = ru.forInterface(ISessionsControlSettings).session_timeout
        return not self.checkTimeout(session_timeout)

class UserProfile(object):
    """Defines the userprofile
    """
    def __init__(self):
        self.user_id     = u""                              
        self.sessions = []
        self.fullname    = u"" 
        self.maxSessions = 99
    
    def orderdSessions(self):
        return sorted(self.sessions, key=lambda session: time.mktime(session.timestamp.timetuple()), reverse=True)

class DBApi(object):
    """ DB Util
    """
    DATA = []
    last_deepclean = datetime.now() 

    def get_timeout(self):
        ru =  getUtility(IRegistry)
        return ru.forInterface(ISessionsControlSettings).session_timeout

    def getSessionUser(self, user_id):
        for user in self.DATA:
            if user.user_id == user_id:
                return user
        return None

    def deepclean(self):  
        # clear the old entries
        now = datetime.now()
        timeout =  now  - timedelta(seconds=REMOVEINACTIVE_SECONDS)
        if self.last_deepclean < timeout:
            #TESTRR
            logger.warning("deepclean")
            self.deleteInactiveSessions()
            self.last_deepclean = now

    def AddUserSession(self, member, member_maxSessions, session_id, session_ip):
        """ Add or refresh the user sessions
        """
        timestamp = datetime.now()
        user_id = member.getId()
        if user_id:
            user = self.getSessionUser(user_id)
            if not user:
                user = UserProfile()
                user.user_id = user_id
                user.name = member.getProperty('fullname') or member.getId()
                self.DATA.append(user)

            # Get or create the session
            session = None
            for s in user.sessions:
                if s.session_id == session_id:
                    session = s
                    break

            if not session:
                # This is a good moment to remove alte sessions
                self.deepclean()

                session = UserSession()
                session.session_id = session_id
                session.timestamp_login = timestamp
                user.sessions.append(session)
                if DEBUG:
                    logger.warning("session created for %s: %s"%(user_id, session.session_id))

            session.timestamp = timestamp
            session.ip = session_ip
            return session
        else:
            logger.error("Ignoring user (UserId is None)")

    def deleteUserSession(self, user_id):
        """ Remove the user """
        for user in self.DATA:
            if user.user_id == user_id:
                self.DATA.remove(user)
                return user
        return None

    def _deleteSessions(self, session_id=None, inactiveTimeout=None):
        """ Remove the sessions with 'session_id' 
            and/or if it is inactive for 'inactiveTimeout' seconds """
        for user in self.DATA[:]:
            for session in user.sessions[:]:
                if session_id and session_id == session.session_id:
                    user.sessions.remove(session)
                    if inactiveTimeout == None:
                        return session
                
                if inactiveTimeout != None and not session.isActive() and session.checkTimeout(inactiveTimeout):
                    #TESTRR
                    logger.warning("Removed inactive sessions: %s"%session.session_id)
                    user.sessions.remove(session)
            if len(user.sessions) <= 0:
                self.DATA.remove(user)

    def deleteInactiveSessions(self, inactiveTimeout=REMOVEINACTIVE_SECONDS):
        """ Remove old sessions """
        return self._deleteSessions(inactiveTimeout=inactiveTimeout)

    def deleteSession(self, session_id):
        """ Remove this session """
        return self._deleteSessions(session_id=session_id)

class DBUtils():
    """ Help functions
    """        
    def convertAttributesToDict(self, object):
        """Returns all public attributes of an object as a dict of attributes"""
        try:
            adict = dict((key, value) for key, value in object.__dict__.iteritems() 
                       if not callable(value) and not key.startswith('_'))
            return adict        
        except:
            return None
db  = DBApi()
