import os
import sys
import mox
import subprocess
import unittest
import vdt.deploy.config
import XenAPI

from StringIO import StringIO
from base64 import encodestring

import vdt.deployplugin.xen.provider
import vdt.deploy.tool

from vdt.deploy.tests import testdata
from vdt.deployplugin.xen import mockconfig
from vdt.deploy.utils import StringCaster


class ProviderCloudstackTest(unittest.TestCase):

    def setUp(self):
        reload(mockconfig)
        self.mockconfig = mockconfig.MockConfig
        vdt.deploy.tool.cfg = self.mockconfig
        vdt.deployplugin.xen.provider.cfg = self.mockconfig
        vdt.deployplugin.xen.provider.Session = mockconfig.MockSession
        self.client = vdt.deployplugin.xen.provider.Provider()
        self.saved_stdout = sys.stdout
        self.out = StringIO()
        sys.stdout = self.out

    def tearDown(self):
        sys.stdout = self.saved_stdout
        self.out = None

    def test_do_status(self):
        self.client.do_status()
        output = self.out.getvalue()
        self.assertEqual("", output)

    def test_do_status_all(self):
        self.client.do_status(all=True)
        output = self.out.getvalue()
        self.assertTrue("puppetmaster" in output)
