---
title: Rust for Infrastructure - resources
source: (multiple — see Reading List)
date_saved: 2026-06-07
processed: true
skill_note: "[[skills/tech/software-eng/Rust for Infrastructure]]"
---

# Rust for Infrastructure — Suggested Resources

## Reading List

**Language fundamentals**
- [The Rust Programming Language ("the book")](https://doc.rust-lang.org/book/) — canonical reference; ownership, borrowing, lifetimes
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/) — runnable snippets
- [Tokio tutorial](https://tokio.rs/tokio/tutorial) — async runtime, the foundation of Rust network services
- [Comprehensive Rust (Google)](https://google.github.io/comprehensive-rust/) — Google's internal Rust course, infra-flavored

**Rust vs Go / Python**
- [JetBrains RustRover — Rust vs Go (2025)](https://blog.jetbrains.com/rust/2025/06/12/rust-vs-go/)
- [Bitfield Consulting — Rust vs Go](https://bitfieldconsulting.com/posts/rust-vs-go)
- [Pullflow — Go vs Python vs Rust (2025 benchmarks, jobs, trade-offs)](https://www.pullflow.com/blog/go-vs-python-vs-rust-complete-performance-comparison)
- [Xenoss — Rust vs Go vs Python strategic comparison](https://xenoss.io/blog/rust-vs-go-vs-python-comparison)

**Rust in cloud-native / infra**
- [Rust at CNCF](https://www.cncf.io/blog/2020/06/22/rust-at-cncf/)
- [CNCF — Cloud Native project velocity 2025](https://www.cncf.io/blog/2026/02/09/what-cncf-project-velocity-in-2025-reveals-about-cloud-natives-future/)
- Projects: Mayastor (OpenEBS storage data plane), wasmCloud, Spin (Wasm), Linkerd2-proxy (service mesh data plane)

**Rust in AI infrastructure**
- [Rust Is Quietly Replacing Python in AI Infrastructure (Groundy)](https://groundy.com/articles/rust-quietly-replacing-python-ai/)
- [candle-vllm — Rust LLM inference/serving](https://github.com/EricLBuehler/candle-vllm)
- [Deploying LLMs: Python vLLM vs Rust Candle benchmarks](https://www.penchef.com/machine-learning-infrastructure/deploying-llms-python-vllm-vs-rust-candle-benchmarks)
- [vLLM Semantic Router (Rust + Candle) — Red Hat](https://developers.redhat.com/articles/2025/09/11/vllm-semantic-router-improving-efficiency-ai-reasoning)

## Notes (distilled facts for the skill note)

### Why Rust exists / what it gives
- **Memory safety without GC** — ownership + borrowing enforced at compile time. No null deref, no dangling pointer, no buffer overflow, no data races. Achieved with zero runtime cost (no garbage collector).
- **Performance** — runs ~2× faster than Go, ~25–100× faster than Python on CPU-bound work. C/C++-class speed.
- **No GC pause / predictable latency** — the key selling point for data-plane and inference: no stop-the-world pauses, consistent tail latency.
- **Fearless concurrency** — the borrow checker statically prevents data races, so concurrent code that compiles is race-free. No GIL (unlike Python).
- **Cost** — steepest learning curve of the three. Compiles 10–60× slower than Go. Borrow checker fights you early.

### Job market signal (2025)
- Rust job postings +35% YoY, vs Python +18%, Go +8%. Accelerating demand, smaller absolute base.

### Where Rust is winning in infra
- **Data-plane / network proxies** — Linkerd2-proxy (service mesh sidecar), Cloudflare Pingora (replaced nginx), proxies where GC pauses are unacceptable.
- **Storage data plane** — Mayastor (OpenEBS) — the most actively developed, perf-critical part of the storage system.
- **WebAssembly** — Spin, wasmCloud; Rust is the premier Wasm source language.
- **Observability agents** — Vector (log/metric pipeline), high-throughput data collection.
- **AI inference layer** — Hugging Face tokenizers (Rust), candle (Rust ML framework), candle-vllm, vLLM Semantic Router.

### Rust in AI infra — the specific argument
- vLLM has C++/CUDA kernels but the orchestration/scheduler layer is Python; on an H100 the Python scheduler can be >60% of execution time. Rust removes that overhead.
- Rust value for inference = performance predictability: no GC → consistent latency; no GIL → simultaneous request handling + tokenization on separate threads.
- Already in production: Cloudflare, Hugging Face, vLLM ecosystem.

### The pragmatic 2025 stack
- Hybrid is the norm: Python for orchestration/ML + Rust for hot paths; or Go APIs + Rust compute modules.
- Rust is NOT replacing Go for K8s operators (controller-runtime ecosystem is Go-only) or Python for ML research. It targets the perf-critical layer underneath.

### Manager-relevant judgment
- Rust is a deliberate, high-cost / high-payoff choice — justified by latency SLOs, scale, or memory-safety-critical code (no GC pauses, no CVEs from memory bugs). Not a default.
- Team cost is real: hiring is harder, ramp is slower, build times hurt iteration. Adopt where the data plane demands it, not for control-plane CRUD.

<!-- Processed into skill note 2026-06-07. Distilled from web research + domain knowledge. -->
