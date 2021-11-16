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

class LxdProfileCharm(CharmBase):
    """
        This charm demonstrate use of lxd-profile.yaml
        Note that you need to change the charm file for this to take effect.
        There are some examples in README.md
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)

    def _on_upgrade_charm(self, event):
        """
            The lxd-profile.yaml gets updated as part of a upgrade-charm event.
        """
        logger.info("LXD profile is updated!")
        self.unit.status = ActiveStatus("LXD profile was updated.")


if __name__ == "__main__":
    main(LxdProfileCharm)
