import csv
import json
from pathlib import Path
from typing import Dict, Any, List


def ensure_output_dir(output_dir: str) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_summary(summary: Dict[str, Any], output_dir: str) -> None:
    out_dir = ensure_output_dir(output_dir)
    summary_path = out_dir / "summary.json"

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)


def write_aggregated_csv(aggregated: Dict[str, Any], output_dir: str) -> None:
    out_dir = ensure_output_dir(output_dir)
    csv_path = out_dir / "aggregated.csv"

    rows = []

    for key, value in aggregated["requests_per_ip"].items():
        rows.append({"metric_type": "requests_per_ip", "key": key, "value": value})

    for key, value in aggregated["requests_per_endpoint"].items():
        rows.append(
            {"metric_type": "requests_per_endpoint", "key": key, "value": value}
        )

    for key, value in aggregated["status_code_counts"].items():
        rows.append({"metric_type": "status_code_counts", "key": key, "value": value})

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric_type", "key", "value"])
        writer.writeheader()
        writer.writerows(rows)


def write_invalid_logs(invalid_logs: List[Dict[str, Any]], output_dir: str) -> None:
    out_dir = ensure_output_dir(output_dir)
    csv_path = out_dir / "invalid_logs.csv"

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["line_number", "raw", "error"])
        writer.writeheader()
        writer.writerows(invalid_logs)


def print_cli_summary(result: Dict[str, Any]) -> None:
    summary = result["summary"]

    print("=== Log Processing Summary ===")
    print(f"Total valid requests : {summary['total_valid_requests']}")
    print(f"4xx errors           : {summary['client_error_count_4xx']}")
    print(f"5xx errors           : {summary['server_error_count_5xx']}")
    print(f"Total errors         : {summary['total_error_count']}")
    print(f"Error rate           : {summary['error_rate']:.2%}")

    print("\nTop 5 IPs:")
    for ip, count in result.get("top_ips", []):
        print(f"  {ip}: {count}")

    print("\nTop 5 Endpoints:")
    for endpoint, count in result.get("top_endpoints", []):
        print(f"  {endpoint}: {count}")

    print("\nRequests Per Hour:")
    for hour, count in result.get("requests_per_hour", {}).items():
        print(f"  {hour}: {count}")
