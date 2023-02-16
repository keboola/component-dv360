from dataclasses import dataclass, field
import dataconf


from pyhocon.config_tree import ConfigTree


@dataclass
class FilterPair:
    name: str
    value: str


@dataclass
class Destination:
    table_name: str
    incremental_loading: bool = True
    primary_key: list[str] = None
    primary_key_existing: list[str] = None


@dataclass
class TimeRange:
    period: str
    date_from: str = ""
    date_to: str = ""


@dataclass
class ReportSettings:
    report_type: str = ""
    dimensions: list[str] = None
    metrics: list[str] = None
    filters: list[FilterPair] = None


class ConfigurationBase:

    @staticmethod
    def fromDict(parameters: dict):
        return dataconf.dict(parameters, Configuration, ignore_unexpected=True)
        pass


@dataclass
class Configuration(ConfigurationBase):
    input_variant: str
    destination: Destination
    time_range: TimeRange
    report_specification: ReportSettings = field(default_factory=lambda: ConfigTree({}))
    existing_report_id: str = ""
    debug: bool = False

    def __eq__(self, other):
        if self.input_variant == "existing_report_id":
            return self.existing_report_id == other.existing_report_id
        else:
            return self.report_specification == other.report_specification


if __name__ == '__main__':
    json_conf_1 = """
    {
      "input_variant": "report_specification",
      "existing_report_id": ""
      "time_range": {
        "period": "LAST_90_DAYS"
        "date_from": "yesterday"
        "date_to": "dneska"
      },
      "report_specification": {
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
        "table_name": "report_row_1.csv",
        "incremental_loading": true,
        "primary_key": [
          "FILTER_ADVERTISER",
          "FILTER_BROWSER"
        ]
      },
      "debug": true,
      "dalsi_parametr": 12
    }
    """

    json_conf_2 = """
    {
      "input_variant": "report_specification",
      "existing_report_id": ""
      "time_range": {
        "period": "LAST_90_DAYS"
        "date_from": "yesterday"
        "date_to": "dneska"
      },
      "report_specification": {
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
        "table_name": "report_row_1.csv",
        "incremental_loading": true,
        "primary_key": [
          "FILTER_ADVERTISER",
          "FILTER_BROWSER"
        ]
      },
      "debug": true,
      "dalsi_parametr": 12
    }
        """

    # cf1 = dataconf.loads(json_conf_1, Configuration)
    cf2 = dataconf.loads(json_conf_2, Configuration, ignore_unexpected=True)

    # print(f'Equality cf1 == cf2 {cf1 == cf2}')

    pars = {
        "input_variant": "report_specification",
        "time_range": {
            "period": "LAST_90_DAYS",
            "date_from": "yesterday",
            "date_to": "dneska"
        },
        "destination": {
            "table_name": "report_row_1.csv",
            "primary_key": [
                "FILTER_ADVERTISER",
                "FILTER_BROWSER"
            ],
            "incremental_loading": True,
        }
    }

    cf3 = Configuration.fromDict(pars)

    pass
