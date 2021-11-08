# storage

Charm that implements the storage hooks of Juju.

    juju model-config logging-config="<root>=WARNING;unit=TRACE"

## Description

A simple machine/vm charm implementing storage hooks.
 
    storage-attached
    storage-detaching

## Usage
    
    charmcraft build
    juju deploy ./storage.charm


## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com