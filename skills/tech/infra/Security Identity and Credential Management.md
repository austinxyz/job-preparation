---
title: Security Identity and Credential Management
category: tech/infra
tags: [security, identity, iam, credential-management, zero-trust, oauth, oidc, rbac, supply-chain-security, secrets-management]
status: draft
priority: medium
last_updated: 2026-05-17
created_from_jd: "[[positions/Senior Manager, Software Engineering, IT Infrastructure - NVIDIA]]"
---

# Security Identity and Credential Management

## Knowledge Map
- 前置知识：CI/CD Pipeline Engineering, Kubernetes, cloud security fundamentals
- 延伸话题：IAM (AWS IAM, GCP IAM), RBAC in Kubernetes, OIDC/OAuth2, Vault (HashiCorp), SPIFFE/SPIRE, zero-trust architecture, supply chain security (SLSA, Sigstore/Cosign)
- 管理关联：security review process, compliance requirements, cross-team security policy enforcement

## Core Concepts

### Access Control Model Taxonomy

| Model | Basis | Flexibility | Complexity | Typical Use Cases |
|-------|-------|-------------|------------|------------------|
| **RBAC** (Role-Based) | User role (Engineer, Manager, Admin) | Low | Low | Most enterprise apps, OS permissions |
| **ABAC** (Attribute-Based) | User attrs + resource attrs + environment attrs | High | High | Fine-grained enterprise access, regulated data |
| **PBAC** (Policy-Based) | Unified policy language (XACML, OPA Rego) | Very High | High | Cloud IAM, Kubernetes, centralized audit |
| **ReBAC** (Relationship-Based) | Graph relationships (friend, team-member, owner) | High | Medium | Social platforms, collaboration tools, Google Zanzibar |
| **CBAC** (Context-Based) | Real-time context: IP, device, location, time | Dynamic | Medium | Zero Trust systems, conditional access |
| **CapBAC** (Capability-Based) | Bearer capability token defining permitted scope | High | Low | IoT, blockchain, distributed systems |

- **RBAC**: simple and auditable; breaks down at scale when roles proliferate (role explosion problem)
- **ABAC**: attributes evaluated at decision time (user.title=Manager + document.classification=Confidential + time=weekday → allow); flexible but policy authoring is complex
- **PBAC**: centralized policy engine (AWS IAM, OPA/Rego in K8s, XACML); enables cross-system audit; treat policies as code (version-controlled, tested)
- **ReBAC**: Google Zanzibar model; "User U has permission P on object O if there exists a path in the relationship graph"; scales to social network-level authorization; used by Google Drive, Airbnb, GitHub
- **CBAC**: real-time contextual signals evaluated at every access attempt; core to Zero Trust; IP allowlisting, MFA step-up for sensitive operations, location-based access
- **CapBAC**: capability = bearer token encoding what the holder can do; common in IoT (device has a token saying "can read sensor data"), blockchain (smart contract capabilities), and distributed systems where centralized identity verification is impractical

### Zero Trust Architecture

- **Principle**: "never trust, always verify" — no implicit trust based on network location; every access request verified as if from an untrusted network
- **Hybrid authorization model** in modern enterprises:
  1. **RBAC** as the base: simplifies role-to-permission mapping
  2. **ABAC/CBAC** layered on top: fine-grained decisions + real-time context evaluation
  3. **PBAC engine** (OPA, AWS IAM, Azure Policy) provides centralized control and audit
  4. **OAuth 2.0 / OpenID Connect** for third-party and federated authorization
- **Zero Trust for AI agents**: agent identity must be independently verified at every invocation; agents don't inherit trust from the user who spawned them; permissions must be explicitly delegated (see [[MCP and A2A Protocols]])

### OAuth 2.1 and PKCE

- **OAuth 2.1** consolidates best practices from OAuth 2.0; requires PKCE for all clients; removes implicit flow
- **PKCE (Proof Key for Code Exchange)**: `code_verifier` (random secret) + `code_challenge` (SHA-256 hash of verifier); prevents authorization code interception attacks; mandatory for public clients
- **Flow summary** (Authorization Code + PKCE):
  1. Client generates `code_verifier` + `code_challenge`
  2. Authorization request with `code_challenge`
  3. User approves → Authorization Server returns `code`
  4. Client exchanges `code` + `code_verifier` → `Access Token` + optional `Refresh Token`
  5. Client uses `Access Token` for resource access
- **For MCP**: OAuth 2.1 is the standard for HTTP-transport MCP deployments; MCP server returns `401 + WWW-Authenticate`, client discovers Authorization Server from resource metadata, then runs PKCE flow

### Secrets Management

- **Never hardcode**: API keys, DB passwords, TLS certs, tokens — all must live in secrets stores, not source code or environment files
- **HashiCorp Vault**: secrets-as-a-service; dynamic secrets (DB credentials generated per-request with TTL); secret leasing and revocation; audit log of every access
- **K8s Secrets + External Secrets Operator**: sync from Vault/AWS Secrets Manager to K8s Secrets; avoids storing secrets in etcd unencrypted (encrypt etcd at rest)
- **SPIFFE/SPIRE**: workload identity for microservices; each workload gets a cryptographic identity (SVID); eliminates static service account tokens; enables mTLS between services

## Key Questions

**Q: When would you choose ABAC over RBAC, and what are the tradeoffs?**
Answer framework: RBAC works when permissions naturally map to roles and role count stays manageable; breaks down with "role explosion" (thousands of roles for fine-grained access). Switch to ABAC when access depends on multiple dynamic factors simultaneously (user department + document classification + time of day). ABAC tradeoffs: more expressive but harder to audit ("who has access to X?" requires policy simulation), policy authoring is complex, performance at scale requires caching. In practice, use RBAC as the base + ABAC for the exceptions; centralize via a PBAC policy engine for auditability.

**Q: Explain Zero Trust and how you'd implement it for a cloud-native infrastructure team.**
Answer framework: Zero Trust = "never trust, always verify" at every access boundary. Implementation layers: (1) identity — every human and workload authenticated via OIDC/SPIFFE, no implicit network trust; (2) device — endpoint posture checked before access granted; (3) network — microsegmentation, no flat internal network, service mesh with mTLS (Istio/Linkerd); (4) application — PBAC policy engine (OPA in K8s) enforces least-privilege; (5) data — encryption at rest + in transit, secrets in Vault with dynamic credentials. For AI agents specifically: agent identity verified independently at each invocation; permissions explicitly delegated, never inherited.

**Q: How would you design a secrets management strategy for a multi-service Kubernetes environment?**
Answer framework: Never store secrets in K8s Secrets unencrypted (etcd encryption at rest is step 1). Use External Secrets Operator to sync from Vault or AWS Secrets Manager into K8s Secrets at runtime. For service-to-service auth, use SPIFFE/SPIRE workload identity (SVID certificates) + mTLS instead of static tokens. For database credentials, use Vault dynamic secrets (credentials generated per-request with short TTL, auto-revoked). Audit: Vault provides audit log of every secret access; use this for compliance. Rotation: prefer dynamic credentials over periodic rotation — if dynamic isn't possible, automate rotation with zero-downtime rollout.

## Summary

Modern enterprise access control has evolved from simple RBAC toward layered hybrid models: RBAC provides the base role structure, ABAC and CBAC add fine-grained attribute- and context-based decisions, and a centralized PBAC engine (OPA, AWS IAM, Azure Policy) unifies policy authoring and audit. ReBAC (Google Zanzibar model) handles relationship-graph authorization at scale for collaborative platforms. The industry has converged on Zero Trust as the architectural principle — no implicit trust based on network location, every access verified independently — implemented via OIDC/SPIFFE workload identity, mTLS service mesh, PBAC policy engines, and OAuth 2.1 + PKCE for application-level authorization. For AI agent systems, Zero Trust is especially critical: agents must have independently verified identities, explicitly delegated (not inherited) permissions, and all authorization events must be logged for compliance audit.

## Key Terms

**Access Control Models**
- `RBAC` · `ABAC` · `PBAC` · `ReBAC` · `CBAC` · `CapBAC` · `Zero Trust` · `role explosion` · `Google Zanzibar`

**OAuth / OIDC**
- `OAuth 2.1` · `PKCE` · `code_verifier` · `code_challenge` · `Authorization Code flow` · `Access Token` · `Refresh Token` · `CIBA`

**Policy Engines**
- `OPA (Open Policy Agent)` · `Rego` · `XACML` · `AWS IAM` · `Azure Policy` · `Kubernetes RBAC`

**Secrets Management**
- `HashiCorp Vault` · `dynamic secrets` · `External Secrets Operator` · `SPIFFE/SPIRE` · `SVID` · `mTLS` · `etcd encryption at rest`

## Raw Material
- `jobs/Weekly/2026-W20 (May 12 - May 18)/MCP 学习笔记.md` (access control taxonomy section)
