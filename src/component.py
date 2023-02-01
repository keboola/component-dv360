"""
Template Component main class.

"""
import logging
# from typing import List, Tuple

# from google_auth_oauthlib.flow import Flow
# from googleapiclient import discovery
from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException
from google_dv360 import GoogleDV360Client, translate_filters
from configuration import Configuration


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

    def write_report(self, contents: str):
        """

        Args:
            contents:

        Returns:

        """
        r = contents.split('\n,', 2)
        csv_contents = r[0]
        pks = translate_filters(self.cfg.destination.primary_keys)
        result_table = self.create_out_table_definition('report.csv', primary_key=pks, incremental=True)
        self.write_manifest(result_table)
        with open(result_table.full_path, 'w') as result:
            result.write(csv_contents)

    def run(self):
        """
        BDM example auth
        """

        logging.debug(self.environment_variables)

        logging.debug(self.configuration.parameters)

        self.cfg = Configuration.fromDict(self.configuration.parameters)

        logging.debug(self.cfg)

        client = GoogleDV360Client(self.configuration.oauth_credentials)

        if self.cfg.input_variant == 'report_settings':
            filters = [(filter_pair.name, filter_pair.value) for filter_pair in self.cfg.report_settings.filters]
            report = client.create_report(self.cfg.report_settings.report_type,
                                          self.cfg.report_settings.dimensions,
                                          self.cfg.report_settings.metrics,
                                          filters)
        else:
            report = self.cfg.entry_id

        print(f'Query created: {report}')

        report_run_id = client.run_report(report,
                                          self.cfg.time_range.period,
                                          date_from=self.cfg.time_range.date_from,
                                          date_to=self.cfg.time_range.date_to)

        report_contents = client.wait_report(report, report_run_id)

        self.write_report(report_contents)

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
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
