#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

import logging

import ops

logger = logging.getLogger(__name__)

class DeployMinimalCharm(ops.CharmBase):
    """
        A minimalistic charm which only implements the deployment hooks

        install -> config_changed -> start
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.start, self._on_start)

    def _on_install(self, event):
        """
            install is the first core hook to fire when deploying.
        """
        logger.info("Step 1/3: INSTALL")
        self.unit.status = ops.MaintenanceStatus("Step: 1/3")

    def _on_config_changed(self, event):
        """
            config_changed is second core hook to fire when deploying.
        """
        logger.info("Step 2/3: CONFIG_CHANGED")
        self.unit.status = ops.MaintenanceStatus("Step: 2/3")

    def _on_start(self, event):
        """
            start is the last core hook to fire when deploying.
        """
        logger.info("Step 3/3: START")
        self.unit.status = ops.ActiveStatus("Step: 3/3")


if __name__ == "__main__":
    ops.main(DeployMinimalCharm)
