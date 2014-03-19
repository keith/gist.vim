import netrc
import urllib2


class User(object):
    username = None
    password = None
    url = None

    def __init__(self, username, password, url=None):
        self.username = username
        self.password = password
        self.url = url

    def __str__(self):
        return "Username: %s, URL: %s" % (self.username, self.url)

    @classmethod
    def authorize(cls, username, password, url, save=True):
        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, url, username, password)
        urllib2.install_opener(urllib2.build_opener(
                               urllib2.HTTPBasicAuthHandler(p)))
        req = urllib2.Request(url)
        pipe = urllib2.urlopen(req)
        data = pipe.read()
        print(data)

    @classmethod
    def from_netrc(cls, path=None, url=None):
        rc = netrc.netrc(path)
        creds = rc.authenticators(url)
        if not creds:
            return None
        login, account, password = creds
        if not login:
            login = account
        if not login or not password:
            return None
        return User(login, password, url)
