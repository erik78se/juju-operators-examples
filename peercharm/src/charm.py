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
          RelationChangedEvent  -> When data is changed on the relation, non-leaders.
          RelationJoinedEvent   -> When a unit joins, leader sends new config.
          RelationDepartedEvent -> When a unit leves a relation, leader sends new config.
        """
        
        if not self.model.unit.is_leader() and isinstance(event, RelationChangedEvent):
            logger.info("Non leader got new config from cluster relation.")
            config = self.model.get_relation("cluster").data[self.app]["config.php"]
            logger.info("Non leader writing new config from relation:" + config)
            self.write_config_file(config)
            self.unit.status = ops.ActiveStatus(f"Loglevel: {self.model.config['log-level']}")
            return
        
        if self.model.unit.is_leader() and ( isinstance(event, RelationJoinedEvent) or isinstance(event, RelationDepartedEvent) ):
            logger.info("Leader generates new config since we have new or departing units.")
            self.write_config_file(self.assemble_config())
            logger.info("Leader sends new config on the relation (relation-joined/departed).")
            self.model.get_relation("cluster").data[self.app]["config.php"] = self.read_config_file()
            self.unit.status = ops.ActiveStatus(f"Loglevel: {self.model.config['log-level']}")
 
        if self.model.unit.is_leader():
            logger.warning("Leader not sure to handle this event for a :" + str(event))
        else:
            logger.warning("Non-leader not sure to handle this event for a :" + str(event))

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        """Handle changed configuration."""
        if not self.model.unit.is_leader():
            # Non leaders don do anything.
            return

        # Fetch config        
        log_level = self.model.config["log-level"].lower()

         # Do some validation of the configuration option
        if log_level in VALID_LOG_LEVELS:
            logger.debug("Log level changed to '%s'", log_level)
            self.unit.status = ops.ActiveStatus(f"Loglevel: {log_level}")
        else:
            self.unit.status = ops.WaitingStatus(f"Incorrect log-level, no config written: {log_level}")
        
        # Write config
        logger.info("Leader generates new config (since we have changed config.)")
        self.write_config_file(self.assemble_config())
        logger.info("Leader sends new config on the relation (config-changed).")
        self.model.get_relation("cluster").data[self.app]["config.php"] = self.read_config_file()

    
    def _remove_unit_from_peers(self, unit):
        """
        Is it the responsibility of the charmer to implement the removal of peers?
        """
        relation = self.model.get_relation("cluster")
        if relation and unit in relation.units:
            self.unit.status = MaintenanceStatus("Removing unit from cluster peer-relation")
            relation.units.remove(unit)
            self._update_peers_relation_data()

    def on_peers_relation_departed(self, event: RelationDepartedEvent):
        self._remove_unit_from_peers(event.unit)


    def assemble_config(self):
        """ Assembles config."""
        log_level = self.model.config["log-level"].lower()
        unit_ips = []
        if self.model.unit.is_leader():
            leader = self.model.unit
        try:
            relation = self.model.get_relation("cluster")
            for unit_or_app in relation.data:
                if unit_or_app.name != self.app.name:
                    unit_ips.append(relation.data[unit_or_app]["private-address"])
        except KeyError:
            # Doesn't yet exist
            unit_ips = ""
        
        content = str(
            f"log-level={log_level}\n"
            f"leader={leader.name}\n"
            f"unit-ips={unit_ips}"
            f"\n"
            )
        return content

    def write_config_file(self, content):
        """Write config to file."""
        with open(CONFIG_FILE, "w") as file:            
            file.write(content)

    def read_config_file(self):
        """ Read config file, return content as a String"""
        with open(CONFIG_FILE, "r") as file:            
            file_content = file.read()
        return file_content

if __name__ == "__main__":
    ops.main.main(PeerCharm)
