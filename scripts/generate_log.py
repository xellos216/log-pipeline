import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path


METHODS = ["GET", "POST", "PUT", "DELETE"]
INVALID_METHODS = ["FETCH", "INVALID"]

URLS = [
    "/",
    "/index.html",
    "/login",
    "/dashboard",
    "/api/users",
    "/api/orders",
    "/health",
]

STATUS_CODES = [200, 201, 302, 400, 401, 403, 404, 500, 502]
INVALID_STATUS_CODES = [99, 999]

IPS = [
    "127.0.0.1",
    "192.168.0.10",
    "10.0.0.5",
    "172.16.1.20",
    "8.8.8.8",
]


def random_timestamp():
    base = datetime(2026, 3, 20, 10, 0, 0)
    delta = timedelta(seconds=random.randint(0, 3600))
    ts = base + delta
    return ts.strftime("%d/%b/%Y:%H:%M:%S +0900")


def generate_valid_log():
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    url = random.choice(URLS)
    status = random.choice(STATUS_CODES)
    size = random.randint(100, 5000)

    return f'{ip} - - [{random_timestamp()}] "{method} {url} HTTP/1.1" {status} {size}'


def generate_invalid_log():
    choice = random.choice(["format", "method", "status"])

    if choice == "format":
        return "this is not a valid log line"

    elif choice == "method":
        ip = random.choice(IPS)
        method = random.choice(INVALID_METHODS)
        url = random.choice(URLS)
        status = 200
        size = 100
        return (
            f'{ip} - - [{random_timestamp()}] "{method} {url} HTTP/1.1" {status} {size}'
        )

    elif choice == "status":
        ip = random.choice(IPS)
        method = random.choice(METHODS)
        url = random.choice(URLS)
        status = random.choice(INVALID_STATUS_CODES)
        size = 100
        return (
            f'{ip} - - [{random_timestamp()}] "{method} {url} HTTP/1.1" {status} {size}'
        )


def generate_logs(count: int, invalid_ratio: float):
    logs = []

    for _ in range(count):
        if random.random() < invalid_ratio:
            logs.append(generate_invalid_log())
        else:
            logs.append(generate_valid_log())

    return logs


def main():
    parser = argparse.ArgumentParser(description="Generate sample access logs")
    parser.add_argument("--output", required=True, help="Output log file path")
    parser.add_argument("--count", type=int, default=100, help="Number of logs")
    parser.add_argument(
        "--invalid-ratio", type=float, default=0.1, help="Ratio of invalid logs"
    )

    args = parser.parse_args()

    logs = generate_logs(args.count, args.invalid_ratio)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for line in logs:
            f.write(line + "\n")

    print(f"Generated {len(logs)} logs → {output_path}")


if __name__ == "__main__":
    main()
