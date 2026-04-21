---
title: Terraform
category: tech/infra
tags: [terraform, iac, infrastructure-as-code, hcl, provider, state-management, modules, cicd]
status: in-progress
priority: medium
last_updated: 2026-04-18
created_from_jd:
---

# Terraform

## Knowledge Map
- Prerequisites（前置知识）：[[Cloud Infrastructure]], [[Kubernetes]]
- Related Topics（延伸话题）：[[Hybrid Cloud Deployment]], [[GitOps]], [[CI/CD]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**Declarative IaC — Infrastructure as Code（声明式基础设施）**
- Terraform describes the "desired end state" (declarative); the system automatically converges — vs shell scripts that describe "how to do it" (imperative), which are one-shot with no state awareness
- Core advantages: **re-entrant, verifiable, idempotent** — running multiple times yields the same result （幂等）
- Provider abstraction layer: 3000+ platforms (AWS/GCP/Azure, etc.) are integrated via Providers; `terraform init` auto-downloads from the Registry, similar to `npm install`
- **DAG (Directed Acyclic Graph)**: Terraform discovers dependencies automatically from resource references; resources without dependencies execute in parallel; `depends_on` adds explicit dependencies （自动依赖推断）

**HCL — Four Core Block Types（四核心语法块）**
- `resource`: declares the resource to create/manage (the primary block)
- `variable`: user input parameters; `sensitive = true` hides plaintext; value priority: `-var` CLI > `TF_VAR_xxx` env var > `*.auto.tfvars` > `terraform.tfvars` > default
- `data`: read-only query of an existing external resource (does not create anything) （只读查询）
- `output`: exposes module outputs for other modules to reference
- `count` vs `for_each`: count uses indexes — deleting a middle element causes all subsequent resources to be recreated (high-risk) （高危）; for_each uses keys for precise deletion, safer

**Lifecycle Workflow（生命周期工作流）**
- `terraform init`: downloads Providers, modules, initializes Backend (must be the first step)
- `terraform validate`: local syntax check (no cloud API calls needed)
- `terraform plan`: calls cloud APIs to compute changes; `+` = create, `~` = modify, `-` = destroy; `-out` saves the plan to a file to prevent state drift between plan and apply
- `terraform apply`: executes changes; `terraform destroy`: deletes all resources in reverse dependency order
- CI/CD best practice: in PR phase run `fmt -check → validate → plan` (read-only); after merge to main, run `apply` （先只读后执行）

**State Management — Remote Backend（State 管理）**
- Multi-person collaboration requires three things: **storage** (shared centrally) + **locking** (prevent concurrent apply) + **encryption** (State contains sensitive data)
- AWS standard: **S3** (stores State file) + **S3 SSE** (at-rest encryption) + **DynamoDB** (distributed lock, `LockID` primary key) （S3+DynamoDB 标准方案）
- Multi-environment isolation: directory isolation (separate directory per environment — flexible, recommended when environments differ significantly) vs Workspace (same code, multiple States — when environments differ minimally)
- Importing manually-created resources: `terraform import` (records in State, but `.tf` config must be written manually); State Drift = real resources diverge from State; `terraform refresh` syncs them

**Module Design（模块化设计）**
- Standard directory layout: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `examples/`, `README.md`
- Modules should **not** declare Providers (loses reusability); the caller passes them in; use `providers` parameter with aliases for multi-Provider scenarios
- Sources: local directory / Git (supports tags) / Terraform Registry (must pin versions); always lock remote module versions to prevent drift

**lifecycle Meta-argument（高级生命周期控制）**
- `prevent_destroy = true`: protects critical resources (e.g., production RDS) from accidental deletion （防误删）
- `ignore_changes = [field]`: ignores diffs triggered by external systems (e.g., Auto Scaler) modifying the specified attribute
- `create_before_destroy = true`: creates the new resource before destroying the old one (zero-downtime replacement); beware that brief co-existence may trigger naming conflicts — use random suffixes

**State Advanced Operations（State 高级操作）**
- `terraform state mv <src> <dst>`: renames a resource in State without destroying it — used when refactoring code (e.g., extracting a resource into a module) （重构必备）
- `terraform state rm <resource>`: removes a resource from State without destroying the real resource — used to "unmanage" a resource or hand it to another module
- `terraform taint <resource>` (deprecated → `terraform apply -replace=<resource>`): forces recreation of a specific resource on next apply
- State file surgery: edit JSON directly only as a last resort; always back up State before any manual operations; most common mistake is losing lock during manual edits

**Secrets and Sensitive Values（Secrets 管理）**
- Terraform State stores values in plaintext by default — any `sensitive = true` variable is still written to State; **State must be encrypted at rest** (S3 SSE / Terraform Cloud encryption)
- Vault integration pattern: use `vault_generic_secret` data source to pull secrets at apply time; secrets never appear in `.tf` files; requires Vault provider auth (AppRole or IAM)
- `sensitive = true` on `output` and `variable` blocks hides values from CLI output and plan — does NOT prevent storage in State
- Environment variable pattern: pass secrets via `TF_VAR_xxx` env vars in CI/CD — never commit secrets to `.tfvars` files

**Scale: Terragrunt and Module Registry（大规模管理）**
- Terragrunt is a thin Terraform wrapper for DRY configuration across many environments: centralizes remote backend config, enforces module version pinning, generates boilerplate `provider` blocks — replaces repetitive copy-paste across `dev/staging/prod` directories
- Internal module registry: publish reusable modules to a private registry (Terraform Cloud, GitLab, or git tags); consumers reference by version (`source = "git::https://..." ref=v1.2.0`) — prevents dependency drift
- Blast radius management: keep modules small and focused; separate state files per service/environment; a `terraform destroy` in one state file should never be able to take down unrelated services
- Atlantis: open-source tool that runs `plan` on PRs and `apply` on merge via GitOps workflow; adds PR comments with plan output; enforces "plan before apply" discipline for teams

**Testing（测试）**
- `terraform validate`: syntax only — fastest, no cloud calls; run first in CI
- `terraform plan`: integration check against real cloud APIs — catches missing IAM permissions, quota limits, naming conflicts
- `terraform test` (1.6+): native HCL test framework; spins up real resources, runs assertions, tears down — replaces need for Go-based tests for simple cases
- Terratest (Go library): full integration testing — provision real infra, run assertions, destroy; overkill for simple modules but essential for complex reusable modules with many consumers
- Checkov / tfsec: static analysis for security misconfigurations (e.g., S3 buckets without encryption, security groups with 0.0.0.0/0); run in CI alongside `plan`
- Infracost: estimates monthly cost change from a plan — useful in PR comments to flag unexpectedly expensive changes before apply

## Key Questions

**Q: What is the fundamental difference between Terraform and deploying infrastructure with shell scripts?**
Answer framework: Declarative vs imperative; re-entrant vs one-shot; Terraform is aware of end state (plan computes diff), shell only describes operations with no state awareness; State lets Terraform know "what currently exists" to compute "what's still missing."
> 中文提示：声明式 vs 命令式；State 是 Terraform 知道"当前是什么"的核心，从而计算"还差什么"

**Q: What is the difference between `count` and `for_each` for batch resource creation? When should you use `for_each`?**
Answer framework: count uses indexes (0~n-1) — deleting a middle element causes all subsequent resources to be recreated; for_each uses keys — only the matching key is deleted; production environments almost always use for_each; count only for simple, fixed-count, order-insensitive scenarios.
> 中文提示：count 按索引，删中间元素触发后续全重建（高危）；for_each 按 key 精确删除；生产几乎总用 for_each

**Q: What problems arise from storing State locally in a multi-person team? How do you solve them?**
Answer framework: concurrent apply conflicts (infrastructure chaos) + State contains sensitive data with no encryption; AWS standard: S3 storage + SSE encryption + DynamoDB lock; all three are required; in practice often wrapped with Atlantis or Terraform Cloud.
> 中文提示：三要素缺一不可：S3 存储 + SSE 加密 + DynamoDB 锁；缺锁并发混乱，缺加密泄露敏感信息

**Q: How do you bring an existing cloud resource (manually created in the console) under Terraform management?**
Answer framework: `terraform import <resource> <id>`; after import, State has the record but `.tf` config must be written manually; run `plan` to verify zero diff before considering it complete; Terraform 1.5+ supports `terraform plan -generate-config-out` to auto-generate initial config (reduces manual effort).
> 中文提示：import 只写 State，.tf 配置需手动补；再跑 plan 确认无 diff 才算完成

**Q: What should Terraform CI/CD run during the PR phase vs after merge?**
Answer framework: PR phase — read-only: `fmt -check` (format) → `validate` (syntax) → `init` (download deps) → `plan` (compute changes for review); fail-fast with lightweight checks first; after merge to main, run apply; optionally add infracost for cost estimation in PR and tfsec for security scanning.
> 中文提示：PR 阶段只读（fmt→validate→plan），合并后才 apply；快速失败原则，轻量检查前置

**Q: How do you manage Terraform across a large organization with many teams and environments?**
Answer framework: Three pillars — module registry (reusable, versioned modules prevent copy-paste drift), remote backend isolation (separate State per team/environment limits blast radius), and GitOps enforcement (Atlantis or Terraform Cloud enforce plan-before-apply). Terragrunt handles DRY configuration for many environments. The key governance rule: no one runs `terraform apply` locally in production — all changes go through CI/CD with PR review of plan output.
> 中文提示：三支柱：模块仓库（版本化复用）+ State 隔离（限爆炸半径）+ GitOps（Atlantis 强制 plan review）

**Q: How do you handle secrets in Terraform? What are the risks?**
Answer framework: Terraform State stores everything in plaintext — `sensitive = true` only hides CLI output, does NOT encrypt State. Three mitigations: (1) encrypt State at rest (S3 SSE or Terraform Cloud); (2) use Vault data sources to pull secrets at apply time — never hardcode in `.tf` or `.tfvars`; (3) pass secrets via `TF_VAR_xxx` env vars in CI/CD. Most common mistake: committing `terraform.tfvars` with secrets — add it to `.gitignore`.
> 中文提示：sensitive=true 只隐藏 CLI 输出，State 仍明文；三招：State 加密 + Vault data source + CI TF_VAR 注入

**Q: You need to refactor a Terraform module — move a resource into a submodule without destroying it. How?**
Answer framework: `terraform state mv module.old.resource_type.name module.new.submodule.resource_type.name` — moves the State record without destroying the real resource. Then update the `.tf` config to match the new address and run `plan` to confirm zero diff. Always back up State first (`terraform state pull > backup.tfstate`). Never do this without a successful backup.
> 中文提示：state mv 只改 State 记录，不动真实资源；改完跑 plan 确认 zero diff；先备份 State

## Summary

Terraform's core value is turning infrastructure changes into a code-reviewable, reversible, engineering-grade process. Declarative IaC completely separates "what infrastructure I want" from "how to get from current state to desired state" — the engineer describes the former, Terraform computes the latter automatically. This thinking is identical to Kubernetes's control loop (observe → diff → act): understand one and the other follows naturally.

State is where Terraform problems most often originate: State Drift (modifying infrastructure outside Terraform), concurrent apply (missing locking), and sensitive data in State (unencrypted) are the three most common sources of production incidents. Remote Backend (S3 + DynamoDB) solves the first two; encryption solves the third.

From an AI Infra / cloud platform perspective, Terraform is the standard tool for managing GPU cluster foundational resources (VPC, subnets, IAM roles, EKS/GKE clusters, IRSA). Common patterns:
- **GPU node group upgrades**: `create_before_destroy` on the managed node group + random suffix on launch template name → zero-downtime rolling replacement; GPU nodes take 5–10 min to provision, so plan for longer convergence windows
- **Shared storage protection**: `prevent_destroy` on EFS/S3 buckets shared across training jobs — accidental `terraform destroy` on a shared dataset store is catastrophic
- **Karpenter compatibility**: `lifecycle.ignore_changes = [desired_size]` on node groups managed by Karpenter — prevents Terraform from fighting Karpenter's autoscaling decisions
- **IRSA (IAM Roles for Service Accounts)**: standard pattern — `aws_iam_role` + trust policy referencing OIDC provider + `aws_iam_role_policy_attachment`; wrap in a reusable module so every team gets IRSA correctly without copy-pasting the trust policy
- **Multi-region GPU fleet**: use `for_each` over a `var.regions` map to replicate cluster resources across regions; per-region State files in separate S3 keys; blast radius of a bad apply stays within one region

> 面试重点：声明式 vs 命令式的本质区别；State 三大问题（Drift/并发/加密）；for_each vs count；CI/CD 最佳实践（PR 只读，合并后执行）

## Raw Material
- [[raw_material/tech/infra/terraform]]
