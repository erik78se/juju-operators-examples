#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.

import os
import logging
import json
import time
import socket

import ops


logger = logging.getLogger(__name__)

class GrafanaDashBoardCharm(ops.CharmBase):
    """
    A charm that deploys a grafana dashboard to grafana.
    
    juju deploy grafana
    juju deploy grafana-example-dashboard.charm
    juju relate grafana grafana-example-dashboard

    Inspiration from: https://opendev.org/openstack/charm-ceph-dashboard/src/branch/master/src/interface_grafana_dashboard.py

    """
    
    def __init__(self, *args):
        super().__init__(*args)

        
        self.framework.observe(self.on.install,
                                self._install)

        # The dashboard relation - provides the dashboard
        self.framework.observe(self.on.grafana_dashboard_relation_changed,
                                self._on_grafana_dashboard_relation_changed)

        # The prometheus scrape endpoint - provides some data for our dashboard via prometheus
        self.framework.observe(self.on.scrape_relation_changed, 
                                self._on_scrape_relation_changed)
        
    def _install(self, event):
        """
        Install prometheus-node-exporter so to provide some metrics.
        """
        logger.debug("Installing prometheus-node-exporter, test with curl -L localhost:9100/metrics")
        os.system('apt -y install prometheus-node-exporter')
        


    def _on_grafana_dashboard_relation_changed(self, event: ops.RelationChangedEvent) -> None:
        """Provide the dashboard to Grafana."""
        # Only one dashboard is needed so let the app leader deal with it
        if not self.unit.is_leader():
            return

        # Check if there is an existing relation named "prometheus-manual"
        scrape_relation = self.model.get_relation("scrape")
        if not scrape_relation:
            logger.error(
                "Missing scrape relation required by grafana-dashboard relation"
            )
            return

        if not scrape_relation.app.name:
            logger.error("Missing app.name for scrape relation")
            return

        # Load the dashboard which contains some labels we will replace with
        # reference to datasources we provide from the scrape relation.
        dashboard_file = "files/grafana-dashboards/dashboard-template.json"
        if not os.path.exists(dashboard_file):
            logger.error("No dashboard for grafana was bundled in the charm")
            return

        with open(dashboard_file) as f:
            data = f.read()
            dashboard = json.loads(data)

        # The bundled dashboard should contain:
        #   "__inputs": [
        #     {
        #       "name": "DS_INFRA",
        #       "label": "infra",
        #       "description": "",
        #       "type": "datasource",
        #       "pluginId": "prometheus",
        #       "pluginName": "Prometheus"
        #     }
        #   ],
        # and the name value needs to be replaced by the proper datasource name which
        # is derived from the application name used when Prometheus2 was deployed.
        ds_prometheus = f'"{scrape_relation.app.name} - Juju generated source"'

        # Safety checks
        if "__inputs" not in dashboard or len(dashboard["__inputs"]) != 1:
            logger.error(f'{dashboard_file} has invalid or missing "__inputs" section')
            return

        # Get the name of the datasource that will need to be replaced
        ds_to_replace = dashboard["__inputs"][0].get("name")
        if not ds_to_replace:
            logger.error(f"{dashboard_file} is malformed")
            return

        # Replace the datasource name
        #   "name": "DS_INFRA"   -> "name": "ds_prometheus"
        #   "uid": "${DS_INFRA}" -> "uid": "ds_prometheus"
        data = data.replace('"' + ds_to_replace + '"', ds_prometheus).replace(
            '"${' + ds_to_replace + '}"', ds_prometheus
        )

        # Reload the mangled data as JSON
        dashboard = json.loads(data)

        # XXX: Introduce an artificial delay before sending the dashboard to
        # Grafana to give time for the prometheus2:grafana-source relation
        # to be established. Without that, the injected dashboard shows
        # as empty requiring manual intervention:
        # # > remove the relation
        # juju remove-relation grafana-dashboard-example:grafana-dashboard grafana:dashboards
        # # > log to grafana using the admin password obtained with:
        # juju run-action --wait grafana/leader get-admin-password
        # # > delete the bogus dashboard
        # # > recreate the relation
        # juju add-relation grafana-dashboard-example:grafana-dashboard grafana:dashboards

        # TODO: Not sure why we need to do this.

        time.sleep(60)

        # Send a compact JSON version of the dashboard to Grafana
        event.relation.data[self.app].update(
            {
                "name": self.app.name.upper(),
                "dashboard": json.dumps(
                    dashboard,
                    separators=(",", ":"),
                ),
            }
        )
        logger.debug("Dashboard sent to Grafana")

    def _on_scrape_relation_changed(self, event: ops.RelationChangedEvent) -> None:
        """
        Provide basic node exporter metrics
        """
        _port = 9100
        _hostname = socket.getfqdn()
        _metrics_path = '/metrics'

        event.relation.data[self.model.unit]['hostname'] = str(_hostname)
        event.relation.data[self.model.unit]['port'] = str(_port)
        event.relation.data[self.model.unit]['metrics_path'] = str(_metrics_path)



if __name__ == "__main__":
    ops.main(GrafanaDashBoardCharm)
