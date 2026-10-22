"""Date helpers for a scheduling tool."""
from datetime import datetime, timezone


def parse_date(text: str) -> datetime:
    """Parse an ISO 8601 timestamp such as 2026-10-22T09:00:00+02:00 into UTC.

    Returns a timezone-aware datetime in UTC. A timestamp without an offset is UTC.
    """
    moment = datetime.fromisoformat(text)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)
