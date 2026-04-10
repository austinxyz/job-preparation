---
title: SRE Practices and SLO Engineering - personal
source: personal experience and practice
date_saved: 2026-04-10
processed: true
skill_note: "[[skills/tech/infra/SRE Practices and SLO Engineering]]"
---

# SRE Practices and SLO Engineering — Personal Notes

我主要是分享我在如何提高eBay K8s API Server Relability的经验，一部分内容也可以看[[eBay - Cloud Infrastructure Team Turnaround]]
总的来说，我们通过apply SRE best Practices，极大的提高了eBay K8s API Server的Reliability，从之前经常site incident，一个极端的例子是Dev API Server down了两天，严重影响了eBay各个开发团队的正常开发。到之后API Server的30天滚动，稳定在SLO 99%, Production可以达到 99.9%

## SLI / SLO / SLA Definitions and Practice

<!-- e.g. How did you define SLIs at eBay? What services did you apply SLOs to?
     What was your target availability? How did you measure it? -->
对于API Server当我们设定SLI/SLO的时候，我们最看中的还是可用性和延迟，因为一开始API Server不是很稳定，所以我们从99%的可用性开始，因为有很多个API Server - Cluster API Server，Federated API Server，不同环境Production，Dev也有API Server。我们从最重要的Federated API Server开始。我们的K8s已经内置了很多Metrics，所以Metrics的建立和SLI/SLO的设定还是挺容易的。
之所以用99%，因为API Server本质上还是Control Plane，主要是Platform Provider来调用的，对于最终用户的影响并不是那么敏感。但是另一方面，我们管理的集群还是很大的，特别是Federated API，总的API的调用量很大，而且各个client在APF没有设定很好情况下容易相互影响，导致整个API Server的Relliability下降。而且很多Team的发布，比如app，network customerrized的controller，都会影响API Server。
## Error Budget Policy

<!-- e.g. What did you do when error budget was exhausted?
     Did you have a freeze policy? How did you balance feature velocity vs. reliability?
     Any specific incident that triggered a budget policy change? -->
基于系统复杂，初始的数据不是很理想，我们开始将Error Budget放的相对高的，95%开始，然后逐渐提高，我们开始的时候做每日review，当发现Error buget快耗尽的时候，去分析具体的原因，是因为release，change的原因，还是因为某个client导致的，所以我们要优化这个client的APF设定。
## Incident Management

<!-- e.g. How did you run incidents? Who was incident commander?
     What was your escalation ladder? How did you do on-call rotation design?
     Any specific high-impact incident and what you learned? -->
我们建立了多级alert/pager，针对SLO/SLI的alert/pager是主要指标，之下还有对于api server instance和etcd相关的alert。我们建立了7 * 24的Pager机制，并且完善了runbook，针对pager，如何做triage，如何恢复都有完整的SOP. 之前我们还几次incident，因为APF没有设定好，因为etcd的goverance没做好，一直上升，对此我们都做了对应的alerts，完善了SOP
## Blameless Post-Mortems

<!-- e.g. How did you run postmortems? What format?
     Examples of systemic fixes that came out of postmortems.
     How did you build psychological safety for engineers to be honest? -->
当然还是会出现Incident，那么事后复盘很重要，对于RCA的话，我们有标准的模板，不是责怪人，侧重中为什么会有incident，为什么MTTD/MTTR高，如何缩短，下次如何避免类似的Incident, 我们将所有Incident的RCA都集中放在一处。每个RCA都有follow up actions，专人负责跟踪，确保action落实。
## Toil Reduction

<!-- e.g. What counted as toil in your teams?
     How did you measure toil as a % of on-call load?
     Examples of toil you eliminated and how. -->
TOIL的工作，我们将某个任务没有SOP，需要on-call化时间重复做的定义为TOIL，API Server的TOIL主要集中在bad instance 和release 导致的API server reliability下降甚至不工作，对于这些问题的triage。目前我们利用AI来做triage，通过MCP server来收集metrics，log，然后由AI agent做综合判断，效果还不错。

## On-Call Design

<!-- e.g. How did you structure on-call rotations?
     Primary/secondary? Follow-the-sun? Escalation paths?
     How did you handle on-call burnout? -->
On-call之前我们是采用follow-the-sun，US和China team各cover 12小时，之后China不能access production，但是我们的India/Europe团队还没有完全成型，我们采用的是Primary/Secondary，让India/Europe团队作为Secondary，并且逐渐往follow-the-sun转移。
Escalation path是on-call person -> tech lead -> engineer manager
## SRE Team Charter and Org Model

<!-- e.g. Embedded SREs vs. centralized SRE team?
     How did you define the handoff criteria between dev team and SRE?
     How did you handle the "SRE as ops dumping ground" anti-pattern? -->
Embedded SREs, team member rotated, centralized SRE team provide tools and best practices. 
## Reliability Culture

<!-- e.g. How did you shift reliability left (making dev teams own reliability)?
     How did you get buy-in from product/PM for reliability investment?
     How did you handle the tension between reliability work and feature work? -->
Team rotated on-call, reliability tickets planned in sprint, team OKR to reduce TOIL, reduce MTTD/MTTR, improve SLO/SLI. encourage feature work to resolve reliability permanently 
## Tools and Stack

<!-- e.g. Monitoring: Prometheus, Grafana, Datadog, CloudWatch?
     Alerting: PagerDuty, OpsGenie?
     Incident tracking: Jira, PagerDuty incidents, Rootly?
     SLO tracking: custom dashboards, Sloth, Nobl9? -->
Prometheus/Sherlock (internal monitor/alert platform)
PagerDuty
JIRA
SLO/SLI dashboard
AI Agent/MCP
## Key Lessons / Principles I'd Defend in an Interview

<!-- Write 3-7 principles you'd stand behind. These become the most memorable
     interview content because they're specific and yours.
     e.g. "Availability targets above 99.9% for stateless services are usually
     achievable with proper deployment practices; the hard part is the dependencies." -->

API Server is complex - we started with simple SLO/SLI, with feasible goal (not aggressive).
Blameless culture, when we made progress,  recognize team member's efforts.
Leverage AI to speed up, based on data analysis, reduce TOIL, improve incident management.
Data driven, resolve top 3 issues firstly
Work-life balance
Build platform features to reduce TOIL


