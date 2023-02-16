# DV360 Extractor

This data source component is using Google Bid Manager API to create and run 
reports that measure results of Display & Video 360 advertising campaigns.


**Table of contents:**

[TOC]

## Prerequisites

1. Arrange authorization of your DV360 account with Keboola support.

2. Log into your account using the Authorize Account button in the Keboola interface. 

![OAuth Authorization](docs/imgs/config_oauth.png)

## Features

| **Feature**             | **Note**                                      |
|-------------------------|-----------------------------------------------|
| Generic UI form         | Dynamic UI form                               |
| Row Based configuration | Allows structuring the configuration in rows. |
| oAuth                   | oAuth authentication enabled                  |
| Incremental loading     | Allows fetching data in new increments.       |
| Dimension filter        | Fetch data of certain dimension values only.  |
| Date range filter       | Specify date range.                           |


## Supported endpoints

The component uses version 2 of Google Bid Manager API.

- `https://doubleclickbidmanager.googleapis.com`

It handles 2 resource types:
- v2.queries - [see reference to queries](https://doubleclickbidmanager.googleapis.com)
- v2.queries.reports - [see reference to reports](https://developers.google.com/bid-manager/reference/rest#rest-resource:-v2.queries.reports)

## Configuration

Component uses 2 configuration variants:
- Full report specification
- Report ID of existing report

In both cases it is possible to specify date ranges for the run of the report.

##DV360 Report
 - Input variant (input_variant) - [REQ] You may choose to either define a new report or to enter existing report ID
 - Time Range (time_range) - [REQ] description
 - Report Period (period) - [OPT] description
 - Date from (date_from) - [OPT] Start date: Either date in YYYY-MM-DD format or a relative date string i.e. 5 days ago, 1 month ago, yesterday, etc.
 - Date to (date_to) - [OPT] End date: Either date in YYYY-MM-DD format or a relative date string i.e. 5 days ago, 1 month ago, yesterday, etc.
 - Report Details (report_specification) - [OPT] description
 - Report Type (report_type) - [OPT] description
 - Dimensions (dimensions) - [OPT] description
 - Metrics (metrics) - [OPT] description
 - Filters (filters) - [OPT] description
 - Report ID (existing_report_id) - [OPT] Enter report ID as presented in DV360 Report Builder
 - Destination (destination) - [REQ] description
 - Selected variant (selected_variant) - [OPT] Helper dummy element to render pkeys
 - Storage Table Name (table_name) - [REQ] Name of the destination table for this report. (e.g. standard_performance_data).
 - Primary Key (primary_key) - [REQ] List of columns (from selected dimensions) to be used as primary key of the resulting table. We recommend using ID columns where possible, to avoid ambiguity in case the dimension name is changed.
 - Primary Key (primary_key_existing) - [OPT] List of columns (load from report) to be used as primary key of the resulting table. We recommend using ID columns where possible, to avoid ambiguity in case the dimension name is changed.
 - Load Type (incremental_loading) - [REQ] If Full load is used, the destination table will be overwritten every run. If Incremental Load is used, data will be upserted into the destination table.
 - Debug (debug) - [OPT] When checked, logging will be more verbose


## Sample Configuration

```json
{
    "storage": {
        "input": {
            "files": [],
            "tables": [
                {
                    "source": "in.c-test.test",
                    "destination": "test.csv",
                    "limit": 50,
                    "columns": [],
                    "where_values": [],
                    "where_operator": "eq"
                }
            ]
        },
        "output": {
            "files": [],
            "tables": []
        }
    },
    "parameters": {
        "time_range": {
            "period": "CUSTOM_DATES",
            "date_from": "120 days ago",
            "date_to": "today"
        },
        "destination": {
            "table_name": "report_row_1",
            "incremental_loading": true,
            "primary_key": [
                "FILTER_ADVERTISER",
                "FILTER_ADVERTISER_NAME",
                "FILTER_BROWSER"
            ]
        },
        "input_variant": "report_specification",
        "report_specification": {
            "filters": [
                {
                    "name": "FILTER_ADVERTISER",
                    "value": "630317194"
                }
            ],
            "metrics": [
                "METRIC_CLICKS",
                "METRIC_COUNTERS",
                "METRIC_ENGAGEMENTS"
            ],
            "dimensions": [
                "FILTER_ADVERTISER",
                "FILTER_ADVERTISER_NAME",
                "FILTER_BROWSER"
            ],
            "report_type": "YOUTUBE"
        },
        "existing_report_id": "",
        "debug": false
    },
    "image_parameters": {
        "syrup_url": "https://syrup.keboola.com/"
    },
    "authorization": {
        "oauth_api": {
            "id": "OAUTH_API_ID",
            "credentials": {
                "id": "main",
                "authorizedFor": "Myself",
                "creator": {
                    "id": "1234",
                    "description": "me@keboola.com"
                },
                "created": "2016-01-31 00:13:30",
                "#data": "{\n    \"access_token\": \"ya29.a0AX9GBdWIPO_vxymZ6TnTLNp3ZBzWYbgL2CZ13SDS64V1hWm0C7nk-X4OQ7sCMSKxZQFP5oOHrWef5Yu1f_eZMmoBOS6ddDOxPSKp3xAG1QI1nrIe-CgpTg0EEKiB7vLa9IRv7cWQ-jO41dfHTWCw6iPdvojdaCgYKAQQSARMSFQHUCsbC5wpREHiB4-rzu7tQFgTmfA0163\",\n    \"scope\": \"https://www.googleapis.com/auth/doubleclickbidmanager\",\n    \"token_type\": \"Bearer\",\n    \"expires_in\": 3599,\n    \"refresh_token\": \"1//04AWs1av4uUF2CgYIARAAGAQSNwF-L9IrOqig-Xyig3ckKS_BEnvnd_JMneoJMdZPr5lxmLkWIzDV4-c_e_O5xS6fThkWlIkvatc\"\n}",
                "oauthVersion": "2.0",
                "appKey": "306269445270-icka3qa2liqrbkinij89v6uk1e1e21nd.apps.googleusercontent.com",
                "#appSecret": "KgAZGxKZ1RGVoGbNbDE-DclC"
            }
        }
    },
    "action": "validate_query"
}
```

Output
======

List of tables, foreign keys, schema.

Development
-----------

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to your custom path in
the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone this repository, init the workspace and run the component with following command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose build
docker-compose run --rm dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the test suite and lint check using this command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose run --rm test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration
===========

For information about deployment and integration with KBC, please refer to the
[deployment section of developers documentation](https://developers.keboola.com/extend/component/deployment/)