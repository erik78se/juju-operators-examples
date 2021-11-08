# corehooks-all

It implements all core hooks of Juju - a great start for a developer getting started with operator and juju.

Installs the service *hello* and the operator can set a custom message for the hello service.

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
    juju add-model examples
    juju model-config default-series=focal
    juju model-config logging-config="<root>=WARNING;unit=DEBUG"
    juju deploy ./<built_charm>
    juju debug-log

## Configs

Set a custom message for the juju service.

    juju config corehooks-all message="Say hello to Juju."

Set this config to make juju automatically restart the hello service if the message is changed.

    juju config corehooks-all restart_on_reconfig=True


## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com