import logging
import time

import dateparser
from google_auth_oauthlib.flow import Flow
from googleapiclient import discovery
from keboola.component.exceptions import UserException
from typing import List, Tuple


class GoogleDV360ClientException(UserException):
    pass


def get_date_period_converted(period_from: str, period_to: str) -> Tuple[dict, dict]:
    """
    Returns given period parameters in datetime format, or next step in back-fill mode
    along with generated last state for next iteration.

    :param period_from: str YYYY-MM-DD or relative string supported by date parser e.g. 5 days ago
    :param period_to: str YYYY-MM-DD or relative string supported by date parser e.g. 5 days ago

    :return: start_date: datetime, end_date: datetime
    """

    start_date_form = dateparser.parse(period_from)
    end_date_form = dateparser.parse(period_to)
    if not start_date_form or not end_date_form:
        raise UserException("Error with dates, make sure both start and end date are defined properly")
    day_diff = (end_date_form - start_date_form).days
    if day_diff < 0:
        raise UserException("start_date cannot exceed end_date.")

    start = dict(
        year=start_date_form.year,
        month=start_date_form.month,
        day=start_date_form.day)

    end = dict(
        year=end_date_form.year,
        month=end_date_form.month,
        day=end_date_form.day)

    return start, end


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
        # TODO: implement
        pass

    def create_report(self,
                      report_name: str,
                      report_type: str,
                      dimensions: List[str],
                      metrics: List[str],
                      filters: List[Tuple[str, str]]) -> str:
        """

        Args:
            report_name: A query name that will be stored in dv360 service
            report_type: One of dv360 predefined report types
            dimensions: Selection of dimensions (group by filters in dv360 terminology) to include
            metrics: Selection dv360 metrics to include
            filters: List of filter pairs to limit source data

        Returns:

        """
        body = {
            "metadata": {
                "title": report_name,
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
        try:
            response = m.execute()
        except Exception as ex:
            if hasattr(ex, 'reason'):
                raise UserException(ex.reason)
            raise ex
        report_id = response['queryId']
        return report_id

    def run_report(self, report_id: str, data_range: str, date_from=None, date_to=None):
        body = {
            "dataRange": {
                "range": data_range
            }
        }
        if data_range == 'CUSTOM_DATES':
            body["dataRange"]["customStartDate"], body["dataRange"]["customEndDate"] = get_date_period_converted(
                date_from, date_to)

        m = self.service.queries().run(body=body, queryId=report_id)
        response = m.execute()
        run_id = response['key']['reportId']
        logging.info(f"Running query : {report_id}:{run_id}")
        return run_id

    def wait_report(self, report_id: str, run_id: str) -> dict:
        m = self.service.queries().reports().get(queryId=report_id, reportId=run_id)
        while True:  # TODO: consider some timeout - currently we terminate on 'DONE' or abort on error
            response = m.execute()
            state = response['metadata']['status']['state']
            logging.info(f"Checking report state : {state}")
            if state == 'DONE':
                return response
            if state == 'FAILED':
                raise GoogleDV360ClientException(f'report failed: {response["metadata"]}')
            time.sleep(30)

    def list_queries(self) -> list[(str, str)]:
        page_token = None
        query_list = []
        while True:
            response = self.service.queries().list(pageSize=100, orderBy='queryId desc', pageToken=page_token).execute()
            if 'queries' in response:
                query_list.extend([(query['queryId'], query['metadata']['title']) for query in response['queries']])
                page_token = response.get('nextPageToken')
                if not page_token:
                    break
            else:
                break
        return query_list

    def get_query(self, query_id: str) -> object | None:
        """ Search for specific query

        If query exists corresponding dv360 object will be returned.

        Args:
            query_id: Query ID to search for

        Returns: dv360 query object or None

        """
        try:
            response = self.service.queries().get(queryId=query_id).execute()
            return response
        except Exception:
            return None
        pass

    def delete_query(self, query_id: str):
        try:
            self.service.queries().delete(queryId=query_id).execute()
        except Exception:
            pass
