"""
Template Component main class.

"""
# from typing import List, Tuple
import json
import logging

import dataconf
# from google_auth_oauthlib.flow import Flow
# from googleapiclient import discovery
import requests
from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

from configuration import Configuration
from google_dv360 import GoogleDV360Client, translate_filters


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

    def __init__(self):
        super().__init__()
        self.cfg = None

    @staticmethod
    def download_file(url: str, result_file_path: str):
        # avoid loading all into memory
        res = requests.get(url, stream=True, timeout=180)
        res.raise_for_status()

        with open(result_file_path, 'wb') as out:
            for chunk in res.iter_content(chunk_size=8192):
                out.write(chunk)

    @staticmethod
    def extract_csv_from_raw(raw_file: str, csv_file: str):
        with open(raw_file, 'r') as src, open(csv_file, 'w') as dst:
            while True:
                line = src.readline()
                if not line or line.startswith(',') or line == '\n':
                    break
                dst.write(line)

            pass

    def write_report(self, contents_url: str):
        """

        Args:
            contents_url: URL where Google stored report contents

        Returns:

        """
        pks = translate_filters(self.cfg.destination.primary_key)
        result_table = self.create_out_table_definition(f"{self.cfg.destination.table_name}.csv",
                                                        primary_key=pks,
                                                        incremental=self.cfg.destination.incremental_loading)
        self.write_manifest(result_table)

        raw_output_file = self.files_out_path + '/' + result_table.name + '.raw.txt'
        self.download_file(contents_url, raw_output_file)
        self.extract_csv_from_raw(raw_output_file, result_table.full_path)

    def save_state(self, report_response):
        cur_state = dict(
            report=report_response,
            configuration=json.loads(dataconf.dumps(self.cfg, out="json"))
        )
        self.write_state_file(cur_state)

    def get_existing_report_id(self, client):
        """ Retrieves existing query ID

        Decide whether we may use already existing query generated previously.
        If state contains configuration identical to current configuration we check
        that correspondent query still exists in dv360 and if so we use its id.
        In any other case, we return None and caller will use a new query (either generated or supplied externally).

        Args:
            client: Service used to check query availability

        Returns: Query id if found else None

        """
        prev_state = self.get_state_file()
        if not prev_state.get('configuration') or not prev_state.get('report'):
            return None
        prev_report_id = prev_state['report']['key']['queryId']
        prev_cfg = Configuration.fromDict(prev_state.get('configuration'))
        if prev_cfg == self.cfg:
            # check for query existence
            q = client.get_query(prev_report_id)
            return prev_report_id if q else None
        # TODO: think over: delete orphan report_id - check input_variant was not entry_id case
        return None

    def generate_query_name(self):
        # TODO: Currently keboola has an inssue: It does not pass row-id in variables, we use a workaround:
        import os
        configrow_id = os.getenv('KBC_CONFIGROWID', 'xxxxxx')
        return 'generated_' + self.environment_variables.project_id + '_' + \
               self.environment_variables.config_id + '_' + \
               configrow_id

    def run(self):
        """
        BDM example auth
        """

        logging.debug(self.environment_variables)

        logging.debug(self.configuration.parameters)

        # TODO: validate parameters
        self.cfg = Configuration.fromDict(self.configuration.parameters)

        logging.debug(self.cfg)

        client = GoogleDV360Client(self.configuration.oauth_credentials)

        report_id = self.get_existing_report_id(client)

        if not report_id:
            if self.cfg.input_variant == 'report_settings':
                filters = [(filter_pair.name, filter_pair.value) for filter_pair in self.cfg.report_settings.filters]
                report_id = client.create_report(self.generate_query_name(),
                                                 self.cfg.report_settings.report_type,
                                                 self.cfg.report_settings.dimensions,
                                                 self.cfg.report_settings.metrics,
                                                 filters)
            else:
                report_id = self.cfg.entry_id

        print(f'Query created: {report_id}')

        report_run_id = client.run_report(report_id,
                                          self.cfg.time_range.period,
                                          date_from=self.cfg.time_range.date_from,
                                          date_to=self.cfg.time_range.date_to)

        # Response structure is documented here:
        # https://developers.google.com/bid-manager/reference/rest/v2/queries.reports#Report
        report_response = client.wait_report(report_id, report_run_id)

        contents_url = report_response['metadata']['googleCloudStoragePath']

        self.write_report(contents_url)

        self.save_state(report_response)

        queries = client.list_queries()
        print("Existing queries:")
        for (q_id, q_title) in queries:
            print(f'{q_id}: {q_title}')


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
