# Juju operators examples
Example charms demonstrating and describing functionalities of Juju operators.

To see more logs from the charms, do:

    juju model-config logging-config="<root>=WARNING;unit=TRACE"

## The charms 

### Basic concepts
#### hello
Implements core juju hooks to deploy the **hello** package via apt. 
systemd is used with a /etc/default/hello config file to manage service startup parameters.

#### metrics-base
Implements some metrics.

#### mertrics-nrpe
Implements a custom metric and provides it via nrpe-external-master interface. 
This allows you to then relate to nagios to monitor your service.

#### storage-filesystem
Uses a separate disk (type: filesystem) for storing log files. 
Useful for charms which needs to have permanent or re-usable data on separate disk.



## Contribute
Please contribute by trying them out and give feedback and code!