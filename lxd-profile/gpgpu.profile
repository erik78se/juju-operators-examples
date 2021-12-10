config:
  boot.autostart: "true"
  security.nesting: "true"
  nvidia.driver.capabilities: all
  nvidia.runtime: "true"
  user.user-data: |
    #cloud-config
    package_upgrade: true
    packages:
        - mesa-utils
        - build-essential
        - nvidia-cuda-toolkit-gcc
        - vim
description: GPGPU profile
devices:
  mygpu:
    type: gpu
  eth0:
    name: eth0
    network: lxdfan0
    type: nic
  root:
    path: /
    pool: local
    type: disk
name: gpgpu
used_by: []
