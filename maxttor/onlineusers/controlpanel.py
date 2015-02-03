#-*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from maxttor.onlineusers.interfaces import ISessionsControlSettings
from maxttor.onlineusers.interfaces import _

class sessionscontrolSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ISessionsControlSettings
    label = _(u"Online Session Control")
    description = _(u"""Control the online users and sessions.
    """)

    def updateFields(self):
        super(sessionscontrolSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(sessionscontrolSettingsEditForm, self).updateWidgets()

class sessionscontrolSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = sessionscontrolSettingsEditForm
