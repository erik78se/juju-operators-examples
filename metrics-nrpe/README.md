# metrics
A simple charm showing metrics use.

## Description

Collects some metrics and expose the same via the nrpe-external-master interface.

## Usage

    charmcraft build
    juju add-model examples
    juju model-config logging-config="<root>=WARNING;unit=TRACE"
    juju deploy ./<built_charm>
    juju deploy nagios
    juju relate nagios metrics-nrpe

## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com