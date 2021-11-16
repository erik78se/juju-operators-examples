# Juju ops examples
Example charms demonstrating and describing functionalities of Juju charms with the juju ops framework.

[Ops](https://ops.readthedocs.io/en/latest/) is a Python framework for developing charms. It uses standard Python structures to make charm development simple.

[Charmcraft](https://github.com/canonical/charmcraft) is a command line tool used alongside Ops to simplify the creation, building, and publication of a charm.

When testing the charms, see more logs with:

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

#### lxd-profile

This demonstrates the use of a *lxd-profile.yaml* to tweak lxd container settings. 
The example deploys privileged containers.

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