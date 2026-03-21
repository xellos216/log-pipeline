from collections import Counter
from typing import List, Dict, Any


def aggregate_logs(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    ip_counter = Counter()
    endpoint_counter = Counter()
    status_counter = Counter()

    total_requests = 0
    client_error_count = 0  # 4xx
    server_error_count = 0  # 5xx

    for record in records:
        ip = record["ip"]
        url = record["url"]
        status_code = int(record["status_code"])

        ip_counter[ip] += 1
        endpoint_counter[url] += 1
        status_counter[status_code] += 1

        total_requests += 1

        if 400 <= status_code <= 499:
            client_error_count += 1
        elif 500 <= status_code <= 599:
            server_error_count += 1

    total_error_count = client_error_count + server_error_count
    error_rate = (total_error_count / total_requests) if total_requests else 0.0

    return {
        "summary": {
            "total_valid_requests": total_requests,
            "client_error_count_4xx": client_error_count,
            "server_error_count_5xx": server_error_count,
            "total_error_count": total_error_count,
            "error_rate": round(error_rate, 4),
        },
        "requests_per_ip": dict(ip_counter),
        "requests_per_endpoint": dict(endpoint_counter),
        "status_code_counts": dict(status_counter),
    }
