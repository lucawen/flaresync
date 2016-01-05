#!/usr/bin/python

try:
    import httplib
except ImportError:
    import http.client as httplib

import json
import urllib
import re
import sys, getopt
from requests import get

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
        address = get('http://api.ipify.org').text
        addressNow = self.getContent("content")
        if address != addressNow:
            if addressNow != None:
                addressNow = address
                self.changeIP(address)
                print "IP Changed"
            else:
                print "Name Record not found."
        else:
            print "IP not changed"

    def getContent(self, content):
        rec_load_all = self.Call( "a=%s&email=%s&tkn=%s&z=%s&o=%s" % ( 'rec_load_all', self.ac, self.key, self.domain, 0) )
        lists_dns = rec_load_all['response']['recs']['objs']
        for dnsrec in lists_dns:
            if self.host == dnsrec['display_name']:
                return dnsrec[content]
        return None

    def changeIP( self, content):
        fmt = "a=rec_edit&tkn=%s&id=%s&email=%s&z=%s&type=A&name=%s&content=%s&ttl=1"
        return self.Call( fmt % (self.key, self.getContent("rec_id"), self.ac, self.domain, self.host, content))

    def Call(self, url):
        con = httplib.HTTPSConnection('www.cloudflare.com')
        con.request('GET', '/api_json.html?'+url)
        response = con.getresponse()
        data = response.read().decode('utf-8')
        data = json.loads(data)
        return data

def main(argv):
    try:
        opt, args = getopt.getopt(argv, "h:m:k:d:n:", ["help", "mail=", "key=", "domain=", "name="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opt:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--mail"):
            mArg = a
        elif o in ("-k", "--key"):
            kArg = a
        elif o in ("-d", "--domain"):
            dArg = a
        elif o in ("-n", "--name"):
            nArg = a
        else:
            assert False, "unhandled option"

    try:
        cloud = FlareSync(mArg, kArg, dArg, nArg)
        cloud.checkIP()
    except:
        print "An error has occurred. Are you sure you enter the e-mail, key and correct domain? Type -h for help"
        sys.exit(2)
def usage():
    usage = """
    -h --help                 Help commands
    -m --mail (arg)           Your cloudflare mail account
    -k --key  (arg)           Your secret key
    -d --domain (arg)         The domain record
    -n --name (arg)           The DNS Record name
    """
    print usage

if __name__ == "__main__":
    main(sys.argv[1:])