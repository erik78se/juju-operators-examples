# use-lib-charm

This charm shows the use of a [juju libraries] in a charm. 

## About juju libraries
Libraries are used to encapsulate functionality just like normal python modules. You can fetch them with charmcraft, include them in your charms, create and publish your own just as with charms.

## About this charm
In this example, we'll install **[apt-cacher-ng]** which is a local cache service for apt packages.

You can have your models use it as apt-http-proxy after you deployed it by setting a model config like this (replace the IP with that of your unit):

```
juju model-config juju-http-proxy=http://10.51.45.208:3142
```

This is picked up imediately by all units in the model when the config is set and saves both time and bandwidth for your future installations.

## How to use a lib in a charm

* Libs can be found on charmhub.io as "normal charms".

Libs are downloaded with **charmcraft fetch-lib**.

This charm uses the systemd and apt modules from the [operator-libs-linux] to start a service. There are other libs that can be used and you can create your own to encapsulate funtionality that is used often.

```
mkdir use-lib-charm
cd use-lib-charm
charmcraft init --profile machine
charmcraft fetch-lib charms.operator_libs_linux.v0.apt
charmcraft fetch-lib charms.operator_libs_linux.v1.systemd
```

This downloads the files *lib/charms/operator_libs_linux/v1/systemd.py* and *lib/charms/operator_libs_linux/v0/apt.py* to your charm code tree.


## Attributions
* Jon Seager - who wrote the juju libraries used here.
* Joseph Phillips for the inspiration to use the apt-cacher-ng
* The [apt-cacher-ng] team for that software
* Canonical for the Juju framework

[operator-libs-linux]: https://charmhub.io/operator-libs-linux/libraries/systemd
[apt-cacher-ng]: https://www.unix-ag.uni-kl.de/~bloch/acng/
[juju libraries]: https://juju.is/docs/sdk/library