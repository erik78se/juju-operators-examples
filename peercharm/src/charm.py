#!/usr/bin/env python3
# Copyright 2023 Erik Lönroth
# See LICENSE file for licensing details.

import json
import logging
from datetime import datetime
import random
import string

from ops.charm import (CharmBase, RelationBrokenEvent, RelationChangedEvent,
                       RelationDepartedEvent, RelationJoinedEvent)
from ops.framework import StoredState
from ops.model import (ActiveStatus, MaintenanceStatus, ModelError,
                       WaitingStatus)

import ops

logger = logging.getLogger(__name__)

class PeerCharm(CharmBase):
    state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.state.set_default(is_ready=False, configfile="")
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.peering_relation_joined, self._on_peers_relation_joined)
        self.framework.observe(self.on.peering_relation_changed, self._on_peers_relation_changed)
        self.framework.observe(self.on.peering_relation_departed, self._on_peers_relation_departed)
        self.framework.observe(self.on.update_config_action, self._on_update_config_action)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.stop, self._on_stop)

    def _on_update_config_action(self,event):
        """
        Update the random element in the config - simulating a change to a config.
        """
        relation = self.model.get_relation("peering")
        try:
            conf = event.params['config']
            relation.data[self.app].update({"config": conf})
        except(ops.model.RelationDataAccessError):
            logger.warning("Non leader unit prevented from setting application data.")
        except Exception as e:
            logger.error("Failed to set relation data:" + str(e))
            return

        self.unit.status = ActiveStatus("Updated config: " + datetime.now().time().strftime("%H:%M:%S"))

    def _on_config_changed(self, event):
        relation = self.model.get_relation("peering")
        if relation:
            # Show all units on the relation peering.
            logger.info(str(relation.units))
        
        if self.state.is_ready:
            logger.info("Changed config event handled.")
            self._update_peers_relation_data()
        else:
            logger.info("Not ready, not handling config change.")
            
    def _on_peers_relation_joined(self, event):
        if self.state.is_ready:
            self._update_peers_relation_data()

    def _on_peers_relation_changed(self, event):
        if self.state.is_ready:
            self._update_peers_relation_data()
            logger.info("I got updated information on the peering relation.")

    def _on_peers_relation_departed(self, event):
        if self.state.is_ready:
            self._update_peers_relation_data()


    def _update_peers_relation_data(self):
        """

        """
        relation = self.model.get_relation("peering")
        
        if not relation:
            self.unit.status = MaintenanceStatus("Waiting for peers relation")
            return
        else:
            # Generate config.
            c = "Unit: "

            # Write config to state.
            units = [unit.name for unit in relation.units]
            if not len(units) == 0:
                # Write config to state.
                logger.info(f"Wring to state.configfile: {str(units)}")
                # This loops if uncommented below
                # self.state.configfile = "Units: " + c.join(units) + " " + self.generate_random_string()
                self.state.configfile = "Units: " + c.join(units)
            else:
                logger.warning("There are no units in the relation. I'm alone.")
        try:
            # Push the data to the relation (Juju will make non leaders will fail.)
            relation.data[self.app].update({"config": self.state.configfile})
        except(ops.model.RelationDataAccessError):
            logger.warning("Non leader unit prevented from setting application data.")
        
        self.unit.status = ActiveStatus("Updated: " + datetime.now().time().strftime("%H:%M:%S"))

    def _remove_unit_from_peers(self, unit):
        relation = self.model.get_relation("peering")
        if relation and unit in relation.units:
            self.unit.status = MaintenanceStatus("Removing unit from peers relation")
            relation.units.remove(unit)
            self._update_peers_relation_data()

    def _on_start(self, event):
        self.unit.status = WaitingStatus("Waiting for peers relation")
        self.state.is_ready = True

    def _on_stop(self, event):
        self.state.is_ready = False

    def on_relation_broken(self, event):
        if event.relation.id == self.model.get_relation("peering").id:
            logger.info("Relatin broken, here is my config: " + self.state.configfile)
            raise ModelError("Peering relation broken")

    def on_peers_relation_joined(self, event: RelationJoinedEvent):
        relation = event.relation
        self.unit.status = MaintenanceStatus("Setting up peering relation")
        relation.data[self.unit].update({"charm": self.app.name})
        self._update_peers_relation_data()        

    def on_peers_relation_changed(self, event: RelationChangedEvent):
        self._update_peers_relation_data()

    def on_peers_relation_departed(self, event: RelationDepartedEvent):
        self._remove_unit_from_peers(event.unit)

    def on_peers_relation_broken(self, event: RelationBrokenEvent):
        self.unit.status = MaintenanceStatus("Peering relation broken")

        # Remove departing units from relation
        for unit in event.relation.units:
            if unit != self.unit:
                self._remove_unit_from_peers(unit)

    def generate_random_string(self,length=8):
        # Define the characters to choose from
        characters = string.ascii_letters + string.digits

        # Generate a random string of specified length
        random_string = ''.join(random.choice(characters) for _ in range(length))

        return random_string

if __name__ == "__main__":
    ops.main.main(PeerCharm)
