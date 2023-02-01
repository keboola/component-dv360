import logging
import time
from typing import List, Tuple
import requests

from google_auth_oauthlib.flow import Flow
from googleapiclient import discovery
from keboola.component.exceptions import UserException


class GoogleDV360ClientException(UserException):
    pass


# TODO: Employ logging
class GoogleDV360Client:
    def __init__(self, oauth_credentials):
        self.service = None
        token_response = oauth_credentials.data
        token_response['expires_at'] = 22222
        client_secrets = {
            "web": {
                "client_id": oauth_credentials.appKey,
                "client_secret": oauth_credentials.appSecret,
                "redirect_uris": ["https://www.example.com/oauth2callback"],
                "auth_uri": "https://oauth2.googleapis.com/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        scopes = ['https://www.googleapis.com/auth/doubleclickbidmanager']
        credentials = Flow.from_client_config(client_secrets, scopes=scopes, token=token_response).credentials
        discovery_url = 'https://doubleclickbidmanager.googleapis.com/$discovery/rest?version=v2'
        # Build the API service.
        self.service = discovery.build(
            'doubleclickbidmanager',
            'v2',
            discoveryServiceUrl=discovery_url,
            credentials=credentials)

    def test_connection(self):
        pass

    def create_report(self,
                      report_type: str,
                      dimensions: List[str],
                      metrics: List[str],
                      filters: List[Tuple[str, str]]) -> str:
        """

        Args:
            report_type:
            dimensions:
            metrics:
            filters:

        Returns:

        """
        body = {
            "metadata": {
                "title": "generated_report",
                "format": "CSV",
                "dataRange": {
                    "range": "PREVIOUS_DAY"
                }
            },
            "params": {
                "type": report_type,
                "groupBys": dimensions,
                "filters": [dict(type=f[0], value=f[1]) for f in filters],
                "metrics": metrics
            },
            "schedule": {
                "frequency": "ONE_TIME"
            }
        }
        m = self.service.queries().create(body=body)
        response = m.execute()
        report_id = response['queryId']
        return report_id

    def run_report(self, report_id: str, data_range: str, date_from=None, date_to=None):
        body = {
            "dataRange": {
                # TODO: Complete date_from x date_to handling in case of 'CUSTOM_DATES' data_range
                "range": data_range
            }
        }
        m = self.service.queries().run(body=body, queryId=report_id)
        response = m.execute()
        run_id = response['key']['reportId']
        logging.info(f"Running query : {report_id}:{run_id}")
        return run_id

    def wait_report(self, report_id: str, run_id: str) -> str:
        m = self.service.queries().reports().get(queryId=report_id, reportId=run_id)
        # TODO: Repeat execute until we get some final state or until timeout (not yet introduced)
        while True:
            response = m.execute()
            state = response['metadata']['status']['state']
            logging.info(f"Report state : {state}")
            if state == 'DONE':
                url = response['metadata']['googleCloudStoragePath']
                resp_report = requests.get(url)
                return resp_report.text
            if state == 'FAILED':
                # TODO: more elaborate exception description
                raise GoogleDV360ClientException('report failed')
            # TODO: some exponential time wait time handling
            time.sleep(30)

    def list_queries(self) -> list[(str, str)]:
        response = self.service.queries().list(pageSize='100').execute()
        if 'queries' in response:
            return [(query['queryId'], query['metadata']['title']) for query in response['queries']]
        else:
            return []
