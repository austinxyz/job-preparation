---
title: Python for Infrastructure
category: tech/software-eng
tags: [python, scripting, automation, devops, infrastructure-tooling, kubernetes, boto3, asyncio, pytest, operator]
status: in-progress
priority: high
last_updated: 2026-04-11
created_from_jd: "[[positions/Manager, DevOps Engineering - NVIDIA]]"
---

# Python for Infrastructure

## Knowledge Map
- 前置知识：Python basics, shell scripting, REST APIs, Kubernetes concepts
- 延伸话题：[[Kubernetes]], [[AWS Infrastructure]], [[CI-CD Pipeline Engineering]], [[LLMOps and AI Pipeline Engineering]]
- 管理关联：automation strategy, build-vs-buy tooling decisions, team skill requirements, platform engineering

## Core Concepts

### Why Python for Infrastructure

Python is the dominant glue language for infrastructure automation because:
- Rich ecosystem of cloud/infra SDKs (boto3, kubernetes client, google-cloud, azure-sdk)
- Readable syntax makes infrastructure-as-code reviewable by engineers who aren't primarily Python developers
- Strong typing via `typing` module and mypy — catches bugs before execution in long-running automation
- Fast iteration: scripting speed with the ability to grow into production-grade tooling
- Dominant language in AI/ML infra — PyTorch, TensorFlow, Ray, Airflow, Kubeflow are all Python-first

### Core Use Cases

| Use case | Key libraries | Typical task |
|---|---|---|
| Cloud automation | `boto3`, `google-cloud-*`, `azure-sdk` | Provision/manage cloud resources, auto-scaling, cost analysis |
| Kubernetes automation | `kubernetes` (k8s Python client) | Manage resources, build operators/controllers, custom tooling |
| Configuration management | `ansible` (Python-based), `fabric` | Remote execution, fleet config, server provisioning |
| CI/CD tooling | `requests`, `subprocess`, `GitPython` | Pipeline scripts, webhook handlers, release automation |
| Observability / alerting | `prometheus_client`, `datadog`, custom | Metric emission, alert rule management, SLO calculation |
| Infrastructure testing | `pytest`, `moto` (AWS mock), `pytest-kubernetes` | Test automation scripts, validate infra behavior |
| AI/ML infra | `ray`, `airflow`, `prefect`, `mlflow` | Training orchestration, pipeline DAGs, experiment tracking |

### Kubernetes Python Client

The official `kubernetes` Python client mirrors the Kubernetes API:

```python
from kubernetes import client, config, watch

# Load kubeconfig (or in-cluster config for operators)
config.load_incluster_config()   # inside a pod
config.load_kube_config()        # local dev

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
custom = client.CustomObjectsApi()

# List pods across namespaces
pods = v1.list_pod_for_all_namespaces(watch=False)

# Watch events (streaming)
w = watch.Watch()
for event in w.stream(v1.list_namespaced_pod, namespace="default"):
    print(f"{event['type']} {event['object'].metadata.name}")

# Patch a deployment
apps_v1.patch_namespaced_deployment(
    name="my-app",
    namespace="default",
    body={"spec": {"replicas": 3}}
)

# Create a CRD instance (Custom Object)
custom.create_namespaced_custom_object(
    group="myorg.io", version="v1", namespace="default",
    plural="myresources", body={...}
)
```

**Key patterns in platform engineering:**
- `watch.Watch()` for event-driven reconciliation loops (operator pattern)
- `list_*_with_http_info()` for pagination via `continue` token on large clusters
- Field selectors and label selectors to scope API calls — avoid `list_pod_for_all_namespaces` on large clusters without filters
- `dry_run="All"` parameter for safe validation before applying changes

### Building K8s Operators in Python (kopf)

`kopf` (Kubernetes Operator Pythonic Framework) is the standard Python framework for writing operators:

```python
import kopf
import kubernetes

@kopf.on.create('myorg.io', 'v1', 'myresources')
def on_create(spec, name, namespace, **kwargs):
    # Called when a MyResource CR is created
    api = kubernetes.client.CoreV1Api()
    api.create_namespaced_config_map(
        namespace=namespace,
        body=kubernetes.client.V1ConfigMap(
            metadata=kubernetes.client.V1ObjectMeta(name=f"{name}-config"),
            data={"key": spec.get("value", "default")}
        )
    )

@kopf.on.update('myorg.io', 'v1', 'myresources')
def on_update(spec, old, new, **kwargs):
    # Reconcile on spec change
    pass

@kopf.on.delete('myorg.io', 'v1', 'myresources')
def on_delete(name, namespace, **kwargs):
    # Cleanup
    pass
```

vs. controller-runtime (Go): kopf is faster to prototype, Go is better for production operators at high event volume.

### AWS Automation with boto3

```python
import boto3
from botocore.exceptions import ClientError

# Session with explicit region/profile
session = boto3.Session(region_name='us-east-1')
ec2 = session.client('ec2')
s3 = session.resource('s3')

# Paginator for large result sets (essential — never assume single-page response)
paginator = ec2.get_paginator('describe_instances')
for page in paginator.paginate(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]):
    for reservation in page['Reservations']:
        for instance in reservation['Instances']:
            print(instance['InstanceId'])

# Waiter — block until resource reaches desired state
ec2.get_waiter('instance_running').wait(InstanceIds=['i-1234567890abcdef0'])

# Error handling
try:
    s3.Object('my-bucket', 'key').get()
except ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchKey':
        print("Object not found")
    else:
        raise
```

**Key boto3 patterns:**
- Always use **paginators** for list operations — AWS APIs are paginated, direct calls only return first page
- Use **waiters** instead of polling loops — they implement exponential backoff correctly
- Use **resource** interface (higher-level) for simple operations; **client** interface for full API access
- **Assume role** pattern for cross-account access: `sts.assume_role()` → temporary credentials → new session

### Async Python for Infrastructure

`asyncio` is essential when managing many concurrent infra operations (parallel API calls, webhook handlers, health checkers):

```python
import asyncio
import aiohttp

async def check_endpoint(session, url):
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
        return url, resp.status

async def health_check_fleet(endpoints: list[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [check_endpoint(session, url) for url in endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Run
results = asyncio.run(health_check_fleet(["https://svc-1/health", "https://svc-2/health"]))
```

Use async when: many concurrent I/O-bound operations (HTTP calls, K8s API calls, DB queries).
Don't use async when: CPU-bound work (use `multiprocessing`), simple sequential scripts.

**Kubernetes async client**: use `kubernetes_asyncio` package for async K8s API calls in operator watch loops.

### Infrastructure Testing with pytest

```python
import pytest
import boto3
from moto import mock_aws   # AWS mocking library

@mock_aws
def test_creates_s3_bucket():
    s3 = boto3.client('s3', region_name='us-east-1')
    from my_infra_module import create_bucket
    create_bucket('test-bucket')
    buckets = [b['Name'] for b in s3.list_buckets()['Buckets']]
    assert 'test-bucket' in buckets

# Fixture for K8s testing (pytest-kubernetes or manual)
@pytest.fixture
def k8s_client():
    from kubernetes import client, config
    config.load_kube_config(config_file='test-kubeconfig')
    return client.CoreV1Api()

def test_pod_has_resource_limits(k8s_client):
    pods = k8s_client.list_namespaced_pod(namespace='default').items
    for pod in pods:
        for container in pod.spec.containers:
            assert container.resources.limits is not None, \
                f"Pod {pod.metadata.name} has no resource limits"
```

**Testing infrastructure code:**
- `moto` for AWS — mocks boto3 calls without hitting real AWS
- `responses` library for mocking HTTP calls
- `pytest-kubernetes` or kind/k3d for real K8s integration tests
- Separate unit tests (fast, mocked) from integration tests (real infra, slower)

### Python for AI/ML Infrastructure

Python is the native language for AI infra tooling:

**Training orchestration:**
```python
import ray
ray.init()

@ray.remote(num_gpus=1)
def train_model(config):
    # Runs on a worker with 1 GPU
    return train(config)

futures = [train_model.remote(cfg) for cfg in configs]
results = ray.get(futures)
```

**Pipeline DAGs (Airflow):**
```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(schedule='@daily', start_date=datetime(2025, 1, 1))
def ml_pipeline():
    @task
    def validate_data():
        # Data quality checks
        return {"rows": 1000000, "valid": True}

    @task
    def train(data_stats: dict):
        # Trigger training job
        pass

    @task
    def evaluate(model_path: str):
        # Model evaluation
        pass

    stats = validate_data()
    model = train(stats)
    evaluate(model)

dag = ml_pipeline()
```

**Model serving health check:**
```python
import httpx
from prometheus_client import Gauge, start_http_server

MODEL_LATENCY = Gauge('model_inference_latency_ms', 'P99 inference latency', ['model_version'])

async def probe_model_server(endpoint: str, model_version: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{endpoint}/predict", json={"input": PROBE_INPUT})
        MODEL_LATENCY.labels(model_version=model_version).set(resp.elapsed.total_seconds() * 1000)
```

### Python vs. Go for Infrastructure — When to Use Which

Kubernetes is written in Go, and the official operator framework (`controller-runtime`) is Go-first. Understanding where Go wins and where Python wins is a core infrastructure engineering judgment call.

#### Language Characteristics Comparison

| Dimension | Python | Go |
|---|---|---|
| **Iteration speed** | Fast — no compile step, REPL, dynamic typing | Slower — compile required, static typing |
| **Runtime performance** | Slower, higher memory usage, GIL limits true parallelism | Fast, low memory, native goroutines for true concurrency |
| **K8s ecosystem fit** | Official client, kopf — functional but second-class | Native — controller-runtime, kubebuilder, operator-sdk |
| **Type safety** | Optional (mypy) — easy to skip, runtime errors possible | Enforced at compile time — no type errors reach production |
| **Deployment** | Requires Python runtime, dependency management (pip/poetry) | Single static binary — easy to distribute, no runtime deps |
| **AI/ML ecosystem** | Native — PyTorch, Ray, Airflow are all Python-first | Limited — no equivalent ML ecosystem |
| **Error handling** | Exceptions — easy to miss, can be silently swallowed | Explicit `(value, error)` return — forces handling at every call site |
| **Concurrency** | asyncio (cooperative), multiprocessing for CPU | Goroutines — lightweight, true parallelism, built into language |
| **Team familiarity** | More engineers know Python | Go is less common outside infra/backend |

#### K8s Operator: Python (kopf) vs Go (controller-runtime)

This is the most concrete comparison point for platform engineering:

**Go controller-runtime strengths:**
- **Informers and caching**: built-in API object cache reduces API server load at scale — watch events are served from local cache, not direct API calls
- **Work queue**: built-in rate limiting, retries, and queue deduplication — handles event storms gracefully
- **Lower latency reconciliation**: compiled, no GC pauses from Python interpreter
- **First-class kubebuilder scaffolding**: `kubebuilder create api` generates CRD scaffolding, RBAC manifests, webhook boilerplate
- **Memory efficiency**: Go operators handling thousands of objects use far less memory than equivalent Python

**Python kopf strengths:**
- **Development speed**: new operator from scratch in 30 minutes, vs. hours with Go boilerplate
- **Richer Python ecosystem in handlers**: easy to call boto3, send Slack notifications, query Prometheus — no need to find Go equivalents
- **Lower barrier for ML/data teams**: ML engineers who know Python can contribute to operators
- **Prototyping**: validate the operator logic before committing to Go implementation

**Decision rule:**
- Operator handles < ~1,000 objects, event rate is low → Python/kopf is fine
- Operator is system-critical, handles many objects, or is a long-term platform investment → Go/controller-runtime
- eBay Federated Deployment Controller: Go — handles all clusters (high event volume, system-critical)

#### When Go Wins Clearly

1. **Production Kubernetes operators at scale** — informer cache, work queue, kubebuilder are mature and battle-tested
2. **CLI tools** — single binary distribution, `cobra` framework, fast startup
3. **Network proxies / data plane components** — Envoy filters, custom CNI plugins, service mesh sidecar logic
4. **High-throughput API servers** — Go HTTP servers handle significantly more concurrent connections than Python (no GIL)
5. **Any component that runs inside the critical path** of production traffic

#### When Python Wins Clearly

1. **AI/ML infrastructure** — no alternative; Ray, Airflow, PyTorch, MLflow are Python-only
2. **Cloud automation scripts and tooling** — boto3, google-cloud, azure-sdk; faster to write and iterate
3. **Internal platform tooling** (dashboards, schedulers, report generators) — not performance-critical
4. **Operator prototyping** — validate CRD design and reconciliation logic before Go implementation
5. **Data pipelines** — Spark (PySpark), Pandas, dbt (Python models), Prefect

#### Pragmatic Hybrid Approach (used at eBay)

Write the automation/tooling layer in Python; implement production operators and controllers in Go. Python scripts call the K8s API for operational tasks (bulk updates, migrations, health sweeps); Go operators handle the continuous reconciliation loop. This plays to each language's strengths without forcing an artificial choice.

```
Python scripts ──► K8s API ──► CRDs managed by Go operators
     ↑                              ↑
  boto3 / cloud SDK            controller-runtime
  AI/ML pipeline calls         informer cache
  operational tooling          work queue
```



**Type hints (mandatory for infra tooling):**
```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class ClusterConfig:
    name: str
    region: str
    node_count: int
    spot_enabled: bool = False
    tags: dict[str, str] = None

def provision_cluster(config: ClusterConfig) -> str:
    """Returns cluster ID."""
    ...
```

**Retry with exponential backoff:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type(TransientError)
)
def call_flaky_api():
    ...
```

**Context managers for resource cleanup:**
```python
from contextlib import contextmanager

@contextmanager
def temp_namespace(k8s_client, name: str):
    k8s_client.create_namespace(V1Namespace(metadata=V1ObjectMeta(name=name)))
    try:
        yield name
    finally:
        k8s_client.delete_namespace(name)

# Usage
with temp_namespace(client, "test-ns") as ns:
    # run tests in isolated namespace
    pass  # namespace auto-deleted
```

**Structured logging (not print statements):**
```python
import structlog

log = structlog.get_logger()
log.info("deployment_started", cluster=cluster_name, version=version, replicas=count)
log.error("deployment_failed", cluster=cluster_name, error=str(e), duration_ms=elapsed)
```

**Common anti-patterns to avoid:**
- `except Exception: pass` — silently swallows errors in automation, causes silent failures
- Hardcoded credentials or region strings — use env vars or secret managers
- Blocking sync calls in async code — use `asyncio.to_thread()` for sync libraries in async context
- No timeout on HTTP/API calls — always set `timeout=` to prevent hanging automation
- Missing pagination — always use paginators for list operations on cloud APIs

## Key Questions

**Q: How do you use Python to automate Kubernetes operations at scale? What are the patterns you rely on?**
Answer framework: kubernetes Python client for API operations; watch.Watch() for event-driven reconciliation; paginators with `continue` token for large clusters; kopf for writing operators. Key discipline: use label/field selectors to scope API calls, never list all pods across all namespaces without filters on a large cluster. For production operators, Go (controller-runtime) is preferable at high event volume; Python is excellent for tooling, batch operations, and operator prototypes.

**Q: How do you write Python infrastructure tooling that's maintainable and testable, not just "scripts"?**
Answer framework: Type hints + dataclasses for configs (catches errors before execution, enables IDE support). Separate side effects from logic — pure functions that transform data, thin wrappers that call APIs. `moto` for AWS mocking, `responses` for HTTP mocking — no need to hit real infra in unit tests. Context managers for resource lifecycle (ensures cleanup). `tenacity` for retry logic instead of hand-rolled loops. Structured logging instead of print statements.

**Q: When would you choose Python vs. Go for infrastructure tooling? K8s is written in Go — does that mean Go is always better for K8s work?**
Answer framework: Go is the right choice for production K8s operators (controller-runtime's informer cache, work queue, and kubebuilder scaffolding are purpose-built for this), CLI tools (single binary, fast startup), and high-throughput data plane components. Python wins for AI/ML infra (Ray, Airflow, PyTorch are Python-only), cloud automation (boto3, google-cloud SDKs), and operator prototyping. The nuance: K8s being written in Go doesn't mean Go is always better for K8s *tooling* — the Python kubernetes client works well for operational scripts and batch operations. The practical split: Python for the automation and tooling layer, Go for the continuous reconciliation operator layer. That's how it worked at eBay — Python scripts for cloud operations and AI infra, Go controllers (like the Federated Deployment Controller) for production K8s lifecycle management.

**Q: How do you handle concurrent operations in Python infrastructure code?**
Answer framework: asyncio + aiohttp/httpx for many concurrent I/O-bound operations (checking 500 endpoints, batch API calls). `asyncio.gather()` for fan-out, `asyncio.Semaphore` to limit concurrency and avoid rate limiting. For CPU-bound work, `multiprocessing` (GIL doesn't affect this). For K8s async, `kubernetes_asyncio`. Key mistake to avoid: mixing sync blocking calls inside async code — use `asyncio.to_thread()` to wrap synchronous libraries.

**Q: How do you use Python in AI/ML infrastructure specifically?**
Answer framework: Ray for distributed training orchestration (remote decorators, GPU resource allocation). Airflow/Prefect for ML pipeline DAGs (data validation → training → evaluation → promotion). MLflow/W&B for experiment tracking. prometheus_client for custom metrics from model servers. The key difference from app infra: Python is not just the automation language but the native runtime language of the AI workloads themselves — infra code and model code share the same language, which reduces the context switch burden on ML engineers.

**Q: What are the most dangerous patterns in infrastructure Python code and how do you prevent them?**
Answer framework: (1) Silent exception swallowing (`except: pass`) — fatal in automation, causes silent partial failures; always log and re-raise or handle explicitly. (2) Missing pagination — boto3 list operations only return first page; always use paginators. (3) No timeouts on external calls — hanging automation blocks pipelines indefinitely. (4) Hardcoded credentials — use environment variables, AWS IAM roles, or Vault. (5) Blocking sync calls in async code — deadlocks the event loop. The common theme: infrastructure automation failures are often worse than no automation because they give a false sense of completion.

## Summary

Python's dominance in infrastructure engineering comes from two complementary strengths: a rich ecosystem of cloud and Kubernetes SDKs that makes common automation tasks concise and readable, and its position as the native language of the AI/ML stack (Ray, Airflow, PyTorch, MLflow) which makes it indispensable for AI Infra roles specifically. In practice, Python infrastructure code lives on a spectrum from quick operational scripts to production-grade operators and platform tooling — the discipline gap between these two ends is significant, and knowing where to apply type hints, testing patterns, async I/O, and retry logic is what distinguishes maintainable infra tooling from fragile automation debt.

The Kubernetes Python client and kopf operator framework enable the "platform engineering as code" model: CRD-driven lifecycle management, watch loops for reconciliation, and programmatic cluster operations that replace manual kubectl workflows. For cloud automation, boto3's paginator and waiter patterns are the most critical idioms to know — the absence of pagination is a silent bug that only manifests at scale, and the absence of waiters leads to brittle polling loops that don't handle API rate limits correctly. For testing, `moto` for AWS and `pytest` with fixture-driven K8s clients allow infra logic to be unit-tested without hitting real infrastructure, which is the prerequisite for treating automation code with the same quality standards as application code.

For AI Infra Manager roles, the most important Python dimension is the AI/ML ecosystem integration: Ray for distributed training orchestration, Airflow/Prefect for pipeline DAGs, and prometheus_client for model serving observability. The key architectural insight is that in AI infrastructure, Python is not just the automation language — it's also the runtime language of the workloads themselves. This means infra engineers and ML engineers share a language, which reduces the tooling gap but also means infra engineers need enough ML-specific Python fluency (async patterns, GPU resource management, distributed computing primitives) to build platforms that ML engineers can actually use.

## Raw Material
<!-- Save source articles to raw_material/ then link here -->
