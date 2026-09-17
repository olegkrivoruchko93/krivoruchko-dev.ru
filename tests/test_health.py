import unittest
from unittest.mock import MagicMock, patch

from app.health import _probe_url


class HealthProbeTests(unittest.TestCase):
    @patch("app.health.urllib.request.urlopen")
    def test_401_counts_as_up_by_default(self, urlopen_mock: MagicMock) -> None:
        exc = __import__("urllib.error", fromlist=["HTTPError"]).HTTPError(
            "https://example.com/", 401, "Unauthorized", {}, None
        )
        urlopen_mock.side_effect = exc

        self.assertTrue(_probe_url("https://example.com/", strict=False))

    @patch("app.health.urllib.request.urlopen")
    def test_401_strict_mode_fails(self, urlopen_mock: MagicMock) -> None:
        exc = __import__("urllib.error", fromlist=["HTTPError"]).HTTPError(
            "https://example.com/", 401, "Unauthorized", {}, None
        )
        urlopen_mock.side_effect = exc

        self.assertFalse(_probe_url("https://example.com/", strict=True))


if __name__ == "__main__":
    unittest.main()
