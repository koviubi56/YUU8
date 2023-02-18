import datetime
import enum
from typing import Any, Dict, List, Optional, Tuple

import requests

SUMMARY_URL = "https://koviubi56.statuspage.io/api/v2/summary.json"
SCHEDULED_MAINTENANCES = (
    "https://koviubi56.statuspage.io/api/v2/scheduled-maintenances"
    "/upcoming.json"
)
ONGOING_MAINTENANCES = (
    "https://koviubi56.statuspage.io/api/v2/scheduled-maintenances/active.json"
)
ONGOING_INIDENTS = (
    "https://koviubi56.statuspage.io/api/v2/incidents/unresolved.json"
)
COMPONENT_NAME = "YUU8"


class Status(enum.Enum):
    OPERATIONAL = "operational"
    PARTIAL_OUTAGE = "partial_outage"
    MAJOR_OUTAGE = "major_outage"
    DEGRADED_PERFORMANCE = "degraded_performance"
    UNDER_MAINTENANCE = "under_maintenance"


def request(url: str) -> Dict[str, Any]:
    re = requests.get(url)
    re.raise_for_status()
    return re.json()


def get_summary() -> Dict[str, Any]:
    return request(SUMMARY_URL)


def get_summary_for_yuu8() -> Dict[str, Any]:
    summary = get_summary()
    for component in summary["components"]:
        if component["name"] == COMPONENT_NAME:
            return component
    raise RuntimeError("Not found")


def get_status_for_yuu8() -> Status:
    component_summary = get_summary_for_yuu8()
    return Status(component_summary["status"])


def get_scheduled_maintenances() -> List[Dict[str, Any]]:
    return request(SCHEDULED_MAINTENANCES)["scheduled_maintenances"]


def is_there_planned_maintenance() -> Optional[Dict[str, Any]]:
    for maintenance in get_scheduled_maintenances():
        for comp in maintenance["components"]:
            if comp["name"] == COMPONENT_NAME:
                return maintenance
    return None


def planned_maintenance_starts_at() -> Optional[datetime.datetime]:
    ma = is_there_planned_maintenance()
    return datetime.datetime.fromisoformat(ma["scheduled_for"]) if ma else None


def is_there_ongoing_maintenance() -> Optional[Dict[str, Any]]:
    for maintenance in request(ONGOING_MAINTENANCES)["scheduled_maintenances"]:
        for comp in maintenance["components"]:
            if comp["name"] == COMPONENT_NAME:
                return maintenance
    return None


def is_there_ongoing_incident() -> Optional[Dict[str, Any]]:
    for incident in request(ONGOING_INIDENTS)["incidents"]:
        for comp in incident["components"]:
            if comp["name"] == COMPONENT_NAME:
                return incident
    return None


def get_text() -> Optional[Tuple[str, str]]:
    ongoing_incident = is_there_ongoing_incident()
    if ongoing_incident:
        return (
            "**There is an ongoing incident!**",
            f"More information: {ongoing_incident['shortlink']}",
        )
    ongoing_maintenance = is_there_ongoing_maintenance()
    if ongoing_maintenance:
        return (
            "**There is an ongoing maintenance**",
            f"More information: {ongoing_maintenance['shortlink']}",
        )
    planned_maintenance = is_there_planned_maintenance()
    if planned_maintenance:
        return (
            "There is a scheduled maintenance",
            "It starts at"
            f" {planned_maintenance_starts_at().isoformat()}. More"
            f" information: {planned_maintenance['shortlink']}",
        )
    return None
