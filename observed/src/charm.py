#!/usr/bin/env python3

import os
import subprocess as sp

import ops
from charms.grafana_agent.v0.cos_agent import COSAgentProvider

EMOJI_GREEN_DOT = "\U0001F7E2"

class ObservedCharm(ops.CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        
        # Define data to send to grafana-agent and 
        # provide paths to dashboards + alert-rules.
        # The COSAgentProvider is added to the source tree from
        #     charmcraft fetch-lib charms.grafana_agent.v0.cos_agent
        # Changes to the rules/dashboards will be updated automatically if the charm
        # is updated.
        
        self._grafana_agent = COSAgentProvider(
            self, metrics_endpoints=[
                {"path": "/metrics", "port": self.config.get('port')},
            ],
            metrics_rules_dir="./src/alert_rules/prometheus",
            logs_rules_dir="./src/alert_rules/loki"
        )

        # Observe core Juju events
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)


    def _on_install(self, theevent):
        # Install from configured channel
        channel = self.config.get('channel')
        self.unit.status = ops.MaintenanceStatus("Installing microsample snap")
        os.system(f"snap install microsample --{channel}")
        self.unit.status = ops.ActiveStatus(EMOJI_GREEN_DOT + " Ready")


    def _on_config_changed(self, theevent):
        # Get port & private address
        port = self.config.get('port')
        cmd = "unit-get private-address"
        
        address = sp.check_output(cmd.split(), 
                                  stdin = None, stderr = None, 
                                  shell = False, universal_newlines = True)
    
        # Set config for the snap and restart.
        os.system(f"snap set microsample address={address}")
        os.system(f"snap set microsample port={port}")
        os.system("systemctl restart snap.microsample.microsample")

    def _on_upgrade_charm(self, theevent):
        # Upgrade triggers an install.
        channel = self.config.get('channel')
        os.system(f"snap install microsample --{channel}")

        # Set workload version
        self.unit.set_workload_version("1.0")
        
        # Set active status.
        self.unit.status = ops.ActiveStatus(EMOJI_GREEN_DOT + " Ready")


if __name__ == "__main__":
    ops.main(ObservedCharm)
