#!/usr/bin/python

try:
    import httplib
except ImportError:
    import http.client as httplib

import json
import urllib
import re
import ipgetter

class FlareSync(object):
    def __init__(self, ac, key, domain, host):
        self.domain = domain
        self.ac = ac
        self.key = key
        self.host = host
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Key': key,
            'X-Auth-Email': ac,
        }

    def checkIP(self):
        addressServer = ipgetter.myip()
        addressCF = self.getContent("content")
        if addressCF != addressServer:
            self.editIP(address)
            print "IP Mudado!!!!!"

    def getContent(self, content):
        rec_load_all = self.Call( "a=%s&email=%s&tkn=%s&z=%s&o=%s" % ( 'rec_load_all', self.ac, self.key, self.domain, 0) )
        lists_dns = rec_load_all['response']['recs']['objs']
        for dnsrec in lists_dns:
            if self.host == dnsrec['display_name']:
                return dnsrec[content]
        return None

    def editIP( self, content):
        fmt = "a=rec_edit&tkn=%s&id=%s&email=%s&z=%s&type=A&name=%s&content=%s&ttl=1"
        return self.Call( fmt % (self.key, self.getContent("rec_id"), self.ac, self.domain, self.host, content))

    def Call(self, url):
        con = httplib.HTTPSConnection('www.cloudflare.com')
        con.request('GET', '/api_json.html?'+url)
        response = con.getresponse()
        data = response.read().decode('utf-8')
        data = json.loads(data)
        return data
