'''
Created on 12. 11. 2018

@author: esner
'''
import unittest
import mock
import os
from freezegun import freeze_time
from unittest.mock import MagicMock, patch

from component import Component
from configuration import Configuration, ReportSettings, Destination, TimeRange


class TestGetExistingReportId(unittest.TestCase):

    def _make_component(self):
        with patch('component.Component.__init__', return_value=None):
            comp = Component.__new__(Component)
        return comp

    def test_report_specification_always_returns_none(self):
        """report_specification mode must never reuse a cached query ID (SUPPORT-15580)."""
        comp = self._make_component()
        comp.cfg = Configuration(
            input_variant='report_specification',
            destination=Destination(table_name='out'),
            time_range=TimeRange(period='PREVIOUS_7_DAYS'),
            report_specification=ReportSettings(report_type='STANDARD'),
        )
        comp.get_state_file = MagicMock(return_value={
            'report': {'key': {'queryId': '1571390906'}},
            'configuration': {
                'input_variant': 'report_specification',
                'destination': {'table_name': 'out'},
                'time_range': {'period': 'PREVIOUS_7_DAYS'},
                'report_specification': {'report_type': 'STANDARD'},
                'existing_report_id': '',
                'debug': False,
            }
        })
        client = MagicMock()

        result = comp.get_existing_report_id(client)

        self.assertIsNone(result)
        client.get_query.assert_not_called()

    def test_existing_report_id_mode_still_reuses(self):
        """existing_report_id mode should still return cached ID when config matches."""
        comp = self._make_component()
        comp.cfg = Configuration(
            input_variant='existing_report_id',
            destination=Destination(table_name='out'),
            time_range=TimeRange(period='PREVIOUS_7_DAYS'),
            existing_report_id='9999999',
        )
        comp.get_state_file = MagicMock(return_value={
            'report': {'key': {'queryId': '9999999'}},
            'configuration': {
                'input_variant': 'existing_report_id',
                'destination': {'table_name': 'out'},
                'time_range': {'period': 'PREVIOUS_7_DAYS'},
                'report_specification': {},
                'existing_report_id': '9999999',
                'debug': False,
            }
        })
        client = MagicMock()
        client.get_query.return_value = {'queryId': '9999999'}

        result = comp.get_existing_report_id(client)

        self.assertEqual(result, '9999999')


class TestComponent(unittest.TestCase):

    # set global time to 2010-10-10 - affects functions like datetime.now()
    @freeze_time("2010-10-10")
    # set KBC_DATADIR env to non-existing dir
    @mock.patch.dict(os.environ, {'KBC_DATADIR': './non-existing-dir'})
    def test_run_no_cfg_fails(self):
        with self.assertRaises(ValueError):
            comp = Component()
            comp.run()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
