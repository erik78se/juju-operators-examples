#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

# storage-filesystem-attach
# storage-filesystem-detaching

# RECOMMENDED: set debugging on the model to see more output:
# juju model-config logging-config="<root>=WARNING;unit=TRACE"

import logging
import os
import shutil

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, WaitingStatus
import subprocess as sp
import sys

logger = logging.getLogger(__name__)

EMOJI_CORE_HOOK_EVENT = "\U0001F4CC"
EMOJI_MESSAGE = "\U0001F4AC"
EMOJI_GREEN_DOT = "\U0001F7E2"
EMOJI_RED_DOT = "\U0001F534"
EMOJI_EXCLAMATION = "\U00002755"
EMOJI_PACKAGE = "\U0001F4E6"


class StorageCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.storage_attached, self._storage_attached)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.storage_detaching, self._storage_detaching)

    def _storage_attached(self, event):
        """
        Executes before install for new units.
        Install and enable the systemd mount file for the attached storage-filesystem.
        """
        shutil.copyfile('templates/etc/systemd/system/var-log-mylogs.mount',
                        '/etc/systemd/system/var-log-mylogs.mount')
        sp.check_call(['systemctl', 'daemon-reload'])
        sp.check_call(['systemctl', 'enable', 'var-log-mylogs.mount'])

    def _install(self, event):
        """
        Query the unit for enabled storage-filesystem. ---> How?
        """
        pass

    def _storage_detaching(self, event):
        """
        Disable the storage-filesystem and remove the unit file.
        """
        sp.check_call(['systemctl', 'disable', 'var-log-mylogs.mount'])
        os.remove('/etc/systemd/system/var-log-mylogs.mount')

if __name__ == "__main__":
    main(StorageCharm)
