import XenAPI
from vdt.deploy import api, pretty
from vdt.deploy.userdata import UserData
from vdt.deploy.utils import find_by_key, \
    find_machine, wrap, sort_by_key, is_puppetmaster, check_call_with_timeout
from vdt.deploy.certificate import add_pending_certificate
from vdt.deploy.config import cfg

__all__ = ('Provider',)


class Provider(api.CmdApi):
    """XenAPI Deployment CMD Provider"""
    prompt = "xen> "

    def __init__(self):
        self.session = XenAPI.Session(cfg.APIURL)
        self.session.login_with_password(cfg.USERNAME, cfg.PASSWORD)
        api.CmdApi.__init__(self)

    def do_status(self, all=False):
        """
        Shows running instances, specify 'all' to show all instances

        Usage::

            xen> status [all]
        """
        vms = self.session.xenapi.VM.get_all()
        result = []
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record['is_a_template'] and not record['is_control_domain']:
                result.append({'id': record['uuid'],
                               'displayname': record['name_label'],
                               'state': record['power_state']})

        machines = sort_by_key(result, 'displayname')
        if not all:
            ACTIVE = ['Running', 'SHuttingDown']
            machines = [x for x in machines if x['state'] in ACTIVE]

        pretty.machine_print(machines)

    def do_quit(self, _=None):
        """
        Quit the deployment tool.

        Usage::

            cloudstack> quit
        """
        return True
