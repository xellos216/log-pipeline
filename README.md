# Log Processing Pipeline

Big Data Engineer / 데이터 엔지니어 포트폴리오를 위한 최소하지만 실용적인 CLI 기반 로그 처리 프로젝트입니다.

이 프로젝트는 서버 access log를 입력으로 받아 다음 흐름으로 처리합니다.

parse → validate → aggregate → report

즉, 원시 로그를 읽고, 파싱하고, 비정상 데이터를 걸러내고, 유의미한 지표로 집계한 뒤, JSON/CSV 형태로 결과를 저장하는 파이프라인입니다.

---

## 1. 프로젝트 목적

실제 운영 환경의 로그는 항상 깨끗하지 않습니다.  
형식이 깨진 로그, 일부 필드가 비정상인 로그, 분석에 바로 쓰기 어려운 원시 로그가 섞여 들어오는 경우가 많습니다.

이 프로젝트의 목적은 이런 로그를 안전하게 처리하여:

- 구조화된 데이터로 변환하고
- 잘못된 로그를 분리하고
- 운영 관점에서 의미 있는 지표를 집계하고
- 후속 분석이나 리포팅에 사용할 수 있는 형태로 저장하는 것

입니다.

작게 만든 프로젝트지만, 실무 로그 파이프라인의 핵심 흐름을 그대로 축약해 보여주는 데 초점을 맞췄습니다.

---

## 2. 이 프로젝트가 다루는 문제

입력 로그 파일에는 다음이 함께 포함될 수 있습니다.

- 정상 로그
- 형식이 깨진 로그
- 잘못된 HTTP 메서드가 들어간 로그
- 비정상 상태 코드가 포함된 로그
- 일부 값이 누락되거나 특수값(`-`)으로 들어온 로그

이 프로젝트는 이러한 입력을 처리하면서 전체 실행이 중단되지 않도록 설계되어 있습니다.

즉, 몇 줄의 오류 때문에 전체 배치가 실패하지 않고:

- 정상 로그는 계속 처리하고
- 비정상 로그는 따로 저장하고
- 최종적으로 전체 요약 결과를 남깁니다

이 점이 실제 데이터 처리 파이프라인과 닮아 있습니다.

---

## 3. 주요 기능

### 3.1 로그 파싱

nginx/apache 스타일 access log 한 줄에서 아래 필드를 추출합니다.

- IP
- timestamp
- method
- URL
- status code
- response size

예시:

```text
127.0.0.1 - - [20/Mar/2026:10:15:32 +0900] "GET /index.html HTTP/1.1" 200 1024
````

---

### 3.2 검증(Validation)

파싱된 로그에 대해 최소한의 데이터 품질 검사를 수행합니다.

검사 항목:

* 로그 형식이 올바른지
* 필수 필드가 존재하는지
* HTTP method가 허용된 값인지
* status code가 정상 범위(100~599)인지
* response size가 숫자인지 또는 허용 가능한 특수값인지

검증 실패 로그는 따로 저장합니다.

---

### 3.3 집계(Aggregation)

정상 로그를 기준으로 다음 지표를 계산합니다.

* IP별 요청 수
* endpoint별 요청 수
* 상태 코드별 개수
* 전체 에러율

  * 4xx 개수
  * 5xx 개수
  * 총 에러 수
  * 전체 요청 대비 에러 비율

---

### 3.4 결과 출력(Reporting)

처리 결과는 다음 파일로 저장됩니다.

* `summary.json`
* `aggregated.csv`
* `invalid_logs.csv`

또한 실행 시 CLI에도 핵심 요약을 출력합니다.

---

## 4. 프로젝트 구조

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

각 파일의 역할은 아래와 같습니다.

* `parser.py`

  * 로그 한 줄을 파싱하여 구조화된 데이터로 변환
* `validator.py`

  * 파싱 결과의 유효성 검사
* `aggregator.py`

  * 정상 로그를 집계하여 지표 생성
* `reporter.py`

  * JSON/CSV 파일 저장 및 CLI 출력
* `main.py`

  * CLI 진입점, 전체 파이프라인 실행

---

## 5. 실행 방법

프로젝트 루트에서 아래와 같이 실행합니다.

```bash
python main.py --input data/access.log --output output/
```

예시:

```bash
python main.py --input data/access.log --output output/
```

실행이 끝나면 `output/` 디렉토리에 결과 파일이 생성됩니다.

---

## 6. 출력 파일 설명

### 6.1 `summary.json`

전체 처리 결과를 요약한 파일입니다.

예시 항목:

* 입력 파일 경로
* 정상 로그 개수
* 비정상 로그 개수
* 총 유효 요청 수
* 4xx 개수
* 5xx 개수
* 총 에러 수
* 에러율

예시:

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

### 6.2 `aggregated.csv`

집계 결과를 CSV 형식으로 저장한 파일입니다.

포함되는 metric:

* `requests_per_ip`
* `requests_per_endpoint`
* `status_code_counts`

예시:

```csv
metric_type,key,value
requests_per_ip,127.0.0.1,2
requests_per_ip,192.168.0.10,3
requests_per_endpoint,/index.html,2
status_code_counts,200,4
status_code_counts,404,1
```

---

### 6.3 `invalid_logs.csv`

처리에 실패한 로그를 저장한 파일입니다.

포함 항목:

* line_number
* raw
* error

예시:

```csv
line_number,raw,error
9,bad line without proper format,invalid format
10,"127.0.0.1 - - [20/Mar/2026:10:20:01 +0900] ""FETCH /weird HTTP/1.1"" 200 100",invalid method: FETCH
12,"10.0.0.5 - - [20/Mar/2026:10:21:00 +0900] ""GET /broken-status HTTP/1.1"" 999 12",status_code out of range: 999
```

---

## 7. 샘플 CLI 출력

예시 실행 결과:

```text
=== Log Processing Summary ===
Total valid requests : 9
4xx errors           : 1
5xx errors           : 1
Total errors         : 2
Error rate           : 22.22%
```

---

## 8. 왜 이 프로젝트가 실무와 맞닿아 있는가

이 프로젝트는 단순한 문자열 처리 연습이 아니라, 실제 로그 처리 시스템의 핵심 단계를 작게 재현한 것입니다.

실무 로그 파이프라인에서도 보통 다음과 같은 문제가 발생합니다.

* 로그 포맷이 완전히 일정하지 않음
* 일부 로그가 깨져 있음
* 잘못된 값이 들어와 있음
* 원시 로그 자체는 바로 분석에 쓰기 어려움
* 집계/모니터링용 지표가 필요함

이 프로젝트는 이런 상황을 가정하고:

* 파싱
* 검증
* 비정상 데이터 분리
* 정상 데이터 집계
* 결과 저장

을 수행합니다.

즉, “원시 운영 데이터”를 “신뢰 가능한 결과물”로 바꾸는 파이프라인의 최소 단위를 보여줍니다.

---

## 9. Splunk와의 관련성

Splunk는 로그 같은 machine data를 수집하고, 필드를 추출하고, 검색/분석할 수 있게 해주는 플랫폼입니다.

이 프로젝트는 Splunk 전체를 구현하는 것은 아니지만, 그 이전 혹은 내부 핵심 단계와 직접 닿아 있습니다.

공통점은 다음과 같습니다.

* 원시 로그 입력
* 필드 추출
* 데이터 정리
* 비정상 데이터 처리
* 집계 결과 생성

즉, 이 프로젝트는 Splunk가 다루는 로그 데이터의 “기초 전처리 및 구조화 과정”을 직접 구현한 형태라고 볼 수 있습니다.

---

## 10. ELK와의 관련성

ELK(Elasticsearch, Logstash, Kibana)는 대표적인 로그 처리/검색/시각화 스택입니다.

이 프로젝트와의 대응 관계는 다음처럼 볼 수 있습니다.

* `parser.py`

  * Logstash의 grok parsing 같은 역할
* `validator.py`

  * 데이터 품질 검사 및 필터링
* `aggregator.py`

  * 집계 및 분석용 기초 지표 생성
* `reporter.py`

  * 최종 결과를 저장하여 후속 활용 가능하게 만듦

즉, 이 프로젝트는 ELK 전체 스택의 대체물이 아니라, ELK 파이프라인에서 중요한 “전처리와 집계” 구간을 Python CLI로 단순화한 버전입니다.

---

## 11. SIEM 시스템과의 관련성

SIEM(Security Information and Event Management)은 여러 시스템의 로그를 수집하고, 분석하고, 이상 징후나 보안 이벤트를 탐지하는 데 사용됩니다.

하지만 SIEM이 동작하기 위해서는 먼저 로그가:

* 읽을 수 있는 구조여야 하고
* 필드가 분리되어 있어야 하며
* 비정상 데이터가 정리되어 있어야 합니다

이 프로젝트는 바로 그 기초 작업을 수행합니다.

즉, 보안 분석 그 자체를 하는 것은 아니지만, SIEM이 의존하는 “정형화된 로그 데이터 준비 과정”을 보여줍니다.

---

## 12. 왜 이 프로젝트가 데이터 엔지니어링 역량을 보여주는가

이 프로젝트는 단순 스크립트보다 데이터 엔지니어링에 더 가까운 이유가 있습니다.

### 12.1 반정형 데이터 처리

로그는 CSV처럼 깔끔한 정형 데이터가 아니라, 텍스트 기반의 반정형 데이터입니다.
이 프로젝트는 그런 데이터를 파싱해서 구조화합니다.

### 12.2 데이터 품질 처리

실제 데이터는 깨져 있거나 잘못된 값이 섞여 있습니다.
이 프로젝트는 invalid 데이터를 분리하고, 정상 데이터만 downstream 처리합니다.

### 12.3 집계와 지표 생성

원시 데이터는 그대로는 가치가 낮습니다.
IP별 요청 수, endpoint별 요청 수, 에러율 같은 지표를 만들어야 운영 관점에서 의미가 생깁니다.

### 12.4 재현 가능한 CLI 파이프라인

CLI 기반으로 동일한 입력에 대해 반복 가능하게 실행할 수 있습니다.
이는 배치 작업, 운영 스크립트, 자동화 파이프라인의 기본 성격과 맞닿아 있습니다.

### 12.5 기계 친화적 출력

결과를 JSON/CSV로 저장하므로 다른 시스템이나 후속 분석에서 활용하기 쉽습니다.

---

## 13. 사용 기술

* Python
* 표준 라이브러리만 사용

  * `re`
  * `csv`
  * `json`
  * `argparse`
  * `pathlib`

프레임워크 없이 구현하여 구조를 단순하게 유지했습니다.

---

## 14. 입력 데이터 예시

샘플 로그 파일에는 정상 로그와 비정상 로그가 함께 포함됩니다.

예시:

```text
127.0.0.1 - - [20/Mar/2026:10:15:32 +0900] "GET /index.html HTTP/1.1" 200 1024
192.168.0.10 - - [20/Mar/2026:10:16:01 +0900] "POST /login HTTP/1.1" 302 512
bad line without proper format
127.0.0.1 - - [20/Mar/2026:10:20:01 +0900] "FETCH /weird HTTP/1.1" 200 100
```

이런 식으로 정상/비정상 케이스를 함께 처리하는 것이 포인트입니다.

---

## 15. 확장 가능 포인트

현재 버전은 의도적으로 최소 기능만 포함합니다.
다만 아래 기능은 이후 자연스럽게 확장할 수 있습니다.

* 시간대별 요청 수 집계
* top N endpoint 출력
* gzip 로그 처리
* SQLite/PostgreSQL 저장
* Bash 스케줄링 연동
* 간단한 이상 요청 탐지
* 다중 로그 파일 처리

하지만 포트폴리오 1차 버전에서는 지금 정도가 더 적절합니다.
구조가 단순하고, 요구사항과 실무 연결성이 분명하기 때문입니다.

---

## 16. 정리

이 프로젝트는 작은 규모지만 다음 역량을 명확하게 보여줍니다.

* 텍스트 기반 로그 파싱
* 데이터 검증 및 예외 처리
* 집계 로직 구현
* 결과 파일 생성
* CLI 기반 파이프라인 설계
* 실무 로그 시스템과의 연결 이해

운영 데이터 처리 흐름을 이해하고 구현할 수 있음을 보여주는 포트폴리오 프로젝트입니다.

---

## 샘플 로그 생성기

테스트용 샘플 로그를 생성할 수 있습니다:

```bash
python scripts/generate_logs.py --output data/access.log --count 1000```
