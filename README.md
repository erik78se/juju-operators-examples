# Juju ops examples
Example charms demonstrating and describing functionalities of Juju charms with the juju ops framework.

To see more logs from the charms, do:

    juju model-config logging-config="<root>=WARNING;unit=DEBUG"

## The charms 

#### corehooks-all
Implements core juju hooks to deploy the **hello** package via apt. 
systemd is used with a /etc/default/hello config file to manage service startup parameters.

#### deploy-minimal
Implements the core hooks relevant to a deploy of a charm: *install*, *config-changed*, *start*

#### deploy-with-storage
Implements the core hooks relevant to a deploy of a charm: *install*, *config-changed*, *start* 
including the storage hooks: *xxx_storage_attached* and *xxx_storage_detaching*

#### metrics-base
This charm demonstrates use of metrics in juju charms.
It loads some metrics on cpu and memory.

#### mertrics-nrpe
This charm demonstrates clever use of metrics together with nagios nrpe.
It loads metrics on cpu, memory & provides them on the nagios-external-nrpe interface.

#### storage-filesystem
Uses a separate disk (type: filesystem) for storing log files. 
Useful for charms which needs to have permanent or re-usable data on separate disk.


## Contribute
Please contribute by creating own examples, trying existing ones out, document, give feedback and support!