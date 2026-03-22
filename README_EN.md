# Log Processing Pipeline

A minimal but practical CLI-based log processing pipeline for a Data Engineering portfolio.

This project processes server logs through:

parse → validate → aggregate → report

---

## Demo

![Log Pipeline Demo](docs/cli-demo.gif)

---

## 1. Purpose

Logs in real systems are often messy and inconsistent.

This project aims to:

- structure semi-structured logs
- filter invalid data
- generate meaningful metrics
- output analysis-ready results

---

## 2. Features

### Parsing
- nginx/apache log parsing
- extract IP, timestamp, method, URL, status, size

### Validation
- detect malformed logs
- validate required fields
- check status code range

### Aggregation
- requests per IP
- requests per endpoint
- status code counts
- error rate (4xx, 5xx)
- **Top N IP / Endpoint analysis**
- **Hourly aggregation (time-based analysis)**

### Output
- summary.json
- aggregated.csv
- invalid_logs.csv
- CLI output

---

## 3. Project Structure

````

log-pipeline/
├── app/
├── data/
├── scripts/
├── out/
├── main.py

````

---

## 4. Usage

### Generate logs

```bash
python scripts/generate_log.py --output data/access.log --count 1000 --invalid-ratio 0.15
````

### Run pipeline

```bash
python main.py --input data/access.log --output out/
```

---

## 5. Output

* `summary.json`: pipeline summary and error rate
* `aggregated.csv`: aggregated metrics
* `invalid_logs.csv`: invalid records
* `requests_per_hour`: hourly request distribution

---

## 6. Example Output

```
=== Log Processing Summary ===
Total valid requests : 847
Error rate           : 64.94%

Top 5 IPs:
...

Top 5 Endpoints:
...

Requests Per Hour:
2026-03-20 10:00: 847
```

---

## 7. Real-World Relevance

This project simulates the preprocessing layer of:

* ELK
* Splunk
* SIEM systems

---

## 8. Data Engineering Perspective

This project demonstrates:

* semi-structured data processing
* data validation
* aggregation and metrics
* Top N analysis
* time-based analysis
* CLI pipeline design

---

## 9. Interview Explanation

This project demonstrates a practical log processing pipeline: parsing semi-structured logs, validating data, aggregating metrics, and performing time-based analysis.

It reflects the core preprocessing layer used in ELK, Splunk, and SIEM systems.
