# Juju operators examples
Example charms demonstrating and describing functionalities of Juju operators.

Remember to do to be able to see more logs from the charms:

    juju model-config logging-config="<root>=WARNING;unit=TRACE"

Work in progress here...

* The hello charm
  * A charm that implements all core juju hooks to deploy the hello package as a service.
* The metrics charm
  * A charm that implements some metrics.
* The storage charm
  * A charm uses a separate disk for storing log files. This shows how you can develop charms which needs to have permanent data on separate disk.
* .... more

Please contribute by trying them out and give feedback and code!