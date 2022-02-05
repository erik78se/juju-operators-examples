# haproxy-relate

This charm shows how to relate with the haproxy charm.

It passes ther "services" key over the relation, containing
the yaml needed to set some custom config for haproxy.

## Usage

    charmcraft build
    juju add-model examples
    juju model-config default-series=focal
    juju model-config logging-config="<root>=WARNING;unit=TRACE"

    juju deploy ./haproxy-relate.charm
    juju deploy ./haproxy.charm
    juju relate haproxy haproxy-relate

## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com
