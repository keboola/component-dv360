"""
Template Component main class.

"""
# from typing import List, Tuple
import json
import logging

import dataconf
import requests
from google.auth.exceptions import RefreshError
from keboola.component.base import ComponentBase, sync_action
from keboola.component.exceptions import UserException
from keboola.utils.header_normalizer import DefaultHeaderNormalizer

from configuration import Configuration
from google_dv360 import GoogleDV360Client, translate_filters, get_filter_table, GoogleDV360ClientException


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
        self.cfg: Configuration = None

    def run(self):
        """
        Main component method.
        """

        logging.debug(self.configuration.parameters)
        self.cfg = Configuration.fromDict(self.configuration.parameters)

        self._validate_configuration()

        client = self._get_google_client()

        report_id = self.get_existing_report_id(client)

        if not report_id:
            if self.cfg.input_variant == 'report_specification':
                filters = [(filter_pair.name, filter_pair.value) for filter_pair in
                           self.cfg.report_specification.filters]
                report_id = client.create_report(self.generate_query_name(),
                                                 self.cfg.report_specification.report_type,
                                                 self.cfg.report_specification.dimensions,
                                                 self.cfg.report_specification.metrics,
                                                 filters)
            else:
                report_id = self.cfg.existing_report_id

        logging.info(f'Query used: {report_id}')

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

    def _get_google_client(self):
        if not self.configuration.oauth_credentials:
            raise UserException("The configuration is not authorized. Please authorize the configuration first.")

        client = GoogleDV360Client(
            self.configuration.oauth_credentials.appKey,
            self.configuration.oauth_credentials.appSecret,
            self.configuration.oauth_credentials.data
        )
        return client

    @staticmethod
    def download_file(url: str, result_file_path: str):
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

    def write_report(self, contents_url: str):
        """

        Args:
            contents_url: URL where Google stored report contents

        Returns: no value returned

        """
        pks_raw = self.cfg.destination.primary_key_existing if self.cfg.input_variant == 'existing_report_id' else \
            self.cfg.destination.primary_key
        header_normalizer = DefaultHeaderNormalizer()
        pks = header_normalizer.normalize_header(translate_filters(pks_raw))
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
        return None

    def generate_query_name(self):
        # TODO: Currently Keboola has an issue: It does not pass row-id in variables, we use a workaround:
        import os
        configrow_id = os.getenv('KBC_CONFIGROWID', 'xxxxxx')
        return 'keboola_generated_' + self.environment_variables.project_id + '_' + \
            self.environment_variables.config_id + '_' + \
            configrow_id

    @sync_action('list_queries')
    def list_queries(self):
        """ A sync action used by Keboola GUI to provide available report (query) IDs for Report ID field.

        Returns: List of dictionaries having value and label attributes.
        """
        client = self._get_google_client()
        queries = client.list_queries()
        # wish was to include query creation date but tha info is not available in the service
        resp = [dict(value=q[0], label=f'{q[0]} - {q[1]}') for q in queries]
        return resp

    @sync_action('list_report_dimensions')
    def list_report_dimensions(self):
        """ A sync action used by Keboola GUI to provide available dimensions for existing report (query)

        Returns: List of dictionaries having value and label attributes.
        """
        existing_report_id = self.configuration.parameters.get('existing_report_id')
        if not existing_report_id:
            raise UserException('No report ID provided.')
        client = self._get_google_client()
        query = client.get_query(query_id=existing_report_id)
        if not query:
            raise UserException(f'Report id = {existing_report_id} was not found')
        table = get_filter_table()
        resp = [dict(value=f, label=table.get(f)) for f in query["params"]["groupBys"]]
        return resp

    @sync_action('validate_query')
    def validate_query(self):
        """ A sync action used by Keboola GUI to check validity of entered data.
        Method uses GUI data and tries to create a query calling the service.
        If service succeeds report specification is considered valid.
        Created query is immediately deleted as it need not be the final specification.

        Returns: no return

        Raises: Exception when create query failed

        """
        report_specification = self.configuration.parameters.get('report_specification')
        if not report_specification:
            raise UserException('No report specification in configuration parameters')
        report_type = report_specification.get('report_type')
        dimensions = report_specification.get('dimensions')
        metrics = report_specification.get('metrics')
        filters = report_specification.get('filters')
        filters = [(filter_pair.get('name'), filter_pair.get('value')) for filter_pair in filters]

        client = self._get_google_client()

        report_id = client.create_report('just_dummy_2_delete', report_type, dimensions, metrics, filters)

        client.delete_query(report_id)

    def _validate_configuration(self):
        errors = []
        if self.cfg.input_variant == 'report_specification':
            if not self.cfg.report_specification.metrics:
                errors.append("At least one metric needs to be specified!")
            if not self.cfg.report_specification.dimensions:
                errors.append("At least one dimension needs to be specified!")
        if errors:
            err_string = '\n'.join(errors)
            raise UserException(f'The configuration is not valid, following errors occurred: \n{err_string}')


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        comp.execute_action()
    except (UserException, GoogleDV360ClientException) as exc:
        logging.exception(exc)
        exit(1)
    except RefreshError as exc:
        logging.error("The OAuth token has expired. Please reauthorize the application.", extra={"exception": exc})
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
