#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.

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

    """
    
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.hello_dashboard_relation_joined,
                               self._send_dashboard)

    def _send_dashboard(self, event):
        """
        Loads json from file, converts it to string and places it on the relation.
        
        """
        dashboard_file = Path('files/grafana-dashboards/hello-world.json')

        f = open(dashboard_file)

        data = json.load(f)

        f.close()

        logger.debug("Sending dashboard: " + json.dumps(data, indent=4))

        event.relation.data[self.model.unit]['dashboard'] = json.dumps(data)

        event.relation.data[self.model.unit]['name'] = self.model.name

        self.unit.status = ActiveStatus("Dashboard sent.")
    
if __name__ == "__main__":
    main(GrafanaDashBoardCharm)
