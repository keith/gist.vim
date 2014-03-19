import unittest
from auth import user


class TestUsers(unittest.TestCase):
    def test_netrc(self):
        path = "/Users/ksmiley/netrc"
        u = user.User.from_netrc(path, "github.com")
        self.assertEqual(u.username, "foo")


if __name__ == "__main__":
    unittest.main()
