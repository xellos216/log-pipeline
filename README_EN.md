# Log Processing Pipeline

A minimal but practical CLI-based log processing project designed for a Big Data Engineer / Data Engineering portfolio.

This project processes server access logs through the following pipeline:

parse → validate → aggregate → report

It reads raw logs, extracts structured data, filters invalid records, computes useful metrics, and outputs results in JSON and CSV formats.

---

## 1. Purpose

In real-world systems, logs are rarely clean.

You often encounter:
- malformed lines
- missing fields
- invalid values
- inconsistent formats

The goal of this project is to:

- safely process raw logs
- separate invalid data
- transform logs into structured records
- generate meaningful operational metrics
- produce outputs suitable for further analysis

This project intentionally keeps the implementation minimal while reflecting real production pipeline behavior.

---

## 2. Problem This Project Solves

The input log file may contain:

- valid log entries
- malformed lines
- invalid HTTP methods
- out-of-range status codes
- missing or special values (e.g. `-`)

The system is designed so that:

- processing does not stop on errors
- invalid logs are isolated
- valid logs continue through the pipeline
- final outputs are always produced

This mirrors real-world batch and streaming log processing systems.

---

## 3. Features

### 3.1 Log Parsing

Parses nginx/apache-style access logs and extracts:

- IP address
- timestamp
- HTTP method
- URL
- status code
- response size

Example:

```text
127.0.0.1 - - [20/Mar/2026:10:15:32 +0900] "GET /index.html HTTP/1.1" 200 1024
````

---

### 3.2 Validation

Performs basic data quality checks:

* correct log format
* required fields present
* valid HTTP methods
* status code in range (100–599)
* response size is numeric or allowed special value

Invalid records are stored separately.

---

### 3.3 Aggregation

Generates operational metrics:

* requests per IP
* requests per endpoint
* status code counts
* error rate

  * 4xx count
  * 5xx count
  * total errors
  * error ratio

---

### 3.4 Reporting

Outputs results to:

* `summary.json`
* `aggregated.csv`
* `invalid_logs.csv`

Also prints a summary to the CLI.

---

## 4. Project Structure

```text
log-pipeline/
├── app/
│   ├── __init__.py
│   ├── parser.py
│   ├── validator.py
│   ├── aggregator.py
│   └── reporter.py
├── data/
│   └── access.log
├── output/
├── main.py
└── README.md
```

---

## 5. Usage

Run from the project root:

```bash
python main.py --input data/access.log --output output/
```

---

## 6. Output Files

### 6.1 summary.json

Contains high-level pipeline results:

* input file
* valid record count
* invalid record count
* total requests
* 4xx errors
* 5xx errors
* total errors
* error rate

Example:

```json
{
  "input_file": "data/access.log",
  "valid_record_count": 9,
  "invalid_record_count": 3,
  "total_valid_requests": 9,
  "client_error_count_4xx": 1,
  "server_error_count_5xx": 1,
  "total_error_count": 2,
  "error_rate": 0.2222
}
```

---

### 6.2 aggregated.csv

Stores aggregated metrics in flat format:

```csv
metric_type,key,value
requests_per_ip,127.0.0.1,2
requests_per_endpoint,/index.html,2
status_code_counts,200,4
```

---

### 6.3 invalid_logs.csv

Stores invalid records:

```csv
line_number,raw,error
9,bad line without proper format,invalid format
10,...,invalid method
```

---

## 7. Example CLI Output

```text
=== Log Processing Summary ===
Total valid requests : 9
4xx errors           : 1
5xx errors           : 1
Total errors         : 2
Error rate           : 22.22%
```

---

## 8. Real-World Relevance

This project reflects the core workflow of real log pipelines:

* ingest raw logs
* parse fields
* validate data quality
* filter invalid data
* aggregate metrics
* output structured results

In production systems, this logic typically exists inside larger platforms, but the core concepts remain the same.

---

## 9. Relation to Splunk

Splunk processes machine data by:

* ingesting logs
* extracting fields
* enabling search and analysis

This project replicates the early-stage workflow:

* raw log ingestion
* field extraction
* validation
* aggregation

It demonstrates how raw logs become structured, queryable data.

---

## 10. Relation to ELK (Elasticsearch, Logstash, Kibana)

Mapping of components:

* `parser.py` → Logstash parsing (grok)
* `validator.py` → data filtering / cleaning
* `aggregator.py` → basic analytics
* `reporter.py` → structured output for indexing or visualization

This project is a simplified CLI version of a typical ELK preprocessing pipeline.

---

## 11. Relation to SIEM Systems

SIEM systems rely on:

* structured logs
* validated data
* consistent fields

Before security analysis can happen, logs must be:

* parsed
* cleaned
* normalized

This project demonstrates that foundational step.

---

## 12. Why This Demonstrates Data Engineering Skills

This project shows:

### 12.1 Semi-structured data processing

Logs are not fully structured; parsing is required.

### 12.2 Data quality handling

Invalid data is detected and isolated without breaking the pipeline.

### 12.3 Metric generation

Raw logs are transformed into meaningful operational metrics.

### 12.4 Reproducible pipeline

CLI-based execution enables repeatable processing.

### 12.5 Machine-friendly outputs

JSON and CSV outputs enable downstream usage.

These are core aspects of real data engineering workflows.

---

## 13. Tech Stack

* Python
* Standard library only:

  * `re`
  * `csv`
  * `json`
  * `argparse`
  * `pathlib`

No frameworks are used to keep the design minimal and transparent.

---

## 14. Sample Input

Example mixed log data:

```text
127.0.0.1 - - [20/Mar/2026:10:15:32 +0900] "GET /index.html HTTP/1.1" 200 1024
192.168.0.10 - - [20/Mar/2026:10:16:01 +0900] "POST /login HTTP/1.1" 302 512
bad line without proper format
127.0.0.1 - - [20/Mar/2026:10:20:01 +0900] "FETCH /weird HTTP/1.1" 200 100
```

---

## 15. Possible Extensions

Keep the base project minimal, but realistic extensions include:

* time-based aggregation (hour/day)
* top-N endpoints
* gzip log support
* database output (SQLite/PostgreSQL)
* batch scheduling via Bash
* anomaly detection (e.g. suspicious IPs)

---

## 16. Summary

This project demonstrates the ability to:

* parse and process raw logs
* handle invalid data safely
* generate aggregated metrics
* build a CLI-based pipeline
* produce structured outputs
* understand real-world logging systems

It is not just a script, but a simplified model of a real log processing pipeline.

--

## Generating Sample Logs

You can generate test logs using:

```bash
python scripts/generate_logs.py --output data/access.log --count 1000
```
