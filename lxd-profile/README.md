# lxd-profile

This demonstrates the use of a *[lxd-profile.yaml](lxd-profile.yaml)* to tweak lxd container settings. 
The example deploys privileged containers.

There are some example yaml files below you can use for you own needs.

Read more in the [Juju official docs]

## Limitations & behaviour
* You can only have one lxd-profile per charm.
* The lxd profile is upgraded during the upgrade of the charm (juju upgrade-charm).
* Profiles are displayed at the machine level by using either the ```juju show-machine``` command 
or the ```juju status --format=yaml``` command.
* There is a hierarchy of profiles. LXD has its own default profile, then the model default profile (juju-<model-name>), and then a charm profile.
Interestingly, you can insert a model profile juju-<model-name> before you add the model, and juju won’t try and override it.
* You can't use "--constraints" to control the behaviour of lxd profiles.
* Profiles are applied in the order they are specified so the last profile to specify a specific key wins.

## Juju LXD information
Juju uses the default "juju-default" profile for container defaults.

    lxc profile show juju-default

You can edit a profile, for example changing the default storage zfs pool:

    lxc profile device set juju-default root pool=lxd-zfs

You can change the lxd profile for a model, lets say mymodel:

     cat lxd-profile.yaml | lxc profile edit juju-mymodel

## Example lxd-profile.yaml files
Note that these profiles are not well tested. Help needed!

### Privileged container profile
    config:
      security.nesting: true
      security.privileged: true

### Allow mounting of a remote NFS export profile 
    raw.lxc: |
          lxc.apparmor.profile=unconfined
          lxc.mount.auto=sys:rw
      security.nesting: true
      security.privileged: true

### Add a GPU profile

    config:
      devices:
        mygpu:
          type: gpu

### A [Kubernetes worker] profile
    config:
      linux.kernel_modules: ip_tables,ip6_tables,netlink_diag,nf_nat,overlay
      raw.lxc: |
        lxc.apparmor.profile=unconfined
        lxc.mount.auto=proc:rw sys:rw
        lxc.cgroup.devices.allow=a
        lxc.cap.drop=
      security.nesting: true
      security.privileged: true
    description: "Kubernetes worker profile"
    devices:
      aadisable:
        path: /dev/kmsg
        source: /dev/kmsg
        type: unix-char

### X11 GUI app profile
    config:
      environment.DISPLAY: :0
      raw.idmap: both 1000 1000
      user.user-data: |
        #cloud-config
        runcmd:
          - 'sed -i "s/; enable-shm = yes/enable-shm = no/g" /etc/pulse/client.conf'
          - 'echo export PULSE_SERVER=unix:/tmp/.pulse-native | tee --append /home/ubuntu/.profile'
        packages:
          - x11-apps
          - mesa-utils
          - pulseaudio
    description: GUI LXD profile
    devices:
      PASocket:
        path: /tmp/.pulse-native
        source: /run/user/1000/pulse/native
        type: disk
      X0:
        path: /tmp/.X11-unix/X0
        source: /tmp/.X11-unix/X0
        type: disk
      mygpu:
        type: gpu

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


[Juju official docs]: https://juju.is/docs/olm/use-lxd-profiles
[Kubernetes worker]: https://github.com/charmed-kubernetes/charm-kubernetes-worker/blob/master/lxd-profile.yaml