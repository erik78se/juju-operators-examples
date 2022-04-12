# grafana-dashboard-example

This juju charm implements the [grafana-dashboard interface] to send over a custom dashboard to grafana using the [prometheus2 charm] to connect it with a datasource.


## Usage

    charmcraft build
    juju add-model examples
    juju model-config default-series=focal
    juju model-config logging-config="<root>=WARNING;unit=TRACE"

    # Deploy grafana
    juju deploy grafana
    
    # Deploy prometheus2 as prometheus since this seems to help.
    juju deploy prometheus2 prometheus

    # Deploy our charm
    juju deploy ./grafana-dashboard-example_ubuntu-20.04-amd64.charm

    # Connect with prometheus and grafana
    juju relate grafana-dashboard-example:scrape prometheus
    juju relate grafana-dashboard-example:grafana-dashboard grafana

    # Visit grafana http://grafana:3000
    # Get admin password:
    juju run-action grafana/0 get-login-info --wait

## General implementation details

We provide two relations in [metadata.yaml]():

    provides:
      grafana-dashboard:
        interface: grafana-dashboard
      scrape:
        interface: prometheus

We implement those in [src/charm.py]()

In the install event, prometheus-node-exporter is installed that collects and provides metrics. This is related with prometheus which create a datasource for us.

### The dashboard-template.json should contain:
```
   "__inputs": [
     {
       "name": "DS_INFRA",
       "label": "infra",
       "description": "",
       "type": "datasource",
       "pluginId": "prometheus",
       "pluginName": "Prometheus"
     }
   ], 
```
The placeholders (DS_INFRA) is replaced in the code, with the datasource name which we modify before  ending them over to grafana with the relation data.

## Your own dashboard

If you intend to roll your own dashboard to send to grafana, you need to properly export it using "share for export externally" which brings along a usable json. You still need to edit it to fit your scenario.

![Alt text](share-export-dashboard.png?raw=true "Exporting a dashboard")

## Authors
Erik Lönroth, support me by attributing my work and pay me.
https://eriklonroth.com


## Attibutions

OpenStack charmers team for code: https://https://opendev.org/openstack/charm-ceph-dashboard/

LMA charmers team for prometheus2 charm: https://git.launchpad.net/charm-prometheus2

Juju team for the grafana-dashboard interface: https://github.com/juju-solutions/interface-grafana-dashboard

LXD charm developers for a massive example: https://github.com/canonical/charm-lxd/


[prometheus2 charm]: https://git.launchpad.net/charm-prometheus2
[grafana-dashboard interface]: https://github.com/juju-solutions/interface-grafana-dashboard
