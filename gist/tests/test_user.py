from gist.auth import user
import tempfile
import os
import unittest

URL = "foobar.com"
USERNAME = "foo"
PASSWORD = "bar"


class TestUsers(unittest.TestCase):
    def test_netrc_login(self):
        text = "machine %s\n\tlogin %s\n\tpassword bar" % (URL, USERNAME)
        name = make_temp(text)
        u = user.User.from_netrc(name, URL)
        os.remove(name)
        self.assertEqual(u.username, USERNAME)

    def test_netrc_username(self):
        text = "machine %s\n\taccount %s\n\tpassword bar" % (URL, USERNAME)
        name = make_temp(text)
        u = user.User.from_netrc(name, URL)
        os.remove(name)
        self.assertEqual(u.username, USERNAME)

    def test_string(self):
        u = make_user()
        self.assertRegex(u.__str__(), r".*Username: %s.*" % USERNAME)

    def test_creation(self):
        u = user.User(USERNAME, PASSWORD, URL)
        self.assertEqual(u.username, USERNAME)
        self.assertEqual(u.password, PASSWORD)
        self.assertEqual(u.url, URL)


def make_temp(text):
    _, name = tempfile.mkstemp()
    f = open(name, "w")
    if not text:
        text = "machine %s\n\tlogin %s\n\tpassword bar" % (URL, USERNAME)
    f.write(text)
    f.close()
    return name


def make_user():
    name = make_temp(None)
    u = user.User.from_netrc(name, URL)
    os.remove(name)
    return u


if __name__ == "__main__":
    unittest.main()
