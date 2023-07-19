#!/usr/bin/env python3
# Copyright 2023 Erik Lönroth
# See LICENSE file for licensing details.

import logging

from ops.charm import (CharmBase, 
                       RelationBrokenEvent, 
                       RelationChangedEvent,
                       RelationDepartedEvent, 
                       RelationJoinedEvent)

from ops.model import (ActiveStatus, 
                       MaintenanceStatus,
                       WaitingStatus,
                       ModelError)

from ops.framework import (
                        StoredState 
                        )
import ops

logger = logging.getLogger(__name__)

VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]
CONFIG_FILE = "/tmp/config.php"

class PeerCharm(CharmBase):
    state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.state.set_default(configfile="")
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.cluster_relation_joined, self._on_cluster_relation_handler)
        self.framework.observe(self.on.cluster_relation_changed, self._on_cluster_relation_handler)
        self.framework.observe(self.on.cluster_relation_departed, self._on_cluster_relation_handler)
        
    def _on_cluster_relation_handler(self, event):
        """
        Handle events affecting the relation.
        The events we care about for a peer relation are: 
          RelationJoinedEvent   -> When a unit joins.
          RelationChangedEvent  -> When data is changed on the relation.
          RelationDepartedEvent -> When a unit leves a relation.
        """
        
        # Leader writes config and sends it to peers
        if not self.model.unit.is_leader():
            return
    
        log_level = self.model.config["log-level"].lower()
        self.write_config_file(log_level)
        # self.model.get_relation("cluster").data[self.app]["config.php"] = self.read_config_file()
        # self.on.config_changed.emit()
  
    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        """Handle changed configuration."""

        # Fetch config        
        log_level = self.model.config["log-level"].lower()

         # Do some validation of the configuration option
        if log_level in VALID_LOG_LEVELS:
            logger.debug("Log level changed to '%s'", log_level)
            self.unit.status = ops.ActiveStatus(f"Loglevel: {log_level}")
        else:
            self.unit.status = ops.WaitingStatus(f"Incorrect log-level, no config written: {log_level}")
        
        if self.model.unit.is_leader():
            self.model.get_relation("cluster").data[self.app]["config.php"] = self.read_config_file()
        else:
            self.write_config_file(log_level)

    
    def _remove_unit_from_peers(self, unit):
        """
        Is it the responsibility of the charmer to implement the removal of peers?
        """
        relation = self.model.get_relation("peering")
        if relation and unit in relation.units:
            self.unit.status = MaintenanceStatus("Removing unit from peers relation")
            relation.units.remove(unit)
            self._update_peers_relation_data()

    def on_peers_relation_departed(self, event: RelationDepartedEvent):
        self._remove_unit_from_peers(event.unit)

    def write_config_file(self, log_level):
        """Write our config file."""
        with open(CONFIG_FILE, "w") as file:            
            try:
                unit_ips = self.model.get_relation("cluster").data[self.app]["unit-ips"]
            except KeyError:
                # Doesn't yet exist
                unit_ips = ""
            file.write(
                f"log-level={log_level}\n"
                f"leader={self.unit.name}\n"
                f"unit-ips={unit_ips}"
                f"\n"
            )

    def read_config_file(self):
        """ Read config file, return content as a String"""
        with open(CONFIG_FILE, "r") as file:            
            file_content = file.read()
        return file_content

if __name__ == "__main__":
    ops.main.main(PeerCharm)
