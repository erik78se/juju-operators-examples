#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk


import logging
import os
from ops.charm import CharmBase
from ops.main import main

from charmhelpers.contrib.charmsupport.nrpe import NRPE
from charmhelpers.core import hookenv, host

logger = logging.getLogger(__name__)

EMOJI_CORE_HOOK_EVENT = "\U0001F4CC"

NAGIOS_PLUGINS_DIR = "/usr/local/lib/nagios/plugins/"

class NrpeCharm(CharmBase):
    """A nrpe charm."""
    
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.nrpe_external_master_relation_created,
                               self._on_nrpe_external_master_relation_created)

    def _on_nrpe_external_master_relation_created(self, event):
        """Handle nrpe-external-master relation joined."""
        
        # Get plugins in place.
        self.update_plugins()

        # Render checks
        self.render_checks()

        # Restart nrpe
        self.restart_nrpe_service()


    @property
    def plugins_dir(self):
        """Get nagios plugins directory."""
        return NAGIOS_PLUGINS_DIR

    def restart_nrpe_service(self):
        """Restart nagios-nrpe-server service."""
        host.service_restart("nagios-nrpe-server")    

    def update_plugins(self):
        """Rsync plugins to the plugin directory."""
        checkscript = os.path.join(hookenv.charm_dir(), "files", "nrpe-external-master/check_hello.sh")
        host.rsync(checkscript, NAGIOS_PLUGINS_DIR, options=["--executability"])

    def render_checks(self):
        """Render nrpe checks."""
        nrpe = NRPE()
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)

        # register basic test
        
        nrpe.add_check(
            shortname="hellocheck",
            description="Dummy hello check",
            check_cmd="check_hello.sh",
        )
        nrpe.write()
        
    
if __name__ == "__main__":
    main(NrpeCharm)
