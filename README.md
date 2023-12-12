# Ops examples
This repo collects example charms built with the juju ops framework. Contributions with your examples is much appreciated!

[Ops](https://ops.readthedocs.io/en/latest/) is a Python framework for developing charms. It uses standard Python structures to make charm development simple.

[Charmcraft](https://github.com/canonical/charmcraft) is a command line tool used alongside Ops to simplify the creation, building, and publication of a charm.

When testing the charms, see more logs with:

    juju model-config logging-config="<root>=WARNING;unit=DEBUG"

## Reference charms  in this repo

Below you find a set of charms to assist in creating your own charms covering a number of useful use-cases.

#### [deploy-minimal](deploy-minimal)
Implements the core hooks in the setup phase of a charm: *install*, *config-changed*, *start*. This is a great starting point for charming up a new software before adding in more features.

#### [corehooks-all](corehooks-all)
This charm implements all core juju hooks to deploy the **hello** package via apt. 
systemd is used with a /etc/default/hello config file to manage service startup parameters. A good reference charm which also  covers a systemd tactic you might use.

#### [deploy-with-storage](deploy-with-storage)
This charm shows a reference implementation for the juju storage hooks: *xxx_storage_attached* and *xxx_storage_detaching*

#### [storage-filesystem](storage-filesystem)
Uses a separate disk (type: filesystem) for storing log files. 
Useful for charms which needs to have permanent or re-usable data on separate disk.

#### [lxd-profile](lxd-profile)
This charm demonstrates how you can ship a *lxd-profile.yaml* to tweak lxd container settings. 
The example deploys privileged containers. It is also specific to LXD clouds/containers.

#### [metrics-base](metrics-base)
This charm demonstrates use of metrics in juju charms.
It loads some metrics on cpu and memory.

#### [monitoring-nrpe](monitoring-nrpe)
This charm demonstrates use nagios nrpe (and charmhelpers) for monitoring a service.
It uses the the local-monitors interface.

#### [haproxy-relate](haproxy-relate)
This charm can form an relation/integration to haproxy to automatically configure it as a reverse proxy. Very useful for deploying custom web-services.

#### [grafana-dashboard-example](grafana-dashboard-example)
This charm shows how to pass a custom grafana dashboard over a integration to monitor prometheus metrics. If you look to monitor your application with a full [Canonical Observability Stack (COS)](https://charmhub.io/cos-lite), you should study the much more mature [observed](observed).

#### [action-charm](action-charm)
This charm implements a hello-world action.

#### [observed](observed)
This charm shows how to integrate with the [grafana-agent](https://charmhub.io/grafana-agent) subordinate-charm and how to add advanced observability/monitoring to your own charms and integrate with the [Canonical Observability Stack (COS)](https://charmhub.io/cos-lite).

#### [use-lib-charm](use-lib-charm)
This charm demonstrate how to include a juju library in your charms.


## Contribute
Please contribute by creating own examples, trying existing ones out, document, give feedback and support!
