import json
import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)

pf = Path('files/grafana-dashboards/hello-world.json')

dashboard_file = open(pf)

logger.debug("Sending dashboard: " + str(dashboard_file))

data = json.load(dashboard_file)

print(json.dumps(data))
