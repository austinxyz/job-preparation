---
title: CI/CD Pipeline Engineering - personal
source: personal experience and practice
date_saved: 2026-04-11
processed: true
skill_note: "[[skills/tech/infra/CI-CD Pipeline Engineering]]"
---

# CI/CD Pipeline Engineering — Personal Notes

<!-- 记录你在 CI/CD 方面的实践经验，供 raw-material-processor 提炼到 skill note。
     用中文写没问题，AI 会处理。重点写：你做了什么、为什么这样做、结果如何。 -->
eBay有CIaaS 和ECD（CI as a service - 基于Jenkins 和eBay CD）两部分，提供了CI/CD Pipeline的平台，eBay developer都是基于ECD这个平台来管理应用的CI/CD流程的，同时对于Cloud Control Plane, 我们有自己的CI/CD 方案，通过prow + releaser（自己内部的一个gitOps CD）的方式来做。此外我们也探索ArgoCD来支持multiple clusters的发布。
## Pipeline Architecture & Design

<!-- e.g. 你设计过哪些 CI/CD pipeline？单 monorepo 还是多 repo？
     Pipeline 的阶段是怎么划分的（build / test / scan / deploy）？
     有没有 fan-out / fan-in 的并行设计？ -->
ECD的话，是基于monorepo的，因为eBay采用microservice，一个service一个repo。
CI的话我们采用CIaaS, 基于Jenkins，对于用户的application，我们在K8s中建立CRD/operator来管理，针对某个app的CI，Jenkins采用master和slave的架构，在创建app的时候operator会做好配置在Jenkins master, 每次CI build，operator会create pod for slave，然后mount volume，将build的结果persistence, build结束，slave pod会销毁。CI是container build，基于Kaniko
CD 基于tekton，有自己的UI，做了封装，并且和K8s的deployment做了集成，主要分成两种pipeline，staging pipeline和PR pipeline, staging pipeline是做feature 测试了，可以将build image deploy在动态建立的feature pool，进行测试，和安全性扫描等。PR pipeline是做 prod release的，会将PR merge，然后一次发布到feature/staging/prod，中间有多个step，多级测试（feature test, integration test， smoke test等），以及blue-green，canary rollout等。
对于每个pipeline，我们会定义了必须遵守的policies，比如PR pipeline必须通过多人的PR review，必须是release branch，通过test coverage criteria和security scan，必须deploy到staging，才能deploy到production等。
用户可以做pipeline的customerization，但是有些police是必须遵守的，也就是某些step必须存在。有fan-out，多个step可能可以并行执行，比如run test和security scan，但之后要check policy决定是不是继续。

CI/CD for Cloud control plan, 我们是用prow做CI build，prow是一个完全基于k8s的CI/CD solution -  https://docs.prow.k8s.io/docs/overview/ ，它支持多repo的，并且和github做了集成，当有一个PR的时候，先针对PR 用prow 做CI build，然后跑e2e test，验证通过才是PR merge的前提（此外还需要>=2人的review），之后才提交image，CD部分是采用我们自己的GitOps solution，我们叫做releaser，也是允许多环境的测试，rollout check（我们叫做health monitor），而发布就是通过releaser来commit spec到git。releaser还提供了UI，可以看progress和log，triage release issues。

ArgoCD的solution是想取代releaser 方案，将pipeline转移到ArgoCD上。

## Build System & Tooling

<!-- e.g. 用过哪些 CI 平台：Jenkins、GitHub Actions、GitLab CI、Tekton、ArgoCD？
     Build tool：Maven、Gradle、Bazel、Make？
     Container build：Docker、Kaniko、BuildKit？
     有没有做过 build cache 优化？ -->

上面提到的，我们用了Jenkins（Master/Slave）, Tekton, Prow, Releaser(homegrown)，ArgoCD
Build的话，对于eBay application，因为主要是基于java的，所以用了Maven, 对于Cloud component，基于Go，我们用了Bazel。
Container build，主要是用Kaniko。

## Test Strategy in CI

<!-- e.g. CI 里跑哪些测试（unit / integration / e2e / performance）？
     测试耗时问题如何解决（并行、分片、selective run）？
     Flaky test 如何治理？
     Test coverage gate 怎么设定？ -->

CI 主要是跑unit test和integration testing，在CD的某些step会跑e2e和performance testing。
测试耗时的解决，主要是采用并行和selective run（eBay集成了一个commical production，帮助智能有选择的跑test cases）
Flaky test 的治理，首先identify是不是infra的问题，还是app的问题，infra的问题，我们对infra relability有要求，并且有自动retry的机制，对于app的问题，会对error log做AI analysis，建议user怎么修改，避免flaky test。
Test coverage gate整个公司有一个统一的标准，但是也会根据release的记录做调整，如果deploy经常失败，以及有incident产生，那么test coverage gate会提高，反之，如果一直success，那么对于一些小的rollout，会有选择的run test case，可能coverage也会低。

## Artifact Management

<!-- e.g. 用哪些 registry：Harbor、ECR、Artifactory、JFrog？
     Image tag 策略（commit SHA / semver / latest）？
     如何做 artifact promotion（dev → staging → prod）？
     有没有做 image scan（Trivy、Snyk）？ -->
我们是用ECR来管理image的，rollout到production的Image tag必须确定，commit SHA
promotion 是需要dev-staging-prod，会设定promotion policy，比如before deploy，build的image有test coverage gate，有image scan，从dev-staging会有额外的testing，integration，e2e等。
我们有自己的基于Anchors扩展的image scan tool （GIS - global info security ）提供
，用kyverno来管理pod policy，保证安全测试过的image deploy
## Deployment Strategies

<!-- e.g. 用过哪些发布策略：rolling update、blue-green、canary、feature flag？
     K8s 上怎么做 canary（Argo Rollouts、Flagger、Istio weight？）
     回滚机制是什么？自动还是手动触发？
     Release approval 流程怎么设计的？ -->
Deployment支持多cluster的rolling update，支持blue-grenn，canary和 feature flag
K8s做canary，我们有两种，一种是我们对于multiple clusters，我们有自己的controller，controller做orchesation，会控制部分cluster的部分pod到最新版本，然后check metrics（我们有自己的AI based health detector），然后决定是不是roll forward or roll back。rollback是根据health detector的siginal自动触发的。
Release approval的流程是通过各种的badge，比如通过了test coverage，那么有test coverage的badge，通过了PR review，有PR review的badge，然后每个step会定义需要有的badge。我们也定义了可视化的UI，让eBay developer可以修改定制他的pipeline。

## GitOps & CD Tooling

<!-- e.g. 用过 ArgoCD、Flux？怎么组织 GitOps repo？
     App-of-apps 还是 applicationsets？
     Sync policy：auto sync 还是手动？
     如何管理 multi-cluster / multi-env 的 CD？ -->

对于ECD，我们没有用GitOps，但是定义了CRD - Image，Mainifest CRD来表述artifact的状态。
对于cloud component，我们采用GitOps，将cloud component的yaml spec 按照environment/cluster放在特定的目录下，releaser会获取，进行deployment。

在ECD中，multi-cluster/multi-env，我们有federated deployment controller来管理mulitple-cluster，而对于multi-env，有deployment-template，也有environment metadata。CD会获取到environment的信息，替换template中的信息，产生正确的spec。

cloud component CD是用不同的git 目录来管理不同的environment和cluster spec的

## Security & Compliance in Pipeline

<!-- e.g. Secret 怎么注入（Vault、AWS Secrets Manager、sealed-secrets）？
     SBOM / supply chain security 有没有做过？
     如何做 image signing（cosign）？
     SAST / DAST / dependency scan 接在哪个阶段？ -->

Secret部分，eBay有自己的secret 产品，我们叫做trust fabric，提供了方案（细节待查）可以注入到pod中。
supply chain security有做的，对tekton做了一些增强，保证image signing，以及deploy的时候去验证这个signing。
SAST scan是接在staging pipeline，image build之后。

## Developer Experience & Velocity

<!-- e.g. 如何缩短 pipeline 耗时（parallel jobs、cache、incremental build）？
     有没有做 PR preview environment？
     Self-service deploy：工程师怎么触发部署，需要等 platform team 吗？
     有没有推过 DORA metrics（lead time、deployment frequency、MTTR、CFR）？ -->

我们推行了DORA metrics，并且综合定义了development friction，侧重在lead time，deployment frequency，rollout duration，rollback duration和success rate的提高。
为了缩短pipeline时间，我们采用了多种手段，build阶段，incremental build，selective test，parallel jobs for validation/security scan，去除manual 介入，blue/green rollout减少rolling upgrade的时间等。
部署完全是自动触发的，通过git的commit和merge就可以触发pipeline，不需要platform team的介入。

## Incidents & War Stories

<!-- e.g. 因为 CI/CD 导致过哪些 outage 或重大问题？
     怎么发现的、怎么处理的、事后做了哪些改进？
     有没有让坏代码漏进 prod 的经历，学到了什么？ -->
CI/CD导致过什么outage，不少
- Infra，CI/CD频繁call API server导致API server down，整个pipeline不work，解决方案，api server加了APF，CI/CD端加了gateway layer，queue了pipeline jobs，监控总的pipeline jobs。同时也可以加入自动retry机制，规避infra的问题。
- Infra，Tekton和Jenkins slave产生的K8s pod太多了，耗尽capacity，影响performance，解决方案，用了dedicated node pool，提高observailty
- framework base Image， 发布的base image有security 问题，导致所有app的image scan都通不过。对base image采用更严格的验证，才能发布。

## Key Principles I'd Defend in an Interview

<!-- 写 3-7 条你真正信服的原则，要有立场，不要泛泛而谈。
     e.g. "Trunk-based development 比 long-lived feature branch 更适合 platform team，
          因为……" -->

- DORA metrics driven, Velocity is the key
- Leverage on K8s solution and features to resolve CI/CD reliability/scalability issues
- Self service, customization, visualization
- Security is important,  wrong image will cause more damage for business

