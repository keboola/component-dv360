"""
Template Component main class.

"""
import logging

from google_auth_oauthlib.flow import Flow
from googleapiclient import discovery
from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

# configuration variables
KEY_API_TOKEN = '#api_token'
KEY_PRINT_HELLO = 'print_hello'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_PRINT_HELLO]
REQUIRED_IMAGE_PARS = []


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
        token_response = self.configuration.oauth_credentials.data

        # this has to be set to something low to force refresh and make the oAuthlib2 work.
        token_response['expires_at'] = 22222
        # Google secrets format
        client_secrets = {
            "web": {
                "client_id": self.configuration.oauth_credentials.appKey,
                "client_secret": self.configuration.oauth_credentials.appSecret,
                "redirect_uris": ["https://www.example.com/oauth2callback"],
                "auth_uri": "https://oauth2.googleapis.com/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }

        scopes = ['https://www.googleapis.com/auth/doubleclickbidmanager']
        credentials = Flow.from_client_config(client_secrets, scopes=scopes, token=token_response).credentials

        # Build the discovery document URL.
        discovery_url = 'https://doubleclickbidmanager.googleapis.com/$discovery/rest?version=v2'

        # Build the API service.
        service = discovery.build(
            'doubleclickbidmanager',
            'v2',
            discoveryServiceUrl=discovery_url,
            credentials=credentials)

        # Build and execute queries.listqueries request.

        query = {
            "metadata": {
                "title": "My_2nd_query",
                "format": "CSV",
                "dataRange": {
                    "range": "LAST_7_DAYS"
                }
            },
            "params": {
                "type": "STANDARD",
                "groupBys": [
                    "FILTER_ADVERTISER_NAME",
                    "FILTER_PARTNER_NAME",
                    "FILTER_MEDIA_PLAN_NAME",
                    "FILTER_BROWSER",
                    "FILTER_COUNTRY"
                ],
                "metrics": [
                    "METRIC_IMPRESSIONS",
                    "METRIC_CLICKS",
                    "METRIC_CTR",
                    "METRIC_TOTAL_CONVERSIONS"
                ],
                "filters": [
                ]
            },
            "schedule": {
                "frequency": "ONE_TIME"
            }
        }

        # q = service.queries()
        # m = q.delete(queryId=1047383473)
        # response = m.execute()

        body = {
            "dataRange": {
                # "range": "PREVIOUS_YEAR"
                "range": "LAST_7_DAYS"
            }
        }

        # m = q.run(body=body, queryId=1047383473, synchronous=True)

        rl = service.queries().reports()
        m = rl.list(queryId=1047383473)


        response = m.execute()

        print(response)

        response = service.queries().list(pageSize='100').execute()

        # Print queries out.
        if 'queries' in response:
            print('Id\t\tName')
            for query in response['queries']:
                print('%s\t%s' % (query['queryId'], query['metadata']['title']))
        else:
            print('No queries exist.')


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
