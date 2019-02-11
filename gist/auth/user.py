"""
Get users from the netrc credentials file for use with Github
Maintained by: Keith Smiley <http://keith.so>
"""
import netrc
import urllib.parse


class User(object):
    def __init__(self, username, password, url=None):
        self.username = username
        self.password = password
        self.url = url

    def __str__(self):
        return "Username: %s, URL: %s" % (self.username, self.url)

    @classmethod
    def from_netrc(cls, path=None, url=None):
        parsed_url = urllib.parse.urlparse(url)
        base_url = parsed_url.netloc
        if not base_url:
            base_url = parsed_url.path
        if not base_url:
            base_url = url

        credential = netrc.netrc(path).authenticators(base_url)
        if not credential:
            return None
        login, account, password = credential
        if not login:
            login = account
        if not login or not password:
            return None

        return User(login, password, url)
