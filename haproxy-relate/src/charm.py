#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.

import os
import logging
import socket
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus
import yaml
from jinja2 import Environment

logger = logging.getLogger(__name__)

class HaproyRelate(CharmBase):
    """
    Relate to haproxy, using service directive as:

    * mode http - This will pass HTTP requests to the servers listed
    
    * balance roundrobin - Use the roundrobin strategy for distributing load amongst the servers
    
    * option forwardfor - Adds the X-Forwarded-For header so our applications can get the clients actually IP address. Without this, our application would instead see every incoming request as coming from the load balancer's IP address
    
    * http-request set-header X-Forwarded-Port %[dst_port] - We manually add the X-Forwarded-Port header so that our applications knows what port to use when redirecting/generating URLs.

    Note that we use the dst_port "destination port" variable, which is the destination port of the client HTTP request. 

    * option httpchk HEAD / HTTP/1.1\r\nHost:localhost - Set the health check HAProxy uses to test if the web servers are still responding. If these fail to respond without error, the server is removed from HAProxy as one to load balance between. This sends a HEAD request with the HTTP/1.1 and Host header set, which might be needed if your web server uses virtualhosts to detect which site to send traffic to 

   * http-request add-header X-Forwarded-Proto https if { ssl_fc } - We add the X-Forwarded-Proto header and set it to "https" if the "https" scheme is used over "http" (via ssl_fc). Similar to the forwarded-port header, this can help our web applications determine which scheme to use when building URL's and sending redirects (Location headers).
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
        service_port => The haproxy listen port (E.g. 443 for standard ssl)
        """
        
        YAML = """
- service_name: microsample
  service_host: 0.0.0.0
  service_port: 443
  crts: [DEFAULT]
  service_options:
      - balance leastconn
      - option forwardfor
      - http-request set-header X-Forwarded-Port %[dst_port]
      - http-request add-header X-Forwarded-Proto https if { ssl_fc }
      - http-check expect rstring ^Online$
      - acl url_discovery path /.well-known/caldav /.well-known/carddav
      - http-request redirect location /remote.php/dav/ code 301 if url_discovery
  servers: [[nextcloud_unit_{{ unitid }}, {{ address }}, {{ port }}, 'cookie S{i} check']]
"""

        # Get address
        ip = str(self.model.get_binding("website").network.bind_address)

        r = Environment().from_string(YAML).render(address=ip,
                                                   port=8080,
                                                   unitid=self.model.unit.name.rsplit('/', 1)[1])
        
        try:
            return str(yaml.safe_load(r))
        except yaml.YAMLError as exc:
            logger.error("Error in service yaml: " + str(r))
            print(exc)

        
if __name__ == "__main__":
    main(HaproyRelate)
