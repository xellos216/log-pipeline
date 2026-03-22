# Log Processing Pipeline

Big Data Engineer / 데이터 엔지니어 포트폴리오를 위한 최소하지만 실용적인 CLI 기반 로그 처리 프로젝트입니다.

이 프로젝트는 서버 access log를 입력으로 받아 다음 흐름으로 처리합니다.

parse → validate → aggregate → report

즉, 원시 로그를 읽고, 파싱하고, 비정상 데이터를 걸러내고, 유의미한 지표로 집계한 뒤, JSON/CSV 형태로 결과를 저장하는 파이프라인입니다.

---

## Demo

![Log Pipeline Demo](docs/cli-demo.gif)

---

## 1. 프로젝트 목적

실제 운영 환경의 로그는 항상 깨끗하지 않습니다.

이 프로젝트는 다음을 목표로 합니다:

- 반정형 로그 데이터를 구조화
- 비정상 데이터 분리
- 운영 지표 생성
- 분석 가능한 형태로 출력

작지만 실무 로그 파이프라인의 핵심 흐름을 재현합니다.

---

## 2. 주요 기능

### 로그 파싱
- nginx/apache 스타일 로그 파싱
- IP, timestamp, method, URL, status, size 추출

### 데이터 검증
- 형식 오류 탐지
- 필수 필드 검증
- 상태 코드 범위 검사

### 집계 (Aggregation)
- IP별 요청 수
- Endpoint별 요청 수
- 상태 코드별 개수
- 에러율 계산 (4xx, 5xx)
- **Top N IP / Endpoint 분석**
- **시간 단위 요청 수 집계 (Hourly Aggregation)**

### 결과 출력
- summary.json
- aggregated.csv
- invalid_logs.csv
- CLI 출력

---

## 3. 프로젝트 구조

```

log-pipeline/
├── app/
├── data/
├── scripts/
├── out/
├── main.py
├── README.md
├── README_EN.md

````

---

## 4. 실행 방법

### 로그 생성

```bash
python scripts/generate_log.py --output data/access.log --count 1000 --invalid-ratio 0.15
````

### 파이프라인 실행

```bash
python main.py --input data/access.log --output out/
```

---

## 5. 출력 결과

* `summary.json`: 전체 요약 및 에러율
* `aggregated.csv`: 집계 데이터
* `invalid_logs.csv`: 비정상 로그
* `requests_per_hour`: 시간 단위 요청 분포

---

## 6. 샘플 출력

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

## 7. 실무 연결성

이 프로젝트는 다음 시스템의 핵심 전처리 단계를 재현합니다:

* ELK (Elasticsearch, Logstash, Kibana)
* Splunk
* SIEM

---

## 8. 데이터 엔지니어링 관점

이 프로젝트는 다음 역량을 보여줍니다:

* 반정형 데이터 처리
* 데이터 품질 검증
* 집계 및 지표 생성
* Top N 분석
* 시간 기반 분석
* CLI 기반 파이프라인 설계

---

## 9. 설명

이 프로젝트는 반정형 서버 로그를 파싱하고, 잘못된 데이터를 검증 및 분리하며, 운영 지표로 집계한 뒤 분석 가능한 형태로 출력하는 로그 처리 파이프라인입니다.

실제 ELK, Splunk, SIEM에서 수행하는 전처리 과정을 단순화하여 구현했습니다.
