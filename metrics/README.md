# mymetrics
A simple charm showing metrics use.

## Description

Metrics charm.

## Key elements
### metrics.yaml
Defines the metrics.

### charm.py

    self.framework.observe(self.on.collect_metrics, self.on_collect_metrics)

## Usage

Shows simple metrics code.

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines
on enhancements to this charm following best practice guidelines, and
`CONTRIBUTING.md` for developer guidance.

## Authors
Erik Lönroth, support me by attributing my work
https://eriklonroth.com