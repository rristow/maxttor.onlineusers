#-*- coding: utf-8 -*-

from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('maxttor.sessioncontrol')

class ISessionsControlSettings(Interface):
    """Global whoisonline settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    enabled = schema.Bool(
            title=_(u"Enabled"),
            description=_(u"Enabled the session control for all users"),
            required=True,
            default=True,
        )

    restrictSessions = schema.Bool(
            title=_(u"restrict sessions"),
            description=_(u"restrict the number of sessions (max sessions) per user at login"),
            required=True,
            default=True,
        )

    session_maximun = schema.Int(
            title=_(u"Max. sessions"),
            description=_(u"The maximum number of sessions allowed"),
            required=True,
            default=3,
        )

    session_timeout = schema.Int(
            title=_(u"Session timeout"),
            description=_(u"For how long should a user be marked as online? (Seconds) "),
            required=True,
            default=600,
        )

    session_ping_interval = schema.Int(
            title=_(u"Refresh interval for the session"),
            description=_(u"Enter refresh interval for the refresh connections (Ajax). \
                    IMPORTANT: Be aware that time period less then 60 seconds may slow down your server! \
                    Time periods less then 4 seconds are not considered."),
            required=True,
            default=60,
        )
   
class ISessionsControl(Interface):
    """Marker interface
    """
