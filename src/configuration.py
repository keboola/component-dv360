from dataclasses import dataclass
import dataconf

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

    def __eq__(self, other):
        if self.input_variant == "entry_id":
            return self.entry_id == other.entry_id
        else:
            return self.report_settings == other.report_settings


if __name__ == '__main__':
    json_conf_1 = """
{
  "input_variant": "report_settings",
  "entry_id": ""
  "time_range": {
    "period": "LAST_90_DAYS",
    "date_from": "yesterday"
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
