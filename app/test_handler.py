import json
import unittest

from handler import lambda_handler


class TestHandler(unittest.TestCase):
    def test_health_response(self):
        """Verify the health endpoint returns a successful response."""
        result = lambda_handler({}, None)

        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(
            result["headers"]["Content-Type"],
            "application/json",
        )

        body = json.loads(result["body"])

        self.assertEqual(body["status"], "broken")
        self.assertEqual(body["service"], "project-atlas")

    def test_response_contains_version(self):
        """Verify the response includes a version field."""
        result = lambda_handler({}, None)
        body = json.loads(result["body"])

        self.assertIn("version", body)
        self.assertTrue(body["version"])

    def test_response_contains_timestamp(self):
        """Verify the response includes a timestamp."""
        result = lambda_handler({}, None)
        body = json.loads(result["body"])

        self.assertIn("timestamp", body)
        self.assertTrue(body["timestamp"])

    def test_request_id_falls_back_to_local(self):
        """Verify the request ID fallback works without Lambda context."""
        result = lambda_handler({}, None)
        body = json.loads(result["body"])

        self.assertEqual(body["request_id"], "local")


if __name__ == "__main__":
    unittest.main()
