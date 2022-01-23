# metrics-nrpe
A simple charm showing metrics and nrpe-external-master

Uses charmhelpers lib to work out the nrpe bits. See: https://github.com/juju/charm-helpers

## Description

Collects some metrics and exposes a dummy nagios check nrpe-external-master interface.

## Usage

    charmcraft build
    juju add-model examples
    juju model-config default-series=focal
    juju model-config logging-config="<root>=WARNING;unit=TRACE"

    juju deploy nagios
    juju deploy ubuntu
    juju deploy nrpe
    juju deploy ./metrics-nrpe.charm
    juju relate nagios:monitors nrpe:monitors
    juju relate metrics-nrpe:nrpe-external-master nrpe:nrpe-external-master

    # Visit nagios http://nagios
    # Get nagiosadmin password:
    juju ssh nagios/0 sudo cat /var/lib/juju/nagios.passwd

## General implementation details
1. Update metadata.yaml

   provides:
     nrpe-external-master:
       interface: nrpe-external-master
       scope: container


2. Add the following to config.yaml

    nagios_context:
      default: "juju"
      type: string
      description: |
        Used by the nrpe subordinate charms.
        A string that will be prepended to instance name to set the host name
        in nagios. So for instance the hostname would be something like:
            juju-myservice-0
        If you're running multiple environments with the same services in them
        this allows you to differentiate between them.
    nagios_servicegroups:
      default: ""
      type: string
      description: |
        A comma-separated list of nagios servicegroups.
        If left empty, the nagios_context will be used as the servicegroup

3. Add custom checks (Nagios plugins) to files/nrpe-external-master

    files/nrpe-external-master/check_mycheck.sh

4. Implement the events in charm.py with something like in this charm

    def render_checks(self):
        """Render nrpe checks."""
        nrpe = NRPE()
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)

        # register basic test
        
        nrpe.add_check(
            shortname="hellocheck",
            description="Dummy hello check",
            check_cmd="check_hello.sh",
        )
        nrpe.write()

5. Update charmcraft.yaml to include the checks/files. Also, make sure setuptools are lower version.

    parts:
      charm:
      charm-python-packages: [setuptools < 58]
      prime:
        - files/*

6. Add to requirements.txt
    charmhelpers


## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com