# hello

A juju charm that implements all core hooks of Juju.


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

The charm installs the service *hello* and allows the operator to set a custom message.

## Usage
    
    charmcraft build
    juju add-model hellomodel
    juju model-config logging-config="<root>=WARNING;unit=TRACE"
    juju deploy ./<built_charm>

## Configs

Set a custom message for the juju service.

    juju config hello message="Say hello to Juju."

Set this config to make juju automatically restart the hello service if the message is changed.

    juju config hello restart_on_reconfig=True


## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com