---
title: Go for Infrastructure
category: tech/software-eng
tags: [golang, go, infrastructure, cli-tools, api-server, concurrency, systems-programming, kubernetes, controller-runtime, kubebuilder]
status: in-progress
priority: high
last_updated: 2026-04-14
created_from_jd: "[[positions/Senior Manager, Software Engineering, IT Infrastructure - NVIDIA]]"
---

# Go for Infrastructure

## Knowledge Map
- 前置知识：Python for Infrastructure, systems programming basics, REST API design, Kubernetes concepts
- 延伸话题：[[Kubernetes]], [[CI-CD Pipeline Engineering]], [[API Design]], [[SRE Practices and SLO Engineering]]
- 管理关联：reviewing Go-based infrastructure code, Go vs Python architectural decisions, K8s operator production readiness

## Core Concepts

### Why Go for Infrastructure

Go has become the dominant systems language for cloud-native infrastructure because:
- **K8s and its entire ecosystem are written in Go** — controller-runtime, client-go, kubebuilder, Helm, Istio, Prometheus, Prow, Tekton, ArgoCD are all Go. Contributing to or extending these tools means Go.
- **Compiled to a single static binary** — no runtime dependencies, no `pip install`, no interpreter version conflicts. `docker cp binary /usr/local/bin/` and it works.
- **True concurrency with goroutines** — goroutines are cheap (2KB stack, grows as needed) and communicate via channels; no GIL. A Go server spawning 10,000 goroutines is routine; a Python equivalent requires asyncio complexity or process-based multiprocessing.
- **Explicit error handling** — every function returns `(value, error)`. Errors cannot be silently swallowed (unlike Python exceptions). This is inconvenient for scripting but essential for production automation where silent partial failures are the hardest bugs.
- **Fast compilation and fast runtime** — Go compiles in seconds, runs near C speed. This matters for CLI tools (Python startup lag is perceptible at 200ms+), high-throughput API servers, and data plane components.
- **Small memory footprint** — a Go service typically uses 5–10x less memory than its Python equivalent, relevant when running many operator instances per cluster.

### Core Use Cases

| Use case                    | Key libraries                                                  | Typical task                                               |
| --------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------- |
| K8s operators / controllers | `controller-runtime`, `client-go`, `kubebuilder`               | Reconcile CRDs, manage cluster lifecycle, enforce policies |
| CLI tools                   | `cobra`, `viper`                                               | `kubectl` plugins, operational scripts, admin tools        |
| REST API servers            | `net/http`, `gin`, `echo`, `chi`                               | Internal APIs for infrastructure self-service platforms    |
| gRPC services               | `google.golang.org/grpc`, `protobuf`                           | High-performance inter-service communication               |
| Admission webhooks          | `controller-runtime/webhook`, `sigs.k8s.io/controller-runtime` | Validate/mutate K8s resources at admission time            |
| Network tooling             | `net`, `gopacket`, `netlink`                                   | CNI plugins, load balancer data planes, proxies            |
| Infrastructure testing      | `testing`, `testify`, `envtest`                                | Unit tests, integration tests with real K8s API            |
| Observability               | `prometheus/client_golang`, `opentelemetry-go`                 | Metrics emission, tracing instrumentation                  |

### Go Concurrency for Infrastructure

Go's concurrency model is the reason it's preferred over Python for components that handle many simultaneous events (K8s controllers, API servers, health checkers).

**Goroutines and channels — basic pattern:**
```go
func processFleet(clusters []string) {
    results := make(chan result, len(clusters))

    for _, cluster := range clusters {
        go func(c string) {
            res, err := checkCluster(c)
            results <- result{cluster: c, data: res, err: err}
        }(cluster)
    }

    for range clusters {
        r := <-results
        if r.err != nil {
            log.Error(r.err, "cluster check failed", "cluster", r.cluster)
        }
    }
}
```

**Limiting concurrency with semaphores:**
```go
sem := make(chan struct{}, 10) // max 10 concurrent

for _, cluster := range clusters {
    sem <- struct{}{}
    go func(c string) {
        defer func() { <-sem }()
        upgradeCluster(c)
    }(cluster)
}
```

**Context for cancellation and timeout — mandatory in infra code:**
```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

if err := deployToCluster(ctx, cluster, spec); err != nil {
    if errors.Is(err, context.DeadlineExceeded) {
        log.Error(err, "deployment timed out", "cluster", cluster)
    }
    return err
}
```

Always pass `context.Context` as the first argument. Every infra operation that touches a network or K8s API must accept a context — this enables timeout propagation, cancellation chains, and clean shutdown.

### Kubernetes Controllers with controller-runtime

`controller-runtime` (the library underlying kubebuilder and operator-sdk) is the production standard for K8s operators in Go. Understanding its architecture is essential for platform engineering.

**Core architecture:**
```
Manager
  └─ Controller (per resource type)
       └─ Reconciler (your business logic)
            └─ client (cached reads + direct writes)
  └─ Informer cache (watches API server, serves reads locally)
  └─ Work queue (deduplicates events, rate-limits retries)
  └─ Webhook server (admission validation/mutation)
```

**The reconciler pattern:**
```go
type ClusterUpgradeReconciler struct {
    client.Client
    Scheme *runtime.Scheme
    Log    logr.Logger
}

func (r *ClusterUpgradeReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := r.Log.WithValues("clusterupgrade", req.NamespacedName)

    // 1. Fetch the desired state (from informer cache — fast, no API call)
    var upgrade myv1.ClusterUpgrade
    if err := r.Get(ctx, req.NamespacedName, &upgrade); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // 2. Observe current state
    currentVersion, err := r.getCurrentClusterVersion(ctx, upgrade.Spec.ClusterName)
    if err != nil {
        return ctrl.Result{}, err  // requeue with backoff
    }

    // 3. Reconcile: make current match desired
    if currentVersion == upgrade.Spec.TargetVersion {
        log.Info("cluster already at target version")
        return ctrl.Result{}, nil
    }

    if err := r.triggerUpgrade(ctx, upgrade); err != nil {
        return ctrl.Result{}, err
    }

    // 4. Requeue to check progress
    return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
}

// Register with manager
func (r *ClusterUpgradeReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&myv1.ClusterUpgrade{}).
        Owns(&corev1.Pod{}).          // also reconcile when owned pods change
        WithOptions(controller.Options{MaxConcurrentReconciles: 5}).
        Complete(r)
}
```

**Key controller-runtime concepts:**

- **Informer cache**: all reads (`r.Get`, `r.List`) are served from an in-memory cache populated by watches on the API server. This dramatically reduces API server load at scale — critical for operators managing thousands of objects.
- **Work queue**: events are deduplicated before entering the reconcile loop. If 10 events arrive for the same object while it's being reconciled, only one reconcile is triggered after. This handles event storms gracefully.
- **`ctrl.Result{RequeueAfter: ...}`**: explicit requeue scheduling — use this instead of sleep loops.
- **Idempotency requirement**: the reconcile function will be called multiple times for the same object. It must be safe to run repeatedly — check current state before acting, don't assume state from previous call.
- **Status subresource**: update status via `r.Status().Update()` (not `r.Update()`) — status and spec have separate RBAC and optimistic concurrency.

### Federated Deployment Controller (eBay — real example)

This was a custom K8s controller built with controller-runtime that orchestrated progressive multi-cluster rollouts:

**What it did:**
- Watched a `FederatedDeployment` CRD that declared: source image, target clusters, rollout strategy
- Reconciled by progressively shifting pods to the new version cluster-by-cluster, not all-at-once
- After each cluster, queried an AI-based health detector API for a go/no-go signal
- If health degraded, automatically triggered rollback to the previous image across all deployed clusters
- Exposed rollout progress via status conditions on the CRD

**Why Go (not Python) was the right choice:**
- High event volume: managing 200+ clusters means constant watch events; Go's informer cache handles this efficiently
- System-critical: this controller was in the critical path of every application deployment at eBay
- Long-lived process: Go's memory efficiency and goroutine model are far better for continuously-running controllers than Python
- Kubebuilder scaffolding provided RBAC generation, webhook boilerplate, and CRD schema validation for free

**The AI health check integration:**
```go
func (r *FederatedDeploymentReconciler) checkHealth(ctx context.Context, cluster string) (HealthStatus, error) {
    req, _ := http.NewRequestWithContext(ctx, "GET",
        fmt.Sprintf("%s/health?cluster=%s", r.HealthDetectorURL, cluster), nil)
    resp, err := r.httpClient.Do(req)
    if err != nil {
        return HealthUnknown, err
    }
    defer resp.Body.Close()

    var status HealthStatus
    if err := json.NewDecoder(resp.Body).Decode(&status); err != nil {
        return HealthUnknown, err
    }
    return status, nil
}
```

### Admission Webhooks in Go

Admission webhooks intercept K8s API requests before they are persisted — used for validation (reject non-compliant resources) and mutation (inject defaults, sidecars, labels).

```go
// Validating webhook: rejects pods without resource limits
type PodResourceValidator struct{}

func (v *PodResourceValidator) Handle(ctx context.Context, req admission.Request) admission.Response {
    pod := &corev1.Pod{}
    if err := json.Unmarshal(req.Object.Raw, pod); err != nil {
        return admission.Errored(http.StatusBadRequest, err)
    }

    for _, container := range pod.Spec.Containers {
        if container.Resources.Limits == nil {
            return admission.Denied(
                fmt.Sprintf("container %s has no resource limits — required by policy", container.Name),
            )
        }
    }
    return admission.Allowed("")
}

// Mutating webhook: inject a standard label
func (m *PodLabelInjector) Handle(ctx context.Context, req admission.Request) admission.Response {
    pod := &corev1.Pod{}
    json.Unmarshal(req.Object.Raw, pod)

    if pod.Labels == nil {
        pod.Labels = map[string]string{}
    }
    pod.Labels["platform.myorg.io/managed"] = "true"

    marshaledPod, _ := json.Marshal(pod)
    return admission.PatchResponseFromRaw(req.Object.Raw, marshaledPod)
}
```

**At eBay:** admission webhooks were used to enforce that every deployed container met resource limit requirements and complied with image signing policies — structural enforcement that couldn't be bypassed by application teams.

### REST API Servers in Go

Go's `net/http` is production-ready without a framework; `gin` and `chi` add ergonomic routing and middleware.

```go
// gin — common for infrastructure APIs
r := gin.New()
r.Use(gin.Recovery())  // recover from panics
r.Use(middleware.RequestID())
r.Use(middleware.PrometheusMetrics())

// Cluster provisioning API
r.POST("/api/v1/clusters", func(c *gin.Context) {
    var req CreateClusterRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    clusterID, err := h.provisioner.CreateCluster(c.Request.Context(), req)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    c.JSON(http.StatusAccepted, gin.H{"cluster_id": clusterID, "status": "provisioning"})
})

// Health probe (K8s liveness/readiness)
r.GET("/healthz", func(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{"status": "ok"})
})
```

**Patterns for infrastructure APIs at scale:**
- Always bind and validate input structs (struct tags + binding); never trust raw JSON
- Return `202 Accepted` for long-running operations, not `200 OK` — callers should poll or subscribe
- Use `context.Context` from `c.Request.Context()` for every downstream call
- Expose `/healthz` and `/readyz` separately — liveness (process health) vs readiness (can serve traffic)
- Export Prometheus metrics on `/metrics` — the standard scrape endpoint for K8s-deployed services

### CLI Tools with cobra and viper

Most K8s ecosystem CLI tools (kubectl, helm, kubebuilder itself) use `cobra` for command structure and `viper` for configuration.

```go
var rootCmd = &cobra.Command{
    Use:   "fleet-ctl",
    Short: "eBay Cloud Fleet management CLI",
}

var upgradeCmd = &cobra.Command{
    Use:   "upgrade [cluster-name]",
    Short: "Trigger a K8s version upgrade for a cluster",
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        dryRun, _ := cmd.Flags().GetBool("dry-run")
        targetVersion, _ := cmd.Flags().GetString("version")
        return runUpgrade(args[0], targetVersion, dryRun)
    },
}

func init() {
    upgradeCmd.Flags().Bool("dry-run", false, "Print plan without executing")
    upgradeCmd.Flags().String("version", "", "Target K8s version (required)")
    upgradeCmd.MarkFlagRequired("version")
    rootCmd.AddCommand(upgradeCmd)

    // Bind viper config (env vars or config file)
    viper.AutomaticEnv()
    viper.SetConfigFile("$HOME/.fleet-ctl/config.yaml")
}

func main() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}
```

**Distribution**: `go build -o fleet-ctl .` produces a single binary. Ship via Docker image, package manager, or direct download — no runtime dependencies.

### Infrastructure Testing in Go

```go
// Unit test with testify
func TestClusterVersionCheck(t *testing.T) {
    tests := []struct {
        name        string
        current     string
        target      string
        wantUpgrade bool
    }{
        {"already at target", "1.29", "1.29", false},
        {"needs upgrade", "1.28", "1.29", true},
        {"downgrade blocked", "1.29", "1.28", false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := needsUpgrade(tt.current, tt.target)
            assert.Equal(t, tt.wantUpgrade, result)
        })
    }
}

// Integration test with envtest (real K8s API, no cluster needed)
var testEnv *envtest.Environment

func TestMain(m *testing.M) {
    testEnv = &envtest.Environment{
        CRDDirectoryPaths: []string{filepath.Join("..", "config", "crd", "bases")},
    }
    cfg, _ := testEnv.Start()
    defer testEnv.Stop()

    k8sClient, _ = client.New(cfg, client.Options{Scheme: scheme})
    os.Exit(m.Run())
}

func TestReconcilerCreatesConfigMap(t *testing.T) {
    ctx := context.Background()
    // Create a CRD instance
    cr := &myv1.ClusterUpgrade{
        ObjectMeta: metav1.ObjectMeta{Name: "test-upgrade", Namespace: "default"},
        Spec:       myv1.ClusterUpgradeSpec{TargetVersion: "1.29"},
    }
    require.NoError(t, k8sClient.Create(ctx, cr))

    // Wait for reconciler to run and assert on outcome
    // ...
}
```

**`envtest`** is the K8s controller testing framework: starts a real etcd + API server binary, registers your CRDs, and runs your reconciler against a real API — without needing a full cluster. This is the standard approach for controller integration tests.

### Go Error Handling — Infrastructure Patterns

Go's explicit `(value, error)` return forces error handling at every call site. For infrastructure code this is a feature — silent failures are the hardest class of automation bugs.

```go
// Wrap errors with context (errors.As + %w)
func upgradeCluster(ctx context.Context, name string) error {
    cluster, err := fetchCluster(ctx, name)
    if err != nil {
        return fmt.Errorf("upgradeCluster: fetch %q: %w", name, err)
    }

    if err := drainNodes(ctx, cluster); err != nil {
        return fmt.Errorf("upgradeCluster: drain nodes in %q: %w", name, err)
    }
    return nil
}

// Sentinel errors for recoverable conditions
var ErrClusterNotFound = errors.New("cluster not found")

func fetchCluster(ctx context.Context, name string) (*Cluster, error) {
    c, ok := registry[name]
    if !ok {
        return nil, fmt.Errorf("%w: %s", ErrClusterNotFound, name)
    }
    return c, nil
}

// Caller: check type, not message string
if errors.Is(err, ErrClusterNotFound) {
    // handle missing cluster specifically
}
```

**Anti-patterns to avoid:**
- `_ = someFunc()` — explicitly discarding an error; acceptable only for cleanup (defer Close()), never for business logic
- Returning `nil` error on a code path that silently failed — use explicit error returns everywhere
- `log.Fatal()` inside library code — only in `main()`, never in packages that others call
- Panic in concurrent code — always recover in goroutines you launch; an unrecovered panic crashes the whole process

### Go vs Python for Infrastructure — Decision Guide

(Complementary to the Python note's comparison — from Go's perspective)

| Scenario | Go | Python |
|---|---|---|
| Production K8s operator | ✅ controller-runtime, informer cache, work queue | ⚠️ kopf works, but higher memory + lower throughput |
| Admission webhook | ✅ controller-runtime/webhook, static binary | ⚠️ possible but less ecosystem support |
| CLI tool (`kubectl` plugin, admin script) | ✅ cobra + single binary, fast startup | ⚠️ startup lag, distribution complexity |
| High-throughput REST API server | ✅ goroutines, no GIL, low memory | ⚠️ asyncio needed, GIL limits true parallelism |
| Cloud automation scripts (boto3 workflows) | ⚠️ AWS SDK for Go exists but more verbose | ✅ boto3 is the gold standard |
| AI/ML infra tooling | ❌ no equivalent ML ecosystem | ✅ Ray, Airflow, PyTorch are Python-only |
| Operator prototyping / quick experiments | ⚠️ kubebuilder scaffolding takes setup time | ✅ kopf: new operator in 30 minutes |
| Data plane / network proxy | ✅ near-C performance, direct syscall access | ❌ not suitable |

**eBay pragmatic approach**: Go for controllers and admission webhooks (Federated Deployment Controller, lifecycle operators); Python for cloud automation scripts, AI/ML pipeline tools, and operational tooling. Not an either/or — the two layers are complementary.

## Key Questions

**Q: You have working knowledge of Go but your background is heavier in Python and K8s operations — how would you approach reviewing a team's Go infrastructure codebase?**
Answer framework: Start with the structural patterns — are controllers using controller-runtime correctly (idempotent reconcilers, informer cache for reads, status subresource for status updates)? Is error handling explicit at every layer with `%w` wrapping for context? Are goroutines supervised and channels drained? Is `context.Context` threaded through all I/O operations? For API servers: are inputs validated, are long-running ops returning 202, is there a `/healthz`? The goal of a manager's code review isn't to catch every bug — it's to identify patterns that will produce a class of bugs, and ensure the team has the architectural instincts to avoid them.

**Q: When would you build a K8s operator in Go vs Python? What factors drive that decision?**
Answer framework: Go is the right choice when: the operator is system-critical or in the critical path of other services; it manages a high volume of objects (hundreds of CRDs, frequent events); it's a long-term platform investment that others will depend on. Go's informer cache (reads don't hit the API server), work queue (event deduplication, rate-limited retries), and single binary distribution are all significant advantages at scale. Python/kopf is the right choice when: prototyping a new operator to validate CRD design and reconciliation logic before committing to Go boilerplate; the operator handles a small object count with low event frequency; the handler logic is naturally Pythonic (heavy boto3, prometheus, or ML library usage). At eBay, the Federated Deployment Controller was Go — system-critical, 200+ clusters, continuous event stream. Internal tooling operators were Python.

**Q: How does Go's concurrency model differ from Python's, and why does it matter for infrastructure components?**
Answer framework: Python has the GIL (Global Interpreter Lock) which prevents true parallel execution of Python bytecode across threads — asyncio works around this for I/O-bound work but doesn't apply to CPU-bound work, and the model is complex (sync/async interop is a common source of bugs). Go goroutines are lightweight (2KB stack), scheduled by the Go runtime across OS threads, and genuinely parallel — no GIL equivalent. For infrastructure components that handle many simultaneous events (a controller watching 1,000 CRDs, an API server handling concurrent requests), Go's model is fundamentally simpler: launch a goroutine per event, use channels for coordination, use `context.Context` for cancellation. The practical impact: a Go K8s controller handling 10,000 events/minute uses far less memory and CPU than a Python equivalent, and the code is more readable than equivalent asyncio.

**Q: Walk me through the architecture of a Kubernetes controller you built or operated. What are the key components and how do they interact?**
Answer framework: Use the Federated Deployment Controller as the concrete example — `FederatedDeployment` CRD declares desired multi-cluster state (target image, rollout strategy); the controller's reconciler watches this CRD via informer cache; on each reconcile, it compares current cluster state against desired, triggers the next cluster upgrade if health checks pass, and requeuees to check progress. Highlight controller-runtime's informer cache (no direct API server reads), work queue (deduplicates events), and `ctrl.Result{RequeueAfter}` for progress polling. Explain why auto-rollback is triggered based on the AI health detector signal, not a fixed timeout — and why that required careful context propagation and explicit error returns at every call site.

**Q: How do you write a REST API in Go for internal infrastructure use? What's the design approach for an API used by thousands of engineers?**
Answer framework: Use `gin` or `chi` for routing and middleware; always bind and validate input structs (struct tags, not raw JSON parsing). Design for async: long-running operations return `202 Accepted` with a job ID, not a blocking `200` — callers poll or subscribe. Expose standard K8s probes (`/healthz`, `/readyz`) and Prometheus metrics (`/metrics`) from the start. Version the API (`/api/v1/`) before you have users — retrofitting versioning is painful. Rate limit per-client to protect downstream services. For an API used by thousands of engineers: document it like a public API (OpenAPI spec), provide a Go client library so consumers don't write raw HTTP calls, and treat breaking changes with the same care as a public API change.

**Q: What Go error handling patterns are most important in infrastructure code?**
Answer framework: The `(value, error)` return at every call site is non-negotiable — infrastructure automation that silently discards errors causes partial failures that are the hardest class of bug. Use `fmt.Errorf("context: %w", err)` to wrap errors with call site context so stack traces are reconstructable from the error message alone. Use sentinel errors (`var ErrNotFound = errors.New(...)`) for recoverable conditions that callers need to handle specifically — and `errors.Is()` / `errors.As()` to check them, never string matching. The anti-pattern that causes the most production incidents: `_ = someFunc()` in a code path that actually matters, or `log.Println(err); return nil` (logging the error but hiding it from the caller).

## Summary

Go has become the canonical language for cloud-native infrastructure because its design aligns with what infrastructure components need: true concurrency without a GIL, a single static binary for distribution, explicit error handling that prevents silent failures, and native integration with the Kubernetes ecosystem. The entire K8s control plane, controller-runtime, kubectl, Helm, ArgoCD, Tekton, and Prometheus are all written in Go — which means any team seriously extending or operating these systems will encounter Go code whether they plan to or not.

For an engineering manager, Go proficiency in the infrastructure domain means being able to review controller code for structural correctness (idempotent reconcilers, informer cache usage, work queue design), assess whether an operator should be written in Go vs Python based on scale and operational requirements, and evaluate REST API designs for production readiness (async patterns, validation, observability). The Federated Deployment Controller at eBay is the clearest example: a controller-runtime-based Go operator that orchestrated multi-cluster progressive rollouts across 200+ clusters, integrated with an AI health detector for automated go/no-go decisions, and triggered rollback on degradation — a system-critical component where Go's performance, memory efficiency, and K8s-native tooling were the right choice over Python's faster prototyping speed.

The Go vs. Python decision is not a language loyalty question — it's an engineering judgment call based on: Is this system-critical and long-lived? (Go.) Is it a script or a prototype? (Python.) Does it need to handle thousands of events continuously? (Go.) Does it need to call boto3 or run on a GPU? (Python.) The most effective infrastructure teams use both: Go for the reconciliation layer, Python for the automation and AI/ML tooling layer. Understanding where each belongs — and being able to articulate why — is the core judgment call for a platform engineering manager.

## Key Terms

**核心语言特性**
- `goroutine` · `channel` · `context.Context` · `select` · `sync.Mutex` · `sync.WaitGroup`
- `(value, error)` pattern · `errors.Is()` · `errors.As()` · `fmt.Errorf("%w")` · sentinel error
- `go build` → static binary · `go modules` (`go.mod`, `go.sum`)

**K8s Controller (controller-runtime)**
- `Reconciler` interface · `ctrl.Result{RequeueAfter}` · `client.Client`
- informer cache · work queue · event deduplication
- `kubebuilder` · `operator-sdk` · `envtest`
- status subresource · `r.Status().Update()` · idempotency
- `For()` · `Owns()` · `MaxConcurrentReconciles`

**Admission Webhooks**
- `admission.Request` · `admission.Response`
- `admission.Allowed` · `admission.Denied` · `admission.PatchResponseFromRaw`
- validating webhook · mutating webhook · webhook certificate (cert-manager)

**REST API**
- `gin` · `chi` · `echo` · `net/http`
- `c.ShouldBindJSON()` · struct tags (`binding:"required"`)
- `202 Accepted` (async pattern) · `/healthz` · `/readyz` · `/metrics`
- OpenAPI spec · versioned API (`/api/v1/`)

**CLI Tools**
- `cobra` · `viper` · `cobra.Command` · `RunE` · `MarkFlagRequired`

**Testing**
- `testing` (stdlib) · `testify/assert` · `testify/require`
- `envtest` · table-driven tests · `t.Run()`

**Observability**
- `prometheus/client_golang` · `Counter` · `Gauge` · `Histogram`
- `opentelemetry-go` · span · trace propagation

**反模式 (要避免)**
- `_ = someFunc()` (discarding error in logic path)
- `log.Fatal()` in library code
- unrecovered panic in goroutine
- blocking call without context timeout
- `log.Println(err); return nil` (hiding error from caller)

**Go vs Python 决策点**
- Go: production K8s operator · admission webhook · CLI binary · high-throughput API server
- Python: cloud automation (boto3) · AI/ML infra · operator prototyping · pipeline DAGs

## Raw Material
<!-- No raw_material/ source file — distilled from experience (Federated Deployment Controller, K8s operator work at eBay) and domain knowledge -->
