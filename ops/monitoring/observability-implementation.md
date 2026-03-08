# Observability implementation checklist

## 1) Structured logging JSON + Correlation/Request ID

Implement middleware/interceptor at **every ingress boundary** (HTTP router, gRPC gateway, queue consumer):

1. Read incoming request ID from `X-Request-ID` or W3C `traceparent`.
2. Generate UUIDv7 request ID if absent.
3. Attach ID to request context and all downstream logs.
4. Return `X-Request-ID` in every response.
5. Log only JSON lines (one event per line).

### Required log fields

| Field | Type | Description |
|---|---|---|
| `timestamp` | RFC3339 | Log time |
| `level` | string | `debug/info/warn/error` |
| `service` | string | Service name |
| `environment` | string | `prod/staging/dev` |
| `request_id` | string | Correlation ID for request |
| `trace_id` | string | OpenTelemetry trace ID |
| `span_id` | string | OpenTelemetry span ID |
| `route` | string | Router template/path |
| `method` | string | HTTP method |
| `status_code` | number | HTTP status |
| `latency_ms` | number | End-to-end latency |
| `user_id` | string/null | Authenticated subject |
| `error_code` | string/null | Domain/system error code |
| `message` | string | Human-readable message |

### JSON log example

```json
{
  "timestamp": "2026-03-07T09:41:42.612Z",
  "level": "info",
  "service": "mokmok-api",
  "environment": "prod",
  "request_id": "0195712e-4c3d-7ec2-b998-36a56d9a4c9f",
  "trace_id": "8f5f4ea07cd3814ecf5f8b22f7cdb590",
  "span_id": "a1d8823a1972ebd4",
  "route": "/v1/orders/{id}",
  "method": "GET",
  "status_code": 200,
  "latency_ms": 37,
  "user_id": "u_912",
  "error_code": null,
  "message": "request completed"
}
```

## 2) Metrics contract

Expose `/metrics` from all services and workers with the following canonical metrics:

- `http_requests_total{service,route,method,status}`
- `http_request_duration_seconds_bucket{service,route,method}` histogram
- `worker_jobs_total{service,queue,status}`
- `queue_consumer_lag_seconds{service,queue}`
- `db_pool_in_use_connections{service,db}`
- `db_pool_idle_connections{service,db}`
- `db_pool_max_connections{service,db}`
- `cache_requests_total{service,cache,result="hit|miss"}`

Derived KPIs are calculated in Prometheus recording rules (`prometheus-rules.yaml`).

## 3) Distributed tracing API -> service -> DB/Redis/worker

- Use OpenTelemetry SDK in every process.
- Propagate W3C context (`traceparent` + `tracestate`) across HTTP, gRPC, and queue headers.
- Add semantic span attributes:
  - HTTP: `http.method`, `url.path`, `http.response.status_code`
  - DB: `db.system`, `db.operation`, `db.statement` (sanitized)
  - Redis: `db.system=redis`, `db.operation`
  - Worker: `messaging.system`, `messaging.destination.name`
- Sample production traces with parent-based ratio (`10%`), while always sampling errors.
- Export OTLP to collector configured in `otel-collector.yaml`.
