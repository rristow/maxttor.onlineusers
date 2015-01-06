# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from maxttor.sessioncontrol.sessionControlTool import sessionTool
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from maxttor.sessioncontrol.interfaces import ISessionsControlSettings
from maxttor.sessioncontrol.config import DEBUG, USER_ID_BLACKLIST
from zope.viewlet.interfaces import IViewlet


class AjaxSessionsControlCall_(BrowserView):
    implements(IViewlet)
    render = ViewPageTemplateFile('sessioncontrol-call.pt')

    def __init__(self, context, request, view, manager):
        super(AnalyticsTrackingViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    def getConfig(self):
        return sessionTool.getConfig()

    def update(self):
        pass
       
    def isActive(self):
        context = aq_inner(self.context)
        return sessionTool.isActive(context)

class OnlineTrackingView(BrowserView):
    """ list & control online users """
    template = ViewPageTemplateFile('sessioncontrol.pt')

    def __call__(self):
        context = aq_inner(self.context)        
        request = context.REQUEST
        #request.set('disable_border', True)

        action = request.get('action')
        user_id = request.get('user_id')

        if action == "delete_session":
            session_id = request.get('session_id')
            sessionTool.deleteSession(session_id=session_id)
        elif action == "delete_user":
            user_id = request.get('user_id')
            sessionTool.deleteUserSession(user_id=user_id)
        return self.template()

    def get_sessiondata(self):
        """ get the short profile of users """
        return sessionTool.get_sessiondata()
