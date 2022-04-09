# monitoring-nrpe
A simple charm that shows how to implement some monitoring with charmhelpers and nrpe to use with nagios.

Uses charmhelpers lib to work out the nrpe bits. See: https://github.com/juju/charm-helpers

## Usage

    charmcraft build
    juju add-model examples
    juju model-config default-series=focal
    juju model-config logging-config="<root>=WARNING;unit=TRACE"

    juju deploy grafana
    juju deploy ./grafana-dashboard-example.charm
    juju relate grafana grafana-dashboard-example

    # Visit nagios http://grafana:3000
    # Get admin password:
    juju run-action grafana/0 get-admin-password --wait

## General implementation details
1. Update metadata.yaml

       provides:
         hello-dashboard:
         interface: grafana-dashboard
         scope: container

3. Add custom dashboards to 

       files/grafana-dashboards/foobar.json

4. Implement the code to send the dashboard:

5. Update charmcraft.yaml to pass along the files

       parts:
        charm:
        charm-python-packages: [setuptools < 58]
        prime:
          - files/*

6. Add to requirements.txt

       ops >= 1.4.0
       charmhelpers==0.20.24

## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com
