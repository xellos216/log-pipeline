import re
from typing import Dict, Any

LOG_PATTERN = re.compile(
    r"^(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+"
    r'"(?P<method>[A-Z]+)\s+(?P<url>\S+)\s+(?P<protocol>[^"]+)"\s+'
    r"(?P<status>\d{3})\s+(?P<size>\S+)$"
)


def parse_line(line: str, line_number: int) -> Dict[str, Any]:
    """
    Parse a single access log line.

    Returns:
        {
            "ok": True,
            "data": {...},
            "error": None
        }
        or
        {
            "ok": False,
            "data": None,
            "error": "reason"
        }
    """
    raw = line.rstrip("\n")

    if not raw.strip():
        return {
            "ok": False,
            "data": None,
            "error": "empty line",
            "raw": raw,
            "line_number": line_number,
        }

    match = LOG_PATTERN.match(raw)
    if not match:
        return {
            "ok": False,
            "data": None,
            "error": "invalid format",
            "raw": raw,
            "line_number": line_number,
        }

    groups = match.groupdict()

    size_value = groups["size"]
    # nginx/apache logs sometimes use "-" when size is missing
    if size_value == "-":
        size_value = None

    parsed = {
        "ip": groups["ip"],
        "timestamp": groups["timestamp"],
        "method": groups["method"],
        "url": groups["url"],
        "status_code": groups["status"],
        "response_size": size_value,
    }

    return {
        "ok": True,
        "data": parsed,
        "error": None,
        "raw": raw,
        "line_number": line_number,
    }
