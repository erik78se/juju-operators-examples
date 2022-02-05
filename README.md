# Ops examples
This repo collects example charms built with the juju ops framework. Contributions with your examples is much appreciated!

[Ops](https://ops.readthedocs.io/en/latest/) is a Python framework for developing charms. It uses standard Python structures to make charm development simple.

[Charmcraft](https://github.com/canonical/charmcraft) is a command line tool used alongside Ops to simplify the creation, building, and publication of a charm.

When testing the charms, see more logs with:

    juju model-config logging-config="<root>=WARNING;unit=DEBUG"

## Charms 

#### [corehooks-all](corehooks-all)
Implements core juju hooks to deploy the **hello** package via apt. 
systemd is used with a /etc/default/hello config file to manage service startup parameters.

#### [deploy-minimal](deploy-minimal)
Implements the core hooks relevant to a deploy of a charm: *install*, *config-changed*, *start*

#### [deploy-with-storage](deploy-with-storage)
Implements the core hooks relevant to a deploy of a charm: *install*, *config-changed*, *start* 
including the storage hooks: *xxx_storage_attached* and *xxx_storage_detaching*

#### [lxd-profile](lxd-profile)

This demonstrates the use of a *lxd-profile.yaml* to tweak lxd container settings. 
The example deploys privileged containers.

#### [metrics-base](metrics-base)
This charm demonstrates use of metrics in juju charms.
It loads some metrics on cpu and memory.

#### [monitoring-nrpe](monitoring-nrpe)
This charm demonstrates use nagios nrpe (and charmhelpers).
It uses the the local-monitoris interface.

#### [storage-filesystem](storage-filesystem)
Uses a separate disk (type: filesystem) for storing log files. 
Useful for charms which needs to have permanent or re-usable data on separate disk.

#### [haproxy-relate](haproxy-relate)
Example on how to form a relation to haproxy, passing information on how to have haproxy
be automatically configured.


## Contribute
Please contribute by creating own examples, trying existing ones out, document, give feedback and support!