---
title: eBay - DoJ and Jade Programs
type: Core
signal_areas: [Scope, Ownership, Ambiguity, Perseverance, Communication, Leadership]
skills: [cross-functional-leadership, kubernetes, k8s, cloud-infrastructure, platform-engineering, incident-management, compliance, automation, devops]
company: eBay
date: 2025-06
impact: high
growing_link:
---

# eBay - DoJ and Jade Programs

## Context

eBay was required to fully remove covered persons from access to PII data, staging, and production environments to comply with a DoJ policy — with significant legal and financial exposure if the deadline was missed. This was a company-wide program with many teams involved. As Cloud Fleet team lead, I owned our team's three workstreams within the larger program: standing up two new cloud environments (SDDZ for isolated dev access and DCPX as a data-sanitization transition layer), transferring ownership of thousands of cloud namespaces and applications away from covered persons, and maintaining full business continuity for all live infrastructure functions — host runtime, OS patching, cloud console, namespace and app RBAC management — throughout the cutover. The overall program ran approximately 3 months, covering solution design, multiple rehearsal rounds, and final execution; the actual environment provisioning and cutover happened in the final 2 weeks once hardware was ready. A significant challenge throughout was ambiguity in requirements: what exactly needed to be isolated was heavily debated — the definition of "covered person access" kept shifting, and each change in scope had large implications for the technical architecture. Multiple rehearsal rounds served double duty: they validated our execution readiness, but they also forced the legal and compliance teams to commit to specific definitions, which is what finally resolved the scope debates.

## Actions

- I broke our team's scope into three parallel execution tracks — Technical (environments and automation), Process (on-call and runbook readiness), People (knowledge transfer and capacity backfill) — and assigned clear ownership within the team for each track so we could move in parallel without constant coordination overhead.
- I participated in the program-wide war room on behalf of Cloud Fleet, ensuring our team's dependencies and blockers were visible to the broader program team and that we were unblocked in time to hit each milestone. A persistent challenge was that the isolation requirements were not fully defined when we started — I had to make architectural decisions with incomplete information, document the assumptions explicitly, and design the environments to be adjustable as the scope got clarified through the rehearsal process.
- I built and maintained a detailed runbook for Cloud Fleet's workstreams covering every step, owner, and dependency, and kept it updated daily as the program evolved.
- I drove automation of AZ/cluster provisioning and namespace/app ownership transfer at scale, using data-driven analysis to prioritize the highest-risk namespaces first; I used AI tooling to build dashboards that gave the team and program leads real-time visibility into transfer progress.
- I streamlined our team's on-call workflows during the program so engineers' attention wasn't split between the migration work and live incident response.
- For knowledge transfer with covered-person engineers, I coordinated and arranged for our engineers to travel on-site where in-person sessions were needed — pairing on critical systems that couldn't be handed off remotely.
- I initiated targeted hiring in parallel to backfill the covered-person capacity we were losing, so we weren't just transferring work but actively rebuilding team capability.

## Results

- Provisioned and configured SDDZ and DCPX environments within the 2-week execution window once hardware was ready.
- Automatically transferred thousands of cloud namespaces and applications with zero customer intervention required.
- Cloud Fleet's workstreams completed on schedule with no critical incidents; the US team absorbed expanded infrastructure scope without service disruption.
- The automated ownership transfer approach was referenced by other teams as a model for large-scale namespace migration.

## Learnings

- Being a team's representative in a large cross-functional program is a different skill than running a project yourself — I had to stay visible and vocal in the war room without overreaching into scope that wasn't ours. Getting that boundary right mattered for team credibility.
- The rehearsal rounds were the highest-ROI investment in the program — not just for de-risking execution, but for forcing requirement clarity. Each rehearsal made the ambiguity concrete: teams had to decide "does this specific system need to be isolated or not?" in order to proceed. I'd start rehearsals much earlier in future programs specifically for this reason — as a mechanism to surface and resolve scope ambiguity, not just as an execution dry-run.
- The manual risk-scoring of namespace priority was a bottleneck on my time in the early weeks. I should have automated that scoring model sooner so the team could self-prioritize without waiting on me.

## Signal Areas

**Primary:** Scope (multi-workstream, zero-slip compliance deadline within a large org-wide program), Ownership (defined and drove Cloud Fleet's three tracks end-to-end), Ambiguity (isolation requirements debated throughout — what needed to be isolated kept shifting, with large technical implications; rehearsal rounds used as a forcing mechanism to resolve scope disputes)

**Secondary:** Perseverance (sustained execution over 3 months with moving requirements and tight deadlines), Communication (war room participation, runbook as coordination artifact, dashboards for stakeholder visibility), Leadership (coordinated knowledge transfer, initiated parallel hiring, kept team on track under sustained external pressure)

## Related Skills
- [[skills/tech/infra/Kubernetes]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/management/people/Engineering Team Management]]

## Interview Usage
- 适用 BQ：Tell me about a time you drove a high-stakes, multi-workstream delivery under an externally imposed deadline
- 适用 BQ：Tell me about a time you coordinated closely with other teams to deliver a critical compliance program
- 适用 BQ：Describe a time you took full ownership of your team's scope within a large cross-functional initiative
- 适用 BQ：Tell me about a time you had to maintain business continuity while executing a major infrastructure change
- 适用 JD 关键词：cross-functional collaboration, compliance, cloud infrastructure, incident management, Kubernetes, program execution, automation at scale

## Key Questions

**Q: How did you manage Cloud Fleet's workstreams within a large, externally-driven program?**
Talking points: Describe how I scoped and structured the three tracks (Technical, Process, People) so the team had clear lanes. War room participation as the visibility mechanism — blocking issues surfaced early. Runbook as the team's single source of truth. Parallel hiring so we rebuilt capacity, not just transferred work.

**Q: Tell me about a time you led a program with significant legal or compliance stakes.**
Talking points: Name the business risk (DoJ policy, PII access, legal and financial exposure). Describe how I focused the team on our specific scope and made sure we hit every milestone. Zero critical incidents on our workstreams. Important to be accurate about role — I owned Cloud Fleet's contribution, not the full program.

**Q: How do you maintain business continuity while executing a major infrastructure migration?**
Talking points: Live surfaces that cannot go down (host runtime, OS patching, RBAC) had their own track. Streamlined on-call to reduce split attention. Automated bulk transfers to remove human bottlenecks. Rehearsal rounds validated the runbook before live cutover.

**Q: How do you make technical decisions when requirements keep changing under a hard deadline?**
Talking points: Name the specific ambiguity (isolation scope kept shifting — each redefinition changed the architecture substantially). Describe how I handled it: documented assumptions explicitly rather than waiting for certainty, designed the environments to be adjustable, and used rehearsal rounds as a mechanism to force legal/compliance teams to commit to specific definitions. The key mindset: ambiguity with a hard deadline means you can't wait for clarity — you move with documented assumptions and create forcing functions that accelerate the decision-making.

**Q: How did you handle knowledge transfer from engineers who were losing system access?**
Talking points: Identified which systems required in-person pairing vs. documentation. Arranged on-site travel for highest-complexity transfers. Built documentation artifacts that persisted beyond the individuals. Started parallel hiring so the team wasn't dependent on any single knowledge-holder long-term.

## Summary

The DoJ and Jade programs were eBay's response to a government compliance mandate requiring covered persons to be fully removed from PII data access. This was a company-wide initiative with many teams involved; Cloud Fleet's contribution was three distinct workstreams — standing up new isolated environments, transferring thousands of namespace and app ownerships at scale, and keeping all live infrastructure functions running through the cutover.

My role was to own Cloud Fleet's scope end-to-end within the larger program: structuring the team's tracks, participating in the program war room to keep our dependencies visible, driving automation for the bulk transfer work, and managing knowledge transfer and capacity backfill in parallel. The full program ran about 3 months; the actual environment setup and cutover completed in 2 weeks once hardware was ready. Cloud Fleet's workstreams hit every milestone with no critical incidents, and the automated namespace transfer approach became a reference for other teams doing similar migrations.

## Raw Material
<!-- No raw_material/ source file — story reconstructed from direct experience -->
