# core

Charm that implements all core hooks of Juju.

    juju model-config logging-config="<root>=WARNING;unit=TRACE"

## Description

A simple machine/vm charm implementing all of the core hooks.

    install
    config-changed
    start
    upgrade-charm
    stop
    remove
    leader-elected
    leader-settings-changed
    update-status
    collect-metrics
    
It does not implement relation, storage, series, pebble or actions hooks.

## Usage
    
    charmcraft build
    juju deploy ./mysimple


## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com