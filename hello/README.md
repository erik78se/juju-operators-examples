# hello

A hello world kind of juju charm.

It implements all core hooks of Juju allowing a charmer to get started with operator and juju.

The charm installs the service *hello* and the operator can set a custom message for the hello service.

The core hooks implemented are:

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