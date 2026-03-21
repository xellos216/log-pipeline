import argparse
from pathlib import Path

from app.parser import parse_line
from app.validator import validate_log
from app.aggregator import aggregate_logs
from app.reporter import (
    write_summary,
    write_aggregated_csv,
    write_invalid_logs,
    print_cli_summary,
)


def process_log_file(input_path: str, output_dir: str) -> None:
    valid_records = []
    invalid_logs = []

    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_file.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            parsed = parse_line(line, line_number)

            if not parsed["ok"]:
                invalid_logs.append(
                    {
                        "line_number": parsed["line_number"],
                        "raw": parsed["raw"],
                        "error": parsed["error"],
                    }
                )
                continue

            record = parsed["data"]
            is_valid, reason = validate_log(record)

            if not is_valid:
                invalid_logs.append(
                    {
                        "line_number": parsed["line_number"],
                        "raw": parsed["raw"],
                        "error": reason,
                    }
                )
                continue

            valid_records.append(record)

    aggregated = aggregate_logs(valid_records)

    summary_output = {
        "input_file": str(input_file),
        "valid_record_count": len(valid_records),
        "invalid_record_count": len(invalid_logs),
        **aggregated["summary"],
    }

    write_summary(summary_output, output_dir)
    write_aggregated_csv(aggregated, output_dir)
    write_invalid_logs(invalid_logs, output_dir)
    print_cli_summary({"summary": summary_output})


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI log processing pipeline")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input access log file",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Directory to store output files",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    process_log_file(args.input, args.output)


if __name__ == "__main__":
    main()
