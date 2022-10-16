#!/usr/bin/env python3
# Copyright 2022 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""

The Action Charm

"""

from cmath import e
import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus, WaitingStatus

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

class ActionCharmCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.hello_action, self._hello_action)

    def _hello_action(self, event):
        """
        Sets a message in the event log (stdout)
        """
        try:
            #custom
            event.set_results({"the-message": "Hello world"})
            
            #stdout
            event.log(event.params['message'])  
        except Exception as e:
            #stderr
            event.fail(message=e)

if __name__ == "__main__":  # pragma: nocover
    main(ActionCharmCharm)
