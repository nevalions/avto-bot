import dataclasses
import json
from datetime import datetime


class SQLJsonEncoder(json.JSONEncoder):  # <<-- Add this custom encoder
    """Custom JSON encoder for the DB class."""

    def default(self, o):
        if dataclasses.is_dataclass(o):  # this serializes anything dataclass can handle
            return dataclasses.asdict(o)
        if isinstance(o, datetime):  # this adds support for datetime
            return o.isoformat()
        return super().default(o)
