#!/usr/bin/env python3

import yaml

YAML = """                                                                                              
- { service_name: microsample,                                                                                 
  service_host: 0.0.0.0,                                                                                       
  service_port: 8080,                                                                                          
  service_options: [mode http, balance leastconn, http-check expect rstring ^Online$],                           servers: [[microsample_unit_unitid, address, port , check]]}
"""

try:
    print(yaml.safe_load(YAML))
except yaml.YAMLError as exc:
    print(exc)


import socket
h = socket.gethostname()

print(h)


n = "foo/0"

print(n.rsplit('/', 1)[1])
