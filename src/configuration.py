from dataclasses import dataclass
import dataconf

KEY_PARAM_INPUT_VARIANT = "report_settings"
KEY_PARAM_ENTRY_ID = "entry_id"
KEY_PARAM_REPORT_SETTINGS = 'report_settings'
KEY_PARAM_REPORT_TYPE = 'report_type'
KEY_PARAM_REPORT_DIMENSIONS = 'dimensions'
KEY_PARAM_REPORT_METRICS = 'metrics'
KEY_PARAM_REPORT_FILTERS = 'filters'
KEY_PARAM_DESTINATION = 'destination'
KEY_PARAM_PRIMARY_KEYS = 'primary_keys'
KEY_PARAM_LOAD_TYPE = 'load_type'
KEY_PARAM_TIME_RANGE = 'time_range'
KEY_TIME_RANGE_PERIOD = 'period'
KEY_TIME_RANGE_FROM = 'date_from'
KEY_TIME_RANGE_TO = 'date_to'

from keboola.component.exceptions import UserException


class ConfigurationException(UserException):
    pass


@dataclass
class FilterPair:
    name: str
    value: str


@dataclass
class Destination:
    load_type: str = ""
    primary_keys: list[str] = None


@dataclass
class TimeRange:
    period: str
    date_from: str = ""
    date_to: str = ""


@dataclass
class ReportSettings:
    report_type: str = None
    dimensions: list[str] = None
    metrics: list[str] = None
    filters: list[FilterPair] = None


@dataclass
class Configuration:
    input_variant: str
    destination: Destination
    time_range: TimeRange
    entry_id: str = ""
    report_settings: ReportSettings = ReportSettings()


@dataclass
class Configuration_2_delete:
    input_variant: str = None
    entry_id: str = None
    report_type: str = None
    dimensions: list[str] = None
    metrics: list[str] = None
    filters: list[(str, str)] = None
    primary_keys: list[str] = None
    load_type: str = None
    time_period: str = None
    date_from: str = None
    date_to: str = None

    def init_from_parameters(self, parameters: dict):
        self.input_variant = parameters[KEY_PARAM_INPUT_VARIANT]
        if self.input_variant == 'report_settings':
            report_settings = parameters[KEY_PARAM_REPORT_SETTINGS]
            self.report_type = report_settings[KEY_PARAM_REPORT_TYPE]
            self.dimensions = report_settings[KEY_PARAM_REPORT_DIMENSIONS]
            self.metrics = report_settings[KEY_PARAM_REPORT_METRICS]
            self.filters = [(filter_pair['name'], filter_pair['value'])
                            for filter_pair in report_settings[KEY_PARAM_REPORT_FILTERS]]
        elif self.input_variant == 'entry_id':
            self.entry_id = parameters[KEY_PARAM_ENTRY_ID]
        else:
            raise ConfigurationException(f'invalid configuration {KEY_PARAM_ENTRY_ID} = {self.input_variant}')

        destination_spec = parameters[KEY_PARAM_DESTINATION]

        time_range_spec = parameters[KEY_PARAM_TIME_RANGE]

        pass


if __name__ == '__main__':


    json_conf_1 = """
{
  "input_variant": "report_settings",
  "entry_id": ""
  "time_range": {
    "period": "LAST_90_DAYS"
    "date_from": "yesterday"
    "date_to": "today"
  },
  "report_settings": {
    "report_type": "STANDARD",
    "dimensions": [
      "FILTER_ADVERTISER",
      "FILTER_ADVERTISER_NAME",
      "FILTER_BROWSER"
    ],
    "metrics": ["METRIC_CLICKS", "METRIC_COUNTERS", "METRIC_ENGAGEMENTS"],
    "filters": [ {
          "name": "FILTER_ADVERTISER",
          "value": "630317194"
        }]
  },
  "destination": {
    "primary_keys": [
      "FILTER_ADVERTISER",
      "FILTER_BROWSER"
    ],
    "load_type": "incremental_load"
  }
}
    """

    json_conf_2 = """
    {
      "input_variant": "report_settings",
      "entry_id": ""
      "time_range": {
        "period": "LAST_90_DAYS"
        "date_from": "yesterday"
        "date_to": "dneska"
      },
      "report_settings": {
        "report_type": "STANDARD",
        "dimensions": [
          "FILTER_ADVERTISER",
          "FILTER_ADVERTISER_NAME",
          "FILTER_BROWSER"
        ],
        "metrics": ["METRIC_CLICKS", "METRIC_COUNTERS", "METRIC_ENGAGEMENTS"],
        "filters": [ {
              "name": "FILTER_ADVERTISER",
              "value": "630317194"
            }]
      },
      "destination": {
        "primary_keys": [
          "FILTER_ADVERTISER",
          "FILTER_BROWSER"
        ],
        "load_type": "incremental_load"
      }
    }
        """

    cf1 = dataconf.loads(json_conf_1, Configuration)
    cf2 = dataconf.loads(json_conf_2, Configuration)

    print(f'Equality cf1 == cf2 {cf1 == cf2}')

    pass
