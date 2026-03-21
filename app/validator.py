from typing import Dict, Any, Tuple, Optional

ALLOWED_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}


def validate_log(record: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate parsed log record.

    Returns:
        (True, None) if valid
        (False, "reason") if invalid
    """
    required_fields = ["ip", "timestamp", "method", "url", "status_code"]

    for field in required_fields:
        value = record.get(field)
        if value is None or value == "":
            return False, f"missing field: {field}"

    method = record["method"]
    if method not in ALLOWED_METHODS:
        return False, f"invalid method: {method}"

    try:
        status_code = int(record["status_code"])
    except (TypeError, ValueError):
        return False, "status_code is not an integer"

    if not (100 <= status_code <= 599):
        return False, f"status_code out of range: {status_code}"

    response_size = record.get("response_size")
    if response_size is not None:
        try:
            size_int = int(response_size)
        except (TypeError, ValueError):
            return False, "response_size is not an integer"
        if size_int < 0:
            return False, f"negative response_size: {size_int}"

    return True, None
