# Getting started (vm-charms)

Lets get started with charming vm charms on lxd.

### What you’ll need:

- Familiarity with the Juju OLM 1
- Some Python programming language, Object-Oriented Programming, Event Handlers
- Some basic LXD skill.

### What you’ll learn:

- Set up your development environment (See: https://discourse.charmhub.io/t/set-up-your-development-environment/7379)
- Initialize a vm charm
- Deploy it to a vm cloud.

## Setup your local lxd cloud
First, make sure your iptables isn't going to mess up from docker fucking up your firewall.

    iptables -P FORWARD ACCEPT; iptables -F FORWARD
    
Launch up a VM with 15GB disk on a Ubuntu 22.04. You can use other virtual machine managers (multipass, libvirt etc.) but I use lxd.

    lxc launch ubuntu:jammy juj -d root,size=15GiB --vm

Setup the machine for the tutorial
    
    lxc shell juj
    root@juj:~# sudo echo Acquire::ForceIPv4 "true"; > /etc/apt/apt.conf.d/99force-ipv4
    root@juj:~# sudo snap install juju --classic
    root@juj:~# sudo snap install charmcraft --classic
    root@juj:~# lxd init --auto
    root@juj:~# lxc remote list
    root@juj:~# juju bootstrap localhost tutorial-controller
    Creating Juju controller "tutorial-controller" on localhost/localhost
    Looking for packaged Juju agent version 2.9.38 for amd64
    Located Juju agent version 2.9.38-ubuntu-amd64 at https://streams.canonical.com/juju/tools/agent/2.9.38/juju-2.9.38-linux-amd64.tgz
    To configure your system to better support LXD containers, please see: https://linuxcontainers.org/lxd/docs/master/explanation/performance_tuning/
    Launching controller instance(s) on localhost/localhost...
     - juju-3a5da3-0 (arch=amd64)                 
    Installing Juju agent on bootstrap instance
    Fetching Juju Dashboard 0.8.1
    Waiting for address
    Attempting to connect to fd42:e802:396b:494a:216:3eff:fe4b:8fc7:22
    Attempting to connect to 10.77.114.74:22
    Connected to fd42:e802:396b:494a:216:3eff:fe4b:8fc7
    Running machine configuration script...
    Bootstrap agent now started
    Contacting Juju controller at 10.77.114.74 to verify accessibility...
    Bootstrap complete, controller "tutorial-controller" is now available
    Controller machines are in the "controller" model
    Initial model "default" added

    root@juj:~# juju status
    Model    Controller           Cloud/Region         Version  SLA          Timestamp
    default  tutorial-controller  localhost/localhost  2.9.38   unsupported  15:26:30Z

    Model "admin/default" is empty.

# Build a charm
Now when we have a juju controller atteched to a local cloud, lets get the charm initialized with charmcraft.

## Initialize the charm
An empty directory with the name of our charm.

    root@juj:~# mkdir mycharm
    root@juj:~# cd mycharm
    root@juj:~/mycharm# charmcraft init --machine # can be simple, machine or kubernetes

## Edit the metadata.yaml and add the name to the charm.

    vi metadata.yaml

Now, compile/pack the charm with charmcraft.

    root@juj:~/mycharm# charmcraft pack # This takes a long time the first time (3-5 minutes) since it builds inside a full container.
    Packing the charm                                                                                                                                                                    
    Created 'mycharm_ubuntu-22.04amd64.charm'.                                                                                                                                          
    Charms packed:                                                                                                                                                                       
       mycharm_ubuntu-22.04-amd64.charm   

The charm is ready to be deployed. Later on, you would be able to upload it to charmhub, but thats another tutorial.

## Deploy your charm on you local LXD cloud

    juju deploy ./mycharm_ubuntu-22.04-amd64.charm 

## Next steps

        Add charm relations and interfaces
          - Example: https://github.com/erik78se/juju-operators-examples/tree/main/haproxy-relate
        Connect external charm libraries and interact with them:
          - Example: Missing
        Add charm actions: 
          - Example: https://github.com/erik78se/juju-operators-examples/tree/main/action-charm
        Add charm configurations: 
          - Example: Missing
        Write tests
          - Example: Missing

## What happens with a charm after deploy?
This explains what happens to a charm once you deploy it and how you can implement advanced features for your charm, depending on your ambitions and needs for your charm and software. https://discourse.charmhub.io/t/a-charms-life/5938

## More advanced topics
https://discourse.charmhub.io/t/talking-to-a-workload-control-flow-from-a-to-z/6161

## Examples

https://github.com/erik78se/juju-operators-example
