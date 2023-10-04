#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.

import os

import ops
from charmhelpers.contrib.charmsupport.nrpe import NRPE
from charmhelpers.core import hookenv, host

NAGIOS_PLUGINS_DIR = "/usr/local/lib/nagios/plugins/"

class MonitoringNrpeCharm(ops.CharmBase):
    """
    A charm that deploys a monitoring script and allows to be
    related to nrpe:local-monitors to be used with nagios.
    
    juju deploy nagios
    juju deploy nrpe
    juju deploy ./monitoring-nrpe_ubuntu-20.04-amd64.charm
    juju relate nagios:monitors nrpe:monitors
    juju relate monitoring-nrpe:local-monitors nrpe

    """
    
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.local_monitors_relation_changed,
                               self._on_nrpe_changed)

    def _on_nrpe_changed(self, event):
        """Handle nrpe relations changed."""
        
        # Get plugins in place.
        self.update_plugins()

        # Render checks
        self.render_checks()

        # Restart nrpe
        self.restart_nrpe_service()

        # Set active status
        self.unit.status = ops.ActiveStatus("Monitoring")


    @property
    def plugins_dir(self):
        """Get nagios plugins directory."""
        return NAGIOS_PLUGINS_DIR

    def restart_nrpe_service(self):
        """Restart nagios-nrpe-server service."""
        host.service_restart("nagios-nrpe-server")    

    def update_plugins(self):
        """Rsync plugins to the plugin directory."""
        checkscript = os.path.join(hookenv.charm_dir(), "files", "nrpe-checks/check_hello.sh")
        host.rsync(checkscript, NAGIOS_PLUGINS_DIR, options=["--executability"])

    def render_checks(self):
        """Render nrpe checks."""
        nrpe = NRPE()
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)

        # Register a basic test.
        # Just add more with add_check before nrpe.write()
        
        nrpe.add_check(
            shortname="hellocheck",
            description="Dummy hello check",
            check_cmd="check_hello.sh",
        )
        nrpe.write()
        
    
if __name__ == "__main__":
    ops.main(MonitoringNrpeCharm)
