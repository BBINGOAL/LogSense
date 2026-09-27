import unittest

from backend.app.api.main import app, list_incidents


class TestDashboardApi(unittest.TestCase):
    def test_lists_dashboard_incident_records(self):
        records = list_incidents()
        self.assertEqual(len(records), 2)
        self.assertEqual(
            records[0].incident.incident_id,
            "auth-20260927T100000Z",
        )
        self.assertEqual(len(records[0].metric_windows), 3)
        self.assertEqual(
            records[0].analysis.metadata.evidence_indices,
            [7, 8, 9],
        )

    def test_registers_incident_endpoint(self):
        route_paths = {
            route.path
            for route in app.routes
        }

        self.assertIn("/api/incidents", route_paths)


if __name__ == "__main__":
    unittest.main()
