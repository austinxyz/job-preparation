---
title: Jenkins CI
category: tech/infra
tags: [jenkins, ci-cd, build-automation, pipeline, groovy, devops, kubernetes, casc, shared-library]
status: in-progress
priority: medium
last_updated: 2026-04-11
created_from_jd: "[[positions/Manager, DevOps Engineering - NVIDIA]]"
---

# Jenkins CI

## Knowledge Map
- 前置知识：CI/CD concepts, Groovy scripting, Git/SCM integration, Kubernetes basics
- 延伸话题：[[CI-CD Pipeline Engineering]], [[Kubernetes]], [[Developer Productivity and DORA Metrics]]
- 管理关联：build infrastructure ownership, developer productivity, migration strategy to modern CI systems

## Core Concepts

### Jenkins Architecture

**Traditional (standalone):**
- Single JVM process: Jenkins master handles scheduling, UI, plugin management, and job execution
- Agents (slaves): remote machines (physical/VM) that execute build steps; connected via SSH or JNLP
- Master is a SPOF — if it goes down, all CI stops

**Modern: Jenkins on Kubernetes (dynamic agents)**
- Master runs as a Kubernetes Deployment; agents are ephemeral pods spun up per job, destroyed after completion
- Kubernetes Plugin provisions agent pods dynamically from a pod template — no pre-allocated machines
- Benefits: elastic capacity (scale to zero between builds), build isolation (each build gets a clean pod), no agent inventory management
- Master still a SPOF for scheduling, but agent layer is fully elastic

**eBay CIaaS pattern:**
- Jenkins Master/Slave on Kubernetes, managed by a K8s CRD/operator
- On app onboarding: operator automatically creates Jenkins job config on the master
- On CI trigger: operator creates a slave pod, mounts the correct artifact volume for that app
- On build completion: slave pod is destroyed; artifacts persisted via mounted volume
- Kaniko used for container image builds inside pods (rootless, no privileged daemon required)

### Pipeline Types: Declarative vs. Scripted

**Declarative Pipeline** (recommended for most use cases):
```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: maven
                    image: maven:3.9-eclipse-temurin-17
                    command: [sleep, infinity]
                  - name: kaniko
                    image: gcr.io/kaniko-project/executor:debug
                    command: [sleep, infinity]
            '''
        }
    }
    environment {
        IMAGE_TAG = "${GIT_COMMIT[0..7]}"
    }
    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean package -DskipTests'
                }
            }
        }
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps { container('maven') { sh 'mvn test' } }
                }
                stage('Security Scan') {
                    steps { sh 'run-scan.sh' }
                }
            }
        }
        stage('Build Image') {
            steps {
                container('kaniko') {
                    sh """
                        /kaniko/executor \
                          --context=dir://. \
                          --destination=my-registry/app:${IMAGE_TAG}
                    """
                }
            }
        }
    }
    post {
        failure { slackSend(message: "Build failed: ${env.BUILD_URL}") }
        always  { junit 'target/surefire-reports/**/*.xml' }
    }
}
```

**Scripted Pipeline** (full Groovy, more flexible, harder to maintain):
```groovy
node('kubernetes') {
    stage('Build') {
        checkout scm
        sh 'mvn clean package'
    }
    if (env.BRANCH_NAME == 'main') {
        stage('Deploy') {
            // arbitrary Groovy logic
        }
    }
}
```

**Choose declarative when**: standard CI flow, readable Jenkinsfile, easier linting and validation.
**Choose scripted when**: complex conditional logic that declarative `when` clauses can't express cleanly.

### Shared Libraries

Shared libraries allow DRY pipeline code across hundreds of repos — define common steps once, import everywhere:

```
(shared library repo)
vars/
  buildAndPush.groovy   ← global var (callable as buildAndPush(...))
  runTests.groovy
src/
  org/myorg/Utils.groovy ← importable Groovy class
```

```groovy
// vars/buildAndPush.groovy
def call(Map config) {
    stage('Build Image') {
        container('kaniko') {
            sh "/kaniko/executor --destination=${config.registry}/${config.name}:${config.tag}"
        }
    }
}
```

```groovy
// Consuming Jenkinsfile
@Library('my-shared-lib@main') _

pipeline {
    agent { kubernetes { ... } }
    stages {
        stage('Build') { steps { buildAndPush(registry: 'my-ecr', name: 'myapp', tag: env.GIT_COMMIT) } }
    }
}
```

**Best practices:**
- Version shared libraries by Git tag/branch — `@Library('my-shared-lib@v1.2.0')` prevents breaking changes propagating to all pipelines
- Test shared library code with `JenkinsPipelineUnit` framework
- Keep shared library thin — policy/orchestration, not domain logic

### Configuration as Code (JCasC)

Jenkins Configuration as Code plugin (`configuration-as-code`) manages master config via YAML — eliminates manual click-through configuration:

```yaml
# jenkins.yaml
jenkins:
  systemMessage: "eBay CIaaS Jenkins"
  numExecutors: 0   # master runs no jobs itself
  clouds:
    - kubernetes:
        name: "kubernetes"
        serverUrl: "https://kubernetes.default"
        namespace: "jenkins"
        podRetention: "never"
        templates:
          - name: "maven-agent"
            label: "maven"
            containers:
              - name: "maven"
                image: "maven:3.9-eclipse-temurin-17"
                resourceRequestCpu: "500m"
                resourceLimitCpu: "2"
                resourceRequestMemory: "512Mi"
                resourceLimitMemory: "2Gi"

credentials:
  system:
    domainCredentials:
      - credentials:
          - usernamePassword:
              id: "registry-creds"
              username: "${REGISTRY_USER}"
              password: "${REGISTRY_PASSWORD}"
```

**Why JCasC matters at scale**: with hundreds of Jenkins jobs and plugin configurations, manual UI management is unscalable and unauditable. JCasC makes Jenkins config version-controlled, reviewable, and reproducible.

### Plugin Management at Scale

Jenkins has 1,800+ plugins — plugin management is a significant operational burden:

**Key plugins for K8s-based CI:**
- `kubernetes` — dynamic agent provisioning
- `configuration-as-code` — JCasC
- `git`, `github-branch-source` — SCM integration
- `pipeline`, `workflow-aggregator` — pipeline support
- `credentials`, `credentials-binding` — secret management
- `blueocean` (or `pipeline-stage-view`) — pipeline visualization
- `junit`, `jacoco` — test result publishing

**Plugin sprawl antipattern**: teams install plugins ad hoc → version conflicts, security vulnerabilities, upgrade complexity. Solution: maintain an approved plugin list in JCasC; require review before adding new plugins.

**Security updates**: Jenkins plugins have frequent CVEs. Pin plugin versions in JCasC, test upgrades in a staging Jenkins instance before applying to production.

### Jenkins Scaling and Reliability

**Horizontal scaling** — Jenkins master doesn't scale horizontally (single JVM, shared state). Mitigation strategies:
- Multiple Jenkins masters per business domain or team cluster (shard load)
- Reduce master load: offload artifact storage to external systems (Nexus, Artifactory, ECR), not master filesystem
- Minimize plugins: each plugin adds memory overhead and potential instability

**Vertical scaling**: master JVM heap size tuning — typical production masters need 4–8GB heap for hundreds of concurrent builds.

**Agent pool management:**
- Kubernetes plugin handles elastic scaling automatically — agents scale with build demand
- Set resource `requests` and `limits` on agent pod templates — prevents runaway builds starving other workloads
- Dedicated node pool for Jenkins agents (taint/toleration) — isolates build load from production workloads

**eBay reliability incidents (and fixes):**
- *API server overload*: Jenkins slave pod lifecycle calls (create/delete per build) hit API server at scale → added gateway/queue layer + APF rate limiting for CI traffic class
- *Node pool exhaustion*: concurrent slave pod creation exhausted shared node capacity → dedicated CI node pool with taints
- *Slave stuck in `Not yet online` state*: network/DNS issue between master and slave → added readiness probe timeout + automatic slave requeue

### Jenkins vs. Modern CI Alternatives

| Dimension | Jenkins | GitHub Actions | Tekton | GitLab CI |
|---|---|---|---|---|
| **Hosting** | Self-hosted (ops burden) | Hosted (or self-hosted runners) | Self-hosted (K8s-native) | Hosted or self-hosted |
| **Config language** | Groovy (Jenkinsfile) | YAML | YAML (TaskRun/Pipeline CRDs) | YAML |
| **K8s native** | Via plugin | Via self-hosted runners | Native (runs as K8s resources) | Via K8s executor |
| **Ecosystem** | 1,800+ plugins (powerful but sprawl) | GitHub Marketplace actions | K8s ecosystem | GitLab ecosystem |
| **Scalability** | Master is SPOF; complex at large scale | Scales well (hosted) | Scales natively (K8s) | Scales with runners |
| **Operator adoption** | High (legacy, widely deployed) | High (new projects) | Growing (platform teams) | High (GitLab shops) |
| **Migration cost** | — | Medium (rewrite Jenkinsfiles) | High (different model) | Medium–high |

**When to keep Jenkins**: existing investment in shared libraries and pipelines; plugin ecosystem dependencies; team expertise already deep in Jenkins.

**When to migrate away**: scaling pain exceeds migration cost; Groovy/plugin maintenance burden is significant; moving to GitOps-first CD model (Tekton + ArgoCD replaces Jenkins CD); new greenfield project (choose GitHub Actions or Tekton from the start).

**eBay migration direction**: Tekton replaced Jenkins for the CD layer (ECD); Jenkins/CIaaS retained for CI build layer with ArgoCD under evaluation for multi-cluster CD. Jenkins wasn't wholesale replaced — the CI build pattern (elastic K8s agents, Kaniko builds) was mature and working.

### Security Best Practices

- **Credentials**: use `credentials-binding` plugin to inject secrets as env vars or files — never hardcode in Jenkinsfile
- **RBAC**: Jenkins role-based access (Role Strategy plugin) — restrict who can configure jobs, approve deploys, access credentials
- **Script approval**: Groovy sandbox mode — scripts require admin approval to run unsafe methods; prevents arbitrary code execution
- **Agent security**: agents should not have elevated K8s RBAC beyond what the build needs; use separate service accounts per build type
- **Audit log**: enable audit trail plugin to track who changed what — essential for compliance
- **Network**: master should not be publicly accessible; agents access external registries through a controlled egress

## Key Questions

**Q: Explain the Jenkins Master/Slave architecture on Kubernetes. Why is this better than static VMs?**
Answer framework: Master handles scheduling, plugin management, UI — runs as a K8s Deployment. Slaves (agents) are ephemeral pods created on-demand by the Kubernetes plugin from a pod template, destroyed after the build completes. Advantages over static VMs: no idle capacity (agents scale to zero), build isolation (each build gets a clean environment), no agent inventory management, declarative pod templates version-controlled alongside pipelines. The tradeoff: master is still a single JVM SPOF — shard by domain if build volume requires it.

**Q: How do you manage Jenkins at scale across hundreds of teams? What are the biggest operational challenges?**
Answer framework: JCasC for reproducible, version-controlled master configuration. Shared libraries to avoid Jenkinsfile duplication across hundreds of repos. Approved plugin list to prevent plugin sprawl and CVE exposure. Dedicated agent node pools to isolate CI load. The biggest challenges: plugin version management (frequent CVEs, upgrade testing burden), master JVM tuning (heap size for concurrent builds), and API server pressure from agent pod lifecycle at scale — at eBay, we added a gateway/queue layer and APF to protect the API server from build traffic bursts.

**Q: When would you migrate away from Jenkins, and how would you approach it?**
Answer framework: Migrate when: scaling pain exceeds maintenance cost, Groovy/plugin burden is limiting velocity, moving to GitOps-first model where Tekton + ArgoCD is a cleaner fit. Don't migrate just because Jenkins is "old" — a well-tuned Jenkins with shared libraries and K8s agents works well. Migration approach: separate CI (build) from CD (deploy) concerns first; migrate CD to ArgoCD/Tekton (lower blast radius); migrate CI build to GitHub Actions or Tekton last (higher complexity, more team impact). At eBay, Tekton replaced the CD layer while Jenkins CI remained for the build layer — incremental, not big-bang.

**Q: What's the difference between declarative and scripted Jenkins pipelines? Which should you use?**
Answer framework: Declarative: structured YAML-like syntax, enforced by Jenkins parser, easier to lint and validate, most teams' needs are met. Scripted: full Groovy, arbitrary logic, more powerful but harder to maintain and audit. Default to declarative; use scripted only when `when` directives and `parallel` blocks can't express the logic cleanly. Mixed approach: declarative outer structure with `script {}` blocks for complex logic in specific stages.

**Q: How do you handle secret management in Jenkins pipelines?**
Answer framework: credentials-binding plugin injects secrets as env vars or temp files scoped to the pipeline step — secrets never appear in logs or Jenkinsfile. For Kubernetes-based agents, integrate with the cluster's secret management (Vault agent injector, External Secrets Operator) to avoid storing secrets in Jenkins at all — the agent pod gets the secret injected at runtime. Audit: enable audit trail plugin to track credential access. Never hardcode secrets in Jenkinsfile or shared libraries — they end up in Git history.

**Q: Jenkins agents on Kubernetes are creating too many pods and causing node pool exhaustion. How do you fix this?**
Answer framework: This is a resource isolation problem. Immediate fix: dedicated CI node pool with taints/tolerations — agent pods scheduled only on CI nodes, can't compete with production workloads for capacity. Medium-term: set resource requests/limits on agent pod templates so each build has a bounded footprint. Long-term: add a job queue / concurrency limiter in front of Jenkins (or use the Kubernetes plugin's `maxRequestsPerHost` and concurrency settings) to prevent burst job submission from overwhelming the node pool. At eBay, we also added API server APF rules specifically for CI traffic class to prevent agent lifecycle calls from degrading the API server.

## Summary

Jenkins remains the most widely deployed CI system in enterprise environments, primarily because of its 1,800+ plugin ecosystem and the deep organizational investment in shared libraries and pipeline configurations built over years. Its architecture — a central JVM master orchestrating ephemeral agents — maps well to Kubernetes: the Kubernetes Plugin provisions agent pods on-demand from pod templates, giving elastic capacity without idle compute, while Kaniko enables rootless container image builds inside pods. Configuration as Code (JCasC) is the operational cornerstone at scale, making master configuration version-controlled, reproducible, and reviewable rather than a click-through black box.

At eBay, Jenkins served as the CI layer of the CIaaS platform (the build half of ECD), managing CI for hundreds of application teams. The K8s-based elastic agent model worked well, but operating Jenkins at that scale surfaced two systemic issues: agent pod lifecycle calls created significant API server pressure during peak build windows (resolved with APF and a gateway/queue layer), and concurrent agent pod creation exhausted shared node pools (resolved with dedicated CI node pools and taints). The Tekton layer replaced Jenkins for the CD pipeline while Jenkins remained for CI builds — a deliberate separation of build from deploy that allowed each system to be optimized independently.

The honest assessment of Jenkins in 2025: it's not the right choice for new projects (GitHub Actions, GitLab CI, or Tekton are better starting points), but it's not worth wholesale replacing in established environments where the shared library investment and plugin ecosystem are providing real value. The migration path that makes the most sense is separating CI from CD: move deployment to ArgoCD/Tekton first (cleaner GitOps model, lower blast radius), evaluate CI migration separately when the Jenkins maintenance burden becomes a real velocity bottleneck. Groovy shared libraries, JCasC, and K8s dynamic agents are the three capabilities that make Jenkins viable at scale — organizations that haven't adopted these are carrying unnecessary operational debt.

## Raw Material
- [[raw_material/tech/infra/CI-CD Pipeline Engineering - personal]]
