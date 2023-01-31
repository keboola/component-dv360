"""
Template Component main class.

"""
import logging

from google_auth_oauthlib.flow import Flow
from googleapiclient import discovery
from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException
from google_dv360 import GoogleDV360Client, translate_filters

# configuration variables
KEY_API_TOKEN = '#api_token'
KEY_PRINT_HELLO = 'print_hello'




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

    def run(self):
        """
        BDM example auth
        """

        contents = '''Advertiser ID,Advertiser,Browser,Clicks,Rich Media Custom Counters,Engagements
630317194,Test_BNRS,Firefox,1,0,0
630317194,Test_BNRS,Google Chrome,2,0,0
,,,3,0,0

Report Time:,2023/01/30 14:14 GMT
Date Range:,2022/11/01 to 2023/01/29
Group By:,Advertiser ID
Group By:,Advertiser
Group By:,Browser
MRC Accredited Metrics,"Clicks(Desktop Video, Desktop Display, Desktop Rich Media, Mobile Video, Mobile Display, Mobile Rich Media, In-App Video, In-App Display, In-App Rich Media)",Active View metrics are accredited only when Measurement Source = Measured
"Reporting numbers from the previous month are finalized (for billing purposes) on the first of each month, unless communicated otherwise. Some numbers in reports may fluctuate for up to seven days before matching billing numbers."
Filter by Advertiser ID:,Test_BNRS (630317194)
Filter by Partner ID:,995544
        '''
        r = contents.split('\n,', 2)
        csv_contents = r[0]

        pks = translate_filters(['FILTER_ADVERTISER', 'FILTER_BROWSER'])
        result_table = self.create_out_table_definition('output.csv', primary_key=pks, incremental=True)
        self.write_manifest(result_table)

        with open(result_table.full_path, 'w') as result:
            result.write(csv_contents)


        pass

        return

        client = GoogleDV360Client(self.configuration.oauth_credentials)

        parameters = self.configuration.parameters
        report_settings = parameters[KEY_PARAM_REPORT_SETTINGS]
        time_range_spec = parameters[KEY_PARAM_TIME_RANGE]

        report_type = report_settings[KEY_PARAM_REPORT_TYPE]
        dimensions = report_settings[KEY_PARAM_REPORT_DIMENSIONS]
        metrics = report_settings[KEY_PARAM_REPORT_METRICS]
        filters = [(filter_pair['name'], filter_pair['value'])
                   for filter_pair in report_settings[KEY_PARAM_REPORT_FILTERS]]

        data_range = time_range_spec[KEY_TIME_RANGE_PERIOD]
        date_from = time_range_spec.get(KEY_TIME_RANGE_FROM)
        date_to = time_range_spec.get(KEY_TIME_RANGE_TO)

        report = client.create_report(report_type, dimensions, metrics, filters)
        print(f'Query created: {report}')

        report_run_id = client.run_report(report, data_range)

        report_url = client.wait_report(report, report_run_id)

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
