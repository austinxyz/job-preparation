---
title: Terraform
category: tech/infra
tags: [terraform, iac, infrastructure-as-code, hcl, provider, state-management, modules, cicd]
status: draft
priority: medium
last_updated: 2026-04-06
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

## Summary

Terraform's core value is turning infrastructure changes into a code-reviewable, reversible, engineering-grade process. Declarative IaC completely separates "what infrastructure I want" from "how to get from current state to desired state" — the engineer describes the former, Terraform computes the latter automatically. This thinking is identical to Kubernetes's control loop (observe → diff → act): understand one and the other follows naturally.

State is where Terraform problems most often originate: State Drift (modifying infrastructure outside Terraform), concurrent apply (missing locking), and sensitive data in State (unencrypted) are the three most common sources of production incidents. Remote Backend (S3 + DynamoDB) solves the first two; encryption solves the third.

From an AI Infra perspective, Terraform is the standard tool for managing GPU cluster foundational resources (VPC, subnets, IAM roles, EKS/GKE clusters). `create_before_destroy` + node group rolling replacement is the common pattern for GPU node upgrades; `prevent_destroy` protects shared storage (EFS/S3) from accidental deletion; `lifecycle.ignore_changes` works with Karpenter to handle external node count adjustments.

> 面试重点：声明式 vs 命令式的本质区别；State 三大问题（Drift/并发/加密）；for_each vs count；CI/CD 最佳实践（PR 只读，合并后执行）

## Raw Material
- [[raw_material/tech/infra/terraform]]
