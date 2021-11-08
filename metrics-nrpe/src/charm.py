#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk


import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus
import subprocess as sp
import sys
import subprocess
import psutil

logger = logging.getLogger(__name__)

EMOJI_CORE_HOOK_EVENT = "\U0001F4CC"

class MetricsNrpeCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.collect_metrics, self._on_collect_metrics)

    def _on_collect_metrics(self, event):
        """
        Runs every: X minutes. Not sure how often really. Can the interval be changed?
        The collect-metrics hook is manually triggered with: juju collect-metrics <charmname> is seems.
        Removed metrics from metrics.yaml seems to go away automatically after some time. Not sure.

        Metrics are presented with:
        UNIT      	           TIMESTAMP	  METRIC	VALUE	LABELS
        mymetric/0	2021-11-04T20:43:16Z	  load_5	   99
        mymetric/0	2021-11-04T20:43:16Z	mem_used	   88

        LABELS is not known what it is yet.
        """
        load_5 = psutil.getloadavg()[1]
        mem_used = psutil.virtual_memory().percent

        #BUG: value overload - fixed in later version of ops. Convert to int to get a workaround.
        load_5 = int(load_5)
        mem_used = int(mem_used)

        logger.info(f"\U0001F4CC Memory % used: {mem_used}")
        logger.info(f"\U0001F4CC Load 5min: {load_5}")

        event.add_metrics({"mem_used": mem_used, "load_5": load_5})

if __name__ == "__main__":
    main(MetricsNrpeCharm)
