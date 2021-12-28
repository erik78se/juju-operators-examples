#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/olm/defining-and-using-persistent-storage

# storage-filesystem-attach
# storage-filesystem-detaching


import logging
import os
import shutil
import functools
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus
import sys

logger = logging.getLogger(__name__)

EMOJI_CORE_HOOK_EVENT = "\U0001F4CC"
EMOJI_CHECK_MARK_BUTTON = "\U00002705"
EMOJI_CROSS_MARK_BUTTON = "\U0000274E"
EMOJI_COMPUTER_DISK = "\U0001F4BD"

def logdecorate(prefix):
    """
    Adds output with a prefix string to any function.
    
    """
    def decorate(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            logger.debug(f"{prefix} {f.__name__} Args: {args} Kwargs: {kwargs}")
            cr = f(*args, **kwargs)
            logger.debug(f"{prefix} {f.__name__} Result: {cr}")
            return cr
        return wrapper
    return decorate


class StorageFilesystemCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.logdata_storage_attached, self._logdata_storage_attached)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.logdata_storage_detaching, self._logdata_storage_detaching)


    @logdecorate(EMOJI_COMPUTER_DISK)
    def _logdata_storage_attached(self, event):
        """
        Executes before install for new units.
        When type is filesystem, a default ext4 filesystem is mounted at the location
        defined in metadata.yaml

        Install and enable the systemd mount file for the attached storage-filesystem.
        """

        shutil.copyfile('templates/etc/systemd/system/var-log-mylogs.mount',
                        '/etc/systemd/system/var-log-mylogs.mount')
        os.system('systemctl daemon-reload')

        # Start the storage unit here, or in some other hook.
        os.system('systemctl enable var-log-mylogs.mount --now')


        # The event carries information of the storage for the unit.        
        storage_location = event.storage.location
        storage_name = event.storage.name
        storage_id = event.storage.id

        # The model has storages you can access like this.
        model_storages = self.model.storages

        logger.debug(f"{event.storage.location} {event.storage.name} {event.storage.id}")
        
        self.unit.status = ActiveStatus(f"{EMOJI_CHECK_MARK_BUTTON} Attached {storage_name}/{storage_id} at {storage_location} bind mount.")

    @logdecorate(EMOJI_CORE_HOOK_EVENT)
    def _on_install(self, event):
        """
        TODO: Render dynamically a unit-file based on the location name?
        1. Query the unit for enabled storage-filesystem.
        """
        self.unit.status = ActiveStatus(f"Ready (installed)")

    @logdecorate(EMOJI_COMPUTER_DISK)
    def _logdata_storage_detaching(self, event):
        """
        Disable the storage-filesystem and remove the unit file.
        """
        os.system('systemctl disable var-log-mylogs.mount --now')
        os.remove('/etc/systemd/system/var-log-mylogs.mount')
        self.unit.status = ActiveStatus(f"{EMOJI_CROSS_MARK_BUTTON} Detached storage.")

        
if __name__ == "__main__":
    main(StorageFilesystemCharm)
