#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.

import os
import socket
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus
import yaml
from jinja2 import Environment

class HaproyRelate(CharmBase):
    """
    Relate to haproxy
    """
    
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.install,
                               self._on_install)
        
        self.framework.observe(self.on.website_relation_changed,
                               self._on_website_changed)

    def _on_install(self,event):
        """ Install """
        
        self.unit.status = MaintenanceStatus("installing microsample snap")
        os.system('snap install microsample --edge')

        
    def _on_website_changed(self, event):
        """Handle website relations changed."""
        
        event.relation.data[self.model.unit]['hostname'] = socket.gethostname()
        event.relation.data[self.model.unit]['port'] = str(80)
        event.relation.data[self.model.unit]['services'] = self._render_services()

        # Set active status
        self.unit.status = ActiveStatus("Ready, relation data sent.")

    def _render_services(self):
        """
        Produce and return a service.yaml yaml string
        """
        
        YAML = """
- { service_name: microsample,
  service_host: 0.0.0.0,
  service_port: 8080,
  service_options: [mode http, balance leastconn, http-check expect rstring ^Online$],
  servers: [[microsample_unit_{{ unitid }}, {{ address }}, {{ port }}, check]]}
"""

        # Get address
        ip = str(self.model.get_binding("website").network.bind_address)

        r = Environment().from_string(YAML).render(address=ip,
                                                   port=8080,
                                                   unitid=self.model.unit.name.rsplit('/', 1)[1])

        try:
            return str(yaml.safe_load(r))
        except yaml.YAMLError as exc:
            print(exc)

        
if __name__ == "__main__":
    main(HaproyRelate)
