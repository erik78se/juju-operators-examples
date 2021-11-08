# metrics
A simple charm showing metrics use.

## Description

The shows how to make a charm collect metrics by adding the **metrics.yaml** file to a charm and implementing the juju core hook:

    collect-metrics

## Usage

    charmcraft build
    juju add-model examples
    juju model-config default-series=focal
    juju model-config logging-config="<root>=WARNING;unit=DEBUG"
    juju deploy ./<built_charm>
    juju debug-log
    juju collect-metrics metrics

## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com