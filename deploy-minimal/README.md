# deploy-minimal
Minimal charm implementing only the deploy hooks.

## Usage
    
    charmcraft build
    juju add-model examples
    juju model-config default-series=focal
    juju model-config logging-config="<root>=WARNING;unit=DEBUG"
    juju deploy ./<built_charm>
    juju debug-log

## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com