from unittest.mock import patch

from django.db.utils import OperationalError
from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def setUp(self):
        self.url = reverse("health-check")

    def test_health_check_happy_path_returns_200_and_connected(self):
        """DB is actually reachable in the test DB -> 200, db=connected."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "db": "connected"})

    def test_health_check_returns_503_when_db_unreachable(self):
        """Failure case 1: DB connection raises -> 503, db=disconnected."""
        with patch("core.views.connection.cursor", side_effect=OperationalError("could not connect")):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "error", "db": "disconnected"})

    def test_health_check_rejects_non_get_methods(self):
        """Failure case 2: POST (or any non-GET) is not allowed -> 405."""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 405)

    def test_health_check_does_not_require_authentication(self):
        """No Authorization header is needed, per the global convention
        that only /register and /login skip auth -- health is the other
        documented exception."""
        response = self.client.get(self.url)

        self.assertNotEqual(response.status_code, 401)
