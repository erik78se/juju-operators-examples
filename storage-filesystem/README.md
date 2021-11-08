# storage-filesystem

This charm demonstrates how to work with juju storage filesystem type disk as defined in metadata.yaml.


    storage:
      data:
        type: filesystem
        description: Storage device for logs.
        minimum-size: 100M
        location: /logs

## Description

The charm installs a systemd mount unit file when juju has made the filesystem available.
 
    storage-attached
    storage-detaching

## Usage
    
    charmcraft build
    juju add-model examples
    juju model-config default-series=focal
    juju model-config logging-config="<root>=WARNING;unit=DEBUG"
    juju deploy ./<built_charm>
    juju debug-log

    # This example adds a storage and then we move it between units.

    # add storage to the first unit
    juju add-storage storage-filesystem/0 logdata=ebs,1,200M

    # list storage
    juju storage

    # remove the disk from the unit
    juju detach-storage logdata/0

    # add a second unit
    juju add-unit storage-filesystem

    # re-attach the old disk (logdata/0) to
    juju attach-storage storage-filesystem/1 logdata/0


## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com