# storage

This charm demonstrates how to work with a filesystem type disk.

## Description

A simple machine/vm charm implementing storage hooks.
 
    storage-attached
    storage-detaching

## Usage
    
    charmcraft build
    juju add-model hellomodel
    juju model-config logging-config="<root>=WARNING;unit=TRACE"
    juju deploy ./<built_charm>
    juju debug-log

## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com