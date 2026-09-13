import os
import shutil
import stat
import tempfile
import unittest

try:
    import yaml
except ImportError:
    yaml = None

if yaml is not None:
    from pytumblr.credentials import load_credentials, save_credentials


@unittest.skipUnless(yaml is not None, "PyYAML is not installed")
class CredentialTests(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.directory)

    def path(self, name):
        return os.path.join(self.directory, name)

    def test_credentials_are_atomically_saved(self):
        path = self.path("credentials.yml")
        credentials = {
            "client_id": "id",
            "token": {"access_token": "secret"},
        }
        save_credentials(path, credentials)
        self.assertEqual(load_credentials(path), credentials)
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)

    def test_credentials_reject_symbolic_links(self):
        target = self.path("target.yml")
        link = self.path("credentials.yml")
        save_credentials(target, {"token": "secret"})
        try:
            os.symlink(target, link)
        except (AttributeError, NotImplementedError, OSError):
            self.skipTest("symbolic links are not available")
        with self.assertRaises((ValueError, OSError)):
            load_credentials(link)
