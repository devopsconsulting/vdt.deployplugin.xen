class MockConfig(object):
    PROVIDER = "xen"
    PUPPETMASTER = "localhost"
    PUPPETMASTER_VERIFIED = "1"
    CLEANUP_TIMEOUT = 20

    PUPPET_BINARY = "/usr/bin/puppet"
    PUPPET_CERT_DIRECTORY = "/tmp"
    CERT_REQ = "/tmp/cert_req.txt"

    APIURL = "http://localhost"
    USERNAME = "ROOT"
    PASSWORD = "PASSWORD"
    CLOUDINIT_PUPPET = "http://localhost/autodeploy/vdt-puppet-agent.cloudinit"
    CLOUDINIT_BASE = "http://localhost/autodeploy/vdt-puppet-base.cloudinit"

    @classmethod
    def update(self, values):
        for key, value in values:
            setattr(self, key.upper(), value)


class MockVM(object):

    def get_all(self):
        return [1, 2]

    def get_record(self, id):
        if id == 1:
            return {'uuid': '1', 'name_label': 'template', 'power_state': 'Unknown', 'is_a_template': True, 'is_control_domain': False}
        elif id == 2:
            return {'uuid': '2', 'name_label': 'puppetmaster', 'power_state': 'Halted', 'is_a_template': False, 'is_control_domain': False}


class MockXenAPI(object):

    @property
    def VM(self):
        return MockVM()


class MockSession(object):

    def __init__(self, url):
        pass

    def login_with_password(self, username, password):
        return True

    @property
    def xenapi(self):
        return MockXenAPI()
