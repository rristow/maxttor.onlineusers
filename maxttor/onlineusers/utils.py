# -*- coding: utf-8 -*-
import sys
import json
import logging
from urllib import quote, unquote
from maxttor.onlineusers.config import DEBUG, COOKIE_NAME

logger = logging.getLogger('maxttor.sessioncontorl')    

def getCookie(request):
    cookie = request.get(COOKIE_NAME, '')
    return unquote(cookie)

def setCookie(request, value):
    """ Save the cookie. Setting to '' means delete."""
    response = request['RESPONSE']
    value = quote(value)
    if value:
        response.setCookie(COOKIE_NAME, value, path='/')
    else:
        response.expireCookie(COOKIE_NAME, path='/')

class JsonDump():
    """ Json dump utils"""
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