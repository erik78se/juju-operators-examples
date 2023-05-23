#!/usr/bin/env python3

from charms.grafana_agent.v0.cos_agent import COSAgentProvider
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus
import os
import stat
import logging
import sys
import subprocess as sp
from pathlib import Path
import jinja2


EMOJI_CORE_HOOK_EVENT = "\U0001F4CC"
EMOJI_GREEN_DOT = "\U0001F7E2"

logger = logging.getLogger(__name__)

class ObservedCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        self._grafana_agent = COSAgentProvider(
            self, metrics_endpoints=[
                {"path": "/metrics", "port": self.config.get('port')},
            ],
            metrics_rules_dir="./src/alert_rules/prometheus",
            logs_rules_dir="./src/alert_rules/loki"
        )
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.install, self._on_what_we_do_in_install)
        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)


    def _on_what_we_do_in_install(self, theevent):
        
        logger.debug(EMOJI_CORE_HOOK_EVENT + sys._getframe().f_code.co_name)

        channel = self.config.get('channel')

        self.unit.status = MaintenanceStatus("Installing microsample snap")

        os.system(f"snap install microsample --{channel}")

        self.unit.status = ActiveStatus(EMOJI_GREEN_DOT + " Ready")


    def _on_config_changed(self, theevent):

        logger.debug(EMOJI_CORE_HOOK_EVENT + sys._getframe().f_code.co_name)

        cmd = "unit-get private-address"
        
        address = sp.check_output(cmd.split(), stdin = None, stderr = None, shell = False, universal_newlines = True)
        
        os.system(f"snap set microsample address={address}")

        port = self.config.get('port')

        os.system(f"snap set microsample port={port}")

        os.system("systemctl restart snap.microsample.microsample")

        # Render a custom motd.

        message = self.config.get('message')

        template = jinja2.Environment(loader=jinja2.FileSystemLoader('templates')).get_template('11-jujuwashere')
        target = Path('/etc/update-motd.d/11-jujwashere')
        ctx = { 'name': message }
        target.write_text(template.render(ctx))
        st = os.stat(target)
        os.chmod(target, st.st_mode | stat.S_IEXEC)

    def _on_upgrade_charm(self, theevent):

        logger.debug(EMOJI_CORE_HOOK_EVENT + sys._getframe().f_code.co_name)

        # Debugging!
        channel = self.config.get('channel')

        logger.debug(f"Our channel is: {channel}")

        os.system(f"snap install microsample --{channel}")

        # Set the version of the snap here.
        self.unit.set_workload_version("1.0")

        self.unit.status = ActiveStatus(EMOJI_GREEN_DOT + " Ready")




if __name__ == "__main__":
    main(ObservedCharm)
