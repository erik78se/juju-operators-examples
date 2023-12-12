#!/usr/bin/env python3
# Copyright 2023 erik
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

import ops
import charms.operator_libs_linux.v0.apt as apt
import charms.operator_libs_linux.v1.systemd as systemd
from charms.operator_libs_linux.v0.apt import PackageNotFoundError, PackageError
import sys

logger = logging.getLogger(__name__)


class UseLibCharmCharm(ops.CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.update_status, self._on_update_status)


    def _on_install(self, event: ops.InstallEvent):
        """Handle install event."""
        try:
            apt.update()
            apt.add_package("apt-cacher-ng")
        except PackageNotFoundError:
            logger.error("a specified package not found in package cache or on system")
            sys.exit(1)
        except PackageError as e:
            logger.error("could not install package. Reason: %s", e.message)
            sys.exit(1)


    def _on_start(self, event: ops.StartEvent):
        """Start the service."""
        if not systemd.service_running("apt-cacher-ng"):
            success = systemd.service_start("apt-cacher-ng")
            if not success:
                logger.error("Failed to start apt-cacher-ng service")
                self.unit.status = ops.BlockedStatus("apt-cacher-ng service failed to start")
                return
        self.unit.status = ops.ActiveStatus("Running.")


    def _on_update_status(self, event: ops.UpdateStatusEvent):
        """Handle update-status event. Sets the workload version."""
        try:
            apt_cacher_ng = apt.DebianPackage.from_installed_package("apt-cacher-ng")
            logger.info("apt-cacher-ng version: %s", apt_cacher_ng.fullversion)
            self.unit.set_workload_version(f"{apt_cacher_ng.fullversion}")
        except PackageNotFoundError:
            logger.error("apt-cacher-ng package not found on system")
            self.unit.set_workload_version("N/A")
        


if __name__ == "__main__":  # pragma: nocover
    ops.main(UseLibCharmCharm)  # type: ignore
