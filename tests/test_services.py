import json
import tempfile
import unittest
from pathlib import Path

from app.services import load_services


class LoadServicesTests(unittest.TestCase):
    def test_normalizes_empty_color(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "services.json"
            path.write_text(
                json.dumps(
                    {
                        "demo": {
                            "name": "Demo",
                            "url": "https://example.com/",
                            "color": "",
                        }
                    }
                ),
                encoding="utf-8",
            )
            services = load_services(path)
            self.assertEqual(services["demo"]["color"], "#6c8cff")

    def test_skips_invalid_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "services.json"
            path.write_text(
                json.dumps(
                    {
                        "bad": {"name": "No URL"},
                        "good": {
                            "name": "Good",
                            "url": "https://example.com/",
                        },
                    }
                ),
                encoding="utf-8",
            )
            services = load_services(path)
            self.assertNotIn("bad", services)
            self.assertIn("good", services)


class AppTests(unittest.TestCase):
    def test_health_endpoint(self):
        from main import app

        client = app.test_client()
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
