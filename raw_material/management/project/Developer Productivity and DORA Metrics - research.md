---
title: Developer Productivity and DORA Metrics - research
source: "DORA 2024 State of DevOps Report, DX Core 4 (getdx.com), Octopus Deploy DORA guide, DX blog 2024"
date_saved: 2026-04-11
processed: true
skill_note: "[[skills/management/project/Developer Productivity and DORA Metrics]]"
---

# Developer Productivity and DORA Metrics — Research Notes

Sources:
- [2024 DORA State of DevOps Report](https://dora.dev/research/2024/dora-report/)
- [DX Core 4 framework](https://getdx.com/dx-core-4/)
- [Measuring developer productivity with DX Core 4](https://getdx.com/research/measuring-developer-productivity-with-the-dx-core-4/)
- [4 DORA Metrics explained + 2024 findings (Octopus Deploy)](https://octopus.com/devops/metrics/dora-metrics/)
- [2024 DORA report highlights (DX blog)](https://getdx.com/blog/2024-dora-report/)

---

## The 4 DORA Metrics — Definitions and Benchmarks

The four core metrics from the DORA (DevOps Research and Assessment) program, measuring software delivery throughput and stability:

### 1. Deployment Frequency
How often code is deployed to production.

| Tier | Benchmark |
|---|---|
| Elite | On-demand (multiple times per day) |
| High | Once a day to once a week |
| Medium | Once a week to once a month |
| Low | Less than once a month |

### 2. Lead Time for Changes
Time from code commit to running in production.

| Tier | Benchmark |
|---|---|
| Elite | < 1 day |
| High | 1 day – 1 week |
| Medium | 1 week – 1 month |
| Low | > 1 month |

### 3. Change Failure Rate
Percentage of deployments that cause a failure in production (requiring hotfix, rollback, or incident).

| Tier | Benchmark |
|---|---|
| Elite | 5% |
| High | 10% |
| Medium | 15% |
| Low | 64% |

### 4. Failed Deployment Recovery Time (formerly MTTR)
Time to restore service after a failed deployment.

| Tier | Benchmark |
|---|---|
| Elite | < 1 hour |
| High | < 1 day |
| Medium | 1 day – 1 week |
| Low | 1 month – 6 months |

### How to Measure

- **Deployment Frequency**: total deployments ÷ days in period
- **Lead Time**: average(deployment_timestamp − commit_timestamp)
- **Change Failure Rate**: (failed deployments ÷ total deployments) × 100
- **Recovery Time**: sum(all recovery durations) ÷ number of failures

---

## 2024 DORA State of DevOps Report — Key Findings

Report scope: 39,000+ professionals across industries globally. 10th year of DORA research.

### AI Adoption: Paradox of Productivity
- 75.9% of respondents use AI for at least part of their job (code writing, summarization, explanation, optimization, documentation)
- 75% reported individual productivity gains from AI
- **BUT**: AI adoption correlated with ~1.5% decrease in delivery throughput and ~7.2% decrease in delivery stability
- Root cause hypothesis: AI increases batch size — larger changesets → greater risk → more failures
- 39.2% do not trust AI-generated code
- Documentation is AI's strongest opportunity: 25% more AI adoption in docs → estimated 7.5% quality improvement

### Performance Distribution Shift
- Elite cluster: stable
- High performers: dropped from 31% → 22% of respondents
- Low performers: grew from 17% → 25%
- For the first time, throughput and quality metrics diverged independently (medium performers had lower failure rates than high performers — unusual)

### Platform Engineering: Benefits with Tradeoffs
- Internal developer platforms improve individual productivity and team performance
- But platforms may **slow overall throughput** during implementation
- Platforms primarily serve governance and security, not just productivity
- User-centric platform design (self-service, good documentation, developer independence) is critical to whether platforms actually deliver value

### What Predicts High Performance
- **Transformational leadership**: leaders with clear vision reduce burnout, improve satisfaction, and drive performance at team/product/org level
- **Psychological safety and team autonomy**: among the strongest predictors of delivery performance
- **High-quality internal documentation**: correlates with better reliability and overall DORA metrics
- **Stable priorities**: teams with changing priorities perform worse regardless of technical practices

---

## Beyond DORA: SPACE Framework

Developed by Microsoft Research, GitHub, and academic researchers. Recognizes that productivity is multi-dimensional.

Five dimensions (SPACE acronym):
- **S**atisfaction and well-being — Do developers find work meaningful? Burnout risk?
- **P**erformance — Does output produce desired outcomes? (quality, not just volume)
- **A**ctivity — Measurable outputs (PRs merged, deployments, code reviews)
- **C**ommunication and collaboration — Knowledge sharing, documentation, code reviews
- **E**fficiency and flow — Uninterrupted work time, handoff minimization, toil reduction

**Key SPACE principle**: Never measure just one dimension. Activity metrics (commits, PRs) without quality/satisfaction metrics create perverse incentives.

**Limitation**: SPACE is a framework for defining your own metrics, not a prescribed metric set — requires significant implementation effort.

---

## DX Core 4: Unified Framework (2024)

Developed by DX (Abi Noda, Laura Tacho) with DORA/SPACE/DevEx authors (Nicole Forsgren et al.). Tested with 300+ organizations.

Integrates DORA, SPACE, and DevEx into four dimensions:

| Dimension | What it measures | Example metrics |
|---|---|---|
| **Speed** | How quickly work moves through the system | Lead time, deployment frequency |
| **Effectiveness** | How well engineering aligns with business goals | Developer Experience Index (DXI), self-reported friction |
| **Quality** | Reliability and robustness of software | Change failure rate, recovery time, test coverage |
| **Business Impact** | Value generated relative to effort | Features shipped, reliability SLOs, toil reduction |

### DX Core 4 Key Principles
- **Balanced measurement**: pair throughput metric with a perceptual counterbalance (e.g., diffs per engineer paired with Developer Experience Index) to prevent gaming
- **Deployable in weeks**: use existing data sources + self-reported surveys immediately
- **Avoid incentive traps**: do NOT tie compensation or performance reviews directly to throughput metrics — leads to metric gaming
- **3-12% efficiency gains** and **15% improvement in engagement** reported across implementations

### Why Not Just DORA?
- DORA: prescriptive but limited scope (system performance only, doesn't capture developer experience or business value)
- SPACE: comprehensive but requires you to define your own metrics — high implementation cost
- DX Core 4: prescriptive set that covers all three perspectives

---

## Measuring Developer Productivity: Common Pitfalls

- **Lines of code / commits as productivity**: meaningless. AI now generates both. Focus on outcomes.
- **Vanity metrics**: high deployment frequency without quality metrics → "deploy fast, break things"
- **Individual metrics without team metrics**: creates competition instead of collaboration
- **Measuring activity without flow**: high PR count but low merge rate suggests process bottleneck, not productivity
- **Ignoring developer experience**: teams with poor DX burn out and leave, which destroys long-term velocity
- **Setting targets on metrics**: Goodhart's Law — when a measure becomes a target, it ceases to be a good measure

---

## Developer Productivity in Practice: Key Levers

### Reducing Lead Time
Break lead time into components to find the real bottleneck:
- PR review wait time (→ culture, reviewer availability, PR size)
- Pipeline queue time (→ CI/CD infrastructure scaling)
- Pipeline execution time (→ build optimization, selective testing, caching)
- Deployment wait / approval gates (→ remove manual approvals, use progressive delivery)
- Monitoring/bake time before next deploy (→ automated health checks)

### Improving Deployment Frequency
- Trunk-based development (eliminates long-lived branch merge risk)
- Feature flags (decouple deploy from release)
- Small PR discipline (reduces review cycle and failure risk)
- Self-service deployment (no platform team bottleneck)

### Reducing Change Failure Rate
- Pre-production test coverage gates
- Canary / progressive delivery with automated rollback
- Better monitoring → faster detection of failures (shrinks blast radius)

### Reducing Recovery Time
- Runbooks and SOP for known failure modes
- Automated rollback triggers
- On-call tooling (AI-assisted triage reduces MTTD)
- Blast radius reduction via canary deployments

---

## Platform Engineering and Developer Productivity

From 2024 DORA: internal platforms improve individual productivity but require careful design to avoid being governance overhead.

Platform team as "product team for developers":
- Treat developers as customers; measure platform adoption and developer NPS
- Self-service > ticket-based workflows (eliminates platform team as bottleneck)
- Good documentation is load-bearing infrastructure — DORA found high-quality docs correlate with better reliability
- Platform paved paths: make the easy path the correct path (guardrails, not gates)

Golden path antipatterns:
- Platform forces all teams through a single workflow with no escape hatch → rebellion or workarounds
- Platform team measures adoption without measuring developer satisfaction → vanity metric
- Platform improves throughput metrics without addressing developer experience → burnout

---

## Personal Experience Notes
<!-- 填入你自己在 eBay 实践中的 DORA/velocity 工作。下面是从 CI/CD personal note 提取的关键点，可以展开 -->

### eBay CI/CD velocity work（来自 CI-CD Pipeline Engineering - personal）
- 推行了 DORA metrics，综合定义了 development friction，侧重 lead time、deployment frequency、rollout duration、rollback duration 和 success rate
- 手段：incremental build、selective test（commercial tool）、parallel jobs for validation/security scan、去除 manual 介入、blue/green rollout 减少 rolling upgrade 时间
- 部署完全自动触发，不需要 platform team 介入
- 结合 engineering velocity program，DORA 目标：65% 应用达到 elite tier metrics（deploy within 1 day, on-demand frequency, sub-hour rollback, 95%+ success rate）

### 补充你的经历
<!-- e.g. 你怎么向工程师解释 DORA？如何获得 leadership 对 velocity investment 的支持？
     有没有遇到 metric gaming 的问题？如何处理？
     你用过 SPACE / DX Core 4 吗？还是纯 DORA？
     除了 pipeline 优化，你还做过哪些提高 dev productivity 的事情（code review 文化、PR size、oncall 减负等）？ -->
对于DORA，作为Cloud team我们主要做了两方面的增强。
1. External
	作为platform，我们提供了CI/CD的Infra，我们做了一下工作来提高DORA
	a. keep high infra reliability，避免infra造成的deployment failure。具体来说，我们做了以下component的reliability增强。
		- CIaaS，确保CI slave稳定provision，并且mount right volume
		- Feature pool creation, CD pipeline会on-demand create feature pool, keep high reliability
		- Tekton infra reliability, keep latest version, 针对Tekton可能会建很多的K8s object，将historial的pipeline放在cold storage
		- Federated deployment controller, 做了很多reliability的优化，比如自动retry，skip problematic cluster etc.
		- Blue-green rollout，做了很多performance/scalability的优化，避免大量pod creation导致performance问题
	b. reduce the build and deployment duration
		- 对于image的upload/download做了优化，支持chunk的paraall downlaod，减少image的upload/download time
		- dedicated node pool for CI slave和tekton pods，成功率和效率都比较高
		- cache feature pool，可以快速重用，降低provision 时间
		- Federated deployment， canary rollout，修改health check strategy, fast fail,提供 auto rollback，减少rollback时间
		- Blue-green rollout,一次性将所有pod creation，极大的减少了deployment time
	c. provide pod/deployment level tracking capability 可以帮助user 快速定位app failure root cause 
2. Internal
	Internal的话，我们有自己的CI/CD，同时做了很多工作来提高我们自己component的DORA
	a. Integrate with DORA dashboard, ECD team提供了DORA dashboard，我们将cloud component的DORA也集成进去。这样很容易看到目前的DORA情况
	b. 提高test coverage，完善end2end test，确保每个component都有成熟的health check，将问题发现在早期阶段，提高PR merge后的sucess rate
	c. 和gitOps的集成，确保high frequency rollout
	d. 开始迁移到ArgoCD，使得pipeline的rollout，rollback更快
	e. 通过AI来分析failure，快速定位root cause
DORA的改善数据
external的话，结合 engineering velocity program，DORA 目标：65% 应用达到 elite tier metrics（deploy within 1 day, on-demand frequency, sub-hour rollback, 95%+ success rate），这个在2025年就达到了
internal的话，我们已经迁移了部分key cloud components to ArgoCD （50%）, 总体20%的components可以达到Elite 