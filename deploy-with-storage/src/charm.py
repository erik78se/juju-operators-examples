#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

import logging
from ops.charm import CharmBase
from ops.main import main
from ops.model import MaintenanceStatus, ActiveStatus

logger = logging.getLogger(__name__)

class DeployMinimalStorageCharm(CharmBase):
    """
    A charm which implements the deployment hooks including the storage hooks.

    foobar_storage_attached -> install -> config_changed -> start

    """

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.foobar_storage_attached, self._on_foobar_storage_attached)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.start, self._on_start)

    def _on_foobar_storage_attached(self, event):
        """
            [foobar]_storage_attached is a core hook only fireing when
            storage with the name [foobar] defined in metadata.yaml
        """
        logger.info("Step 1/4: STORAGE_ATTACHED")
        self.unit.status = MaintenanceStatus("Step: 1/4")

    def _on_install(self, event):
        """
            install is the first core hook to fire when deploying.
        """
        logger.info("Step 2/4: INSTALL")
        self.unit.status = MaintenanceStatus("Step: 2/4")

    def _on_config_changed(self, event):
        """
            config_changed is second core hook to fire when deploying.
        """
        logger.info("Step 3/4: CONFIG_CHANGED")
        self.unit.status = MaintenanceStatus("Step: 3/4")

    def _on_start(self, event):
        """
            start is the last core hook to fire when deploying.
        """
        logger.info("Step 4/4: START")
        self.unit.status = ActiveStatus("Step: 4/4")


if __name__ == "__main__":
    main(DeployMinimalStorageCharm)
