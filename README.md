# Juju operators examples
Example charms demonstrating and describing functionalities of Juju operators.

To see more logs from the charms, do:

    juju model-config logging-config="<root>=WARNING;unit=TRACE"

## The charms 

#### hello
Implements core juju hooks to deploy the **hello** package via apt. 
systemd is used with a /etc/default/hello config file to manage service startup parameters.

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
Please contribute by trying them out and give feedback and code!