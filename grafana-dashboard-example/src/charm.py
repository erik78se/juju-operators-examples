#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.

import copy
import os
import logging
import json
from pathlib import Path
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus


logger = logging.getLogger(__name__)

class GrafanaDashBoardCharm(CharmBase):
    """
    A charm that deploys a grafana dashboard to grafana.
    
    juju deploy grafana
    juju deploy grafana-example-dashboard.charm
    juju relate grafana grafana-example-dashboard

    Inspiration from: https://opendev.org/openstack/charm-ceph-dashboard/src/branch/master/src/interface_grafana_dashboard.py

    """
    
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.hello_dashboard_relation_joined,
                               self._send_dashboard)

        # self.framework.observe(self.on.hello_dashboard_relation_changed,
        #                       self._send_dashboard)

    def _send_dashboard(self, event):
        """
        Loads json from file, converts it to string and places it on the relation.
        
        """
        dashboard_file = Path('files/grafana-dashboards/hello-world.json')

        # Load up json
        f = open(dashboard_file)
        _dashboard = json.load(f)
        f.close()

        # We add in a source_model key,value
        _dashboard["source_model"] = self.model.name

        logger.debug("Sending dashboard: " + json.dumps(_dashboard, indent=4, sort_keys=True))

        # Set data on the event relation.
        # event.relation.data[self.model.unit]['dashboard'] = json.loads(dashboard_file.read_text())
        event.relation.data[self.model.unit]['dashboard'] = json.dumps(_dashboard)
        event.relation.data[self.model.unit]['name'] = "myName1"

        # Done
        self.unit.status = ActiveStatus("Dashboard sent.")
    

if __name__ == "__main__":
    main(GrafanaDashBoardCharm)
