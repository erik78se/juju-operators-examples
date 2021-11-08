# storage

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
    juju model-config logging-config="<root>=WARNING;unit=TRACE"
    juju deploy ./<built_charm>
    juju debug-log

## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com