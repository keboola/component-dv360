from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(extra="ignore")


class FilterPair(_Base):
    name: str
    value: str


class Destination(_Base):
    table_name: str
    incremental_loading: bool = True
    primary_key: list[str] = Field(default_factory=list)
    primary_key_existing: list[str] = Field(default_factory=list)
    normalize_header: bool = True


class TimeRange(_Base):
    period: str
    date_from: str = ""
    date_to: str = ""


class ReportSettings(_Base):
    report_type: str = ""
    dimensions: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    filters: list[FilterPair] = Field(default_factory=list)


class Configuration(_Base):
    input_variant: str
    destination: Destination
    time_range: TimeRange
    report_specification: ReportSettings = Field(default_factory=ReportSettings)
    existing_report_id: str = ""
    debug: bool = False

    @staticmethod
    def fromDict(parameters: dict) -> Configuration:
        return Configuration.model_validate(parameters)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Configuration):
            return NotImplemented
        if self.input_variant == "existing_report_id":
            return self.existing_report_id == other.existing_report_id
        return self.report_specification == other.report_specification

    def __hash__(self) -> int:
        return hash((self.input_variant, self.existing_report_id))
