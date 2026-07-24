import os
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from freezegun import freeze_time
from googleapiclient.errors import HttpError

from component import Component
from configuration import Configuration, Destination, ReportSettings, TimeRange
from google_dv360 import GoogleDV360Client


class TestGetExistingReportId(unittest.TestCase):
    def _make_component(self):
        with patch("component.Component.__init__", return_value=None):
            comp = Component.__new__(Component)
        return comp

    def test_report_specification_always_returns_none(self):
        """report_specification mode must never reuse a cached query ID (SUPPORT-15580)."""
        comp = self._make_component()
        comp.cfg = Configuration(
            input_variant="report_specification",
            destination=Destination(table_name="out"),
            time_range=TimeRange(period="PREVIOUS_7_DAYS"),
            report_specification=ReportSettings(report_type="STANDARD"),
        )
        comp.get_state_file = MagicMock(
            return_value={
                "report": {"key": {"queryId": "1571390906"}},
                "configuration": {
                    "input_variant": "report_specification",
                    "destination": {"table_name": "out"},
                    "time_range": {"period": "PREVIOUS_7_DAYS"},
                    "report_specification": {"report_type": "STANDARD"},
                    "existing_report_id": "",
                    "debug": False,
                },
            }
        )
        client = MagicMock()

        result = comp.get_existing_report_id(client)

        self.assertIsNone(result)
        client.get_query.assert_not_called()

    def test_existing_report_id_mode_still_reuses(self):
        """existing_report_id mode should still return cached ID when config matches."""
        comp = self._make_component()
        comp.cfg = Configuration(
            input_variant="existing_report_id",
            destination=Destination(table_name="out"),
            time_range=TimeRange(period="PREVIOUS_7_DAYS"),
            existing_report_id="9999999",
        )
        comp.get_state_file = MagicMock(
            return_value={
                "report": {"key": {"queryId": "9999999"}},
                "configuration": {
                    "input_variant": "existing_report_id",
                    "destination": {"table_name": "out"},
                    "time_range": {"period": "PREVIOUS_7_DAYS"},
                    "report_specification": {},
                    "existing_report_id": "9999999",
                    "debug": False,
                },
            }
        )
        client = MagicMock()
        client.get_query.return_value = {"queryId": "9999999"}

        result = comp.get_existing_report_id(client)

        self.assertEqual(result, "9999999")


class TestComponent(unittest.TestCase):
    # set global time to 2010-10-10 - affects functions like datetime.now()
    @freeze_time("2010-10-10")
    # set KBC_DATADIR env to non-existing dir
    @mock.patch.dict(os.environ, {"KBC_DATADIR": "./non-existing-dir"})
    def test_run_no_cfg_fails(self):
        with self.assertRaises(ValueError):
            comp = Component()
            comp.run()


class TestExecuteWithRetry(unittest.TestCase):
    """Regression tests for the transient-error retry added around DV360 API calls.

    Covers the failure seen in production: a transient HTTP 500 from the DV360
    ``queries().run()`` call that previously crashed the job with an opaque internal
    error (exit 2). The retry must smooth over transient blips but still fail loudly on
    a persistent outage, and must NOT retry non-transient (4xx) errors.
    """

    def _make_client(self):
        # Bypass __init__ (it performs OAuth/network setup); we only test the helper.
        return GoogleDV360Client.__new__(GoogleDV360Client)

    @staticmethod
    def _http_error(status: int) -> HttpError:
        class _Resp:
            def __init__(self, s):
                self.status = s
                self.reason = f"HTTP {s}"

        return HttpError(_Resp(status), b"")

    @patch("google_dv360.client.time.sleep", return_value=None)
    def test_transient_5xx_retried_then_reraised(self, mock_sleep):
        """A persistent 5xx exhausts the attempts and re-raises — the job still fails."""
        client = self._make_client()
        request = MagicMock()
        request.execute.side_effect = self._http_error(500)

        with self.assertRaises(HttpError) as ctx:
            client._execute_with_retry(request, attempts=3)

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertEqual(request.execute.call_count, 3)  # every attempt was used
        self.assertEqual(mock_sleep.call_count, 2)  # backoff between attempts, not after last

    @patch("google_dv360.client.time.sleep", return_value=None)
    def test_transient_then_success(self, mock_sleep):
        """A single transient blip is absorbed and the eventual success is returned."""
        client = self._make_client()
        request = MagicMock()
        expected = {"key": {"reportId": "42"}}
        request.execute.side_effect = [self._http_error(503), expected]

        result = client._execute_with_retry(request, attempts=5)

        self.assertEqual(result, expected)
        self.assertEqual(request.execute.call_count, 2)

    @patch("google_dv360.client.time.sleep", return_value=None)
    def test_non_transient_4xx_not_retried(self, mock_sleep):
        """A 4xx error is raised immediately without retrying (caller maps it to UserException)."""
        client = self._make_client()
        request = MagicMock()
        request.execute.side_effect = self._http_error(404)

        with self.assertRaises(HttpError) as ctx:
            client._execute_with_retry(request, attempts=5)

        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(request.execute.call_count, 1)
        mock_sleep.assert_not_called()

    @patch("google_dv360.client.time.sleep", return_value=None)
    def test_happy_path_executes_once(self, mock_sleep):
        """When the request succeeds first try, behaviour matches a plain execute()."""
        client = self._make_client()
        request = MagicMock()
        expected = {"key": {"reportId": "7"}}
        request.execute.return_value = expected

        result = client._execute_with_retry(request)

        self.assertEqual(result, expected)
        self.assertEqual(request.execute.call_count, 1)
        mock_sleep.assert_not_called()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
