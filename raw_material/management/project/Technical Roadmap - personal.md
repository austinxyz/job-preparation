---
title: Technical Roadmap - personal
source: personal experience + notes
date_saved: 2026-04-13
processed: true
skill_note: "[[skills/management/project/Technical Roadmap]]"
---

# Technical Roadmap — Personal Notes

> 这个文件用于收集 Technical Roadmap 相关的框架、思考和 experience。
> 内容齐了之后运行 `/raw-material-processor` 蒸馏进 skill note。

---

## 一、Roadmap 的本质是什么

<!-- 你怎么理解 roadmap？它是 plan 还是 commitment 还是 communication tool？
     你在 eBay 是怎么定义 roadmap 的 scope 和 horizon 的（quarterly? annual? rolling?）
     roadmap 和 OKR 的关系是什么？哪个先有？ -->

---
我觉得roadmap有不同的layer，比如north star roadmap是一个org/domain长远的规划，它是一个plan，也可以有yearly，quarterly的roadmap，那更多的是偏commitment，以及作为和stackhold，team communication的tool。通常是先有roadmap，在制订OKR，毕竟Key Result和delivery有很大的关系，但是OKR反过来也会影响下一步的roadmap

## 二、Prioritization 框架

### 理论框架

**常用方法：**
- **RICE**: Reach × Impact × Confidence ÷ Effort — 给每个 item 打分排序，适合 feature roadmap
- **MoSCoW**: Must Have / Should Have / Could Have / Won't Have — 快速分层，适合 scope cut 场景
- **Impact vs. Effort Matrix (2×2)**: 快速直觉分类；右上象限（high impact, low effort）= 立即做；右下（high impact, high effort）= 规划做；左象限 = 质疑是否做
- **Jobs to be Done**: 以"用户/客户在什么场景下需要完成什么任务"为单位，而非以 feature 为单位排优先级 — 避免做了功能但没解决问题

**Infrastructure/Platform 特有的优先级权衡：**

| 工作类型 | 优先级驱动因素 | 典型陷阱 |
|---|---|---|
| 可靠性/SRE | error budget 耗尽速率、SLO breach 频率 | 把 incident 修了就算完，不修根因 |
| 技术债 | 速度影响（lead time 增长）、onboarding 时间 | 技术债不可见，容易一直被 feature 挤掉 |
| 安全/合规 | deadline 驱动（监管）或 CVE severity | 往往是 reactive，缺乏 proactive roadmap |
| 平台新能力 | 用户需求信号、策略对齐 | 建了没人用（缺乏 golden path 和 adoption 计划）|
| 迁移/升级 | 风险窗口（EOL, K8s version support）| 低估迁移复杂度，没有 phased rollback 计划 |

<!-- 你自己怎么做优先级决策？有没有用过上面这些框架？
     eBay 有没有统一的 prioritization 工具或会议？
     当 feature 和 reliability 冲突时，你怎么做决定？有没有具体的例子？ -->

---
通常会Top down和bottom up结合，从整个组织的roadmap，从用户/客户出发，拿到要做的items，也会听取team member的意见，结合他们觉得重要的item，比如有些TOIL的工作，要转为platform的feature写到roadmap中，一些技术债。有了这些items，再根据Impact和Effort来打分，综合考量。
eBay company和org level的roadmap是通过airtable来进行管理的，中间层我们之前用monday来管理，现在有了AI之后，结合AI来定义Skills，skill会根据历史信息，和team member的input对effort有更准确的评估，形成markdown文件。然后结合infra team的特点，会预留一些buffer在可靠性/SRE中。
当feature和reliability冲突的时候，我会看reliability的impact情况，我们有buffer在可靠性和SRE，尽量用这个buffer，保证足够的invest在feature。如果relability对客户产生严重impact，那么会调整优先级，但是当前sprint先做mitigation，同时将长期修复转化为platform feature，plan在接下来的sprint中，尽量不影响当前的计划和roadmap。

## 三、Roadmap 结构与格式

### 常见 Roadmap 格式

**Now / Next / Later（推荐）：**
- Now：当前 quarter 在做的
- Next：下个 quarter 计划的（已有资源承诺）
- Later：6–12 月 horizon（方向性，未 committed）
- 优点：诚实表达不确定性；不给 Later 做虚假承诺

**Quarterly OKR-linked：**
- 每个 Objective 对应一个主题（reliability / platform velocity / AI infra）
- Key Results 是可测量的里程碑
- Roadmap items 挂在 KR 下

**Themes-based（适合 org-level roadmap）：**
- 不以 feature list 展示，而以主题/战略方向
- 利于跨团队对齐：每个 theme 解释"为什么这一年这件事重要"
- 具体 items 在 team level 展开

<!-- 你在 eBay 用的是哪种格式？roadmap 是季度的还是年度的？
     你是怎么把 platform 团队的 roadmap 和 application team 的需求对齐的？
     有没有遇到 roadmap 格式本身造成误解的情况（比如 Later 被当成 commitment）？ -->

---
我们有google doc 是org level的long term（3 years）roadmap，然后airtable item记录了年度季度的items，之后是用markdown文件来定义OKR，对每个key result定义efforts，作为季度plan之后，将确定的deliver的item create成JIRA epic和user story。会分成commit和stretch两种。

## 四、Stakeholder 管理与 Buy-in

### 理论要点

- **RACI（Responsible / Accountable / Consulted / Informed）**: 明确每个 item 谁 own、谁需要 consult、谁只需 inform — 防止"人人参与但人人不负责"
- **Pre-wiring（预热对齐）**: 重要决策在 1:1 里先 socialize，再到 group 会议确认 — 避免 group 场合的公开分歧
- **"Not in scope" list**: 主动维护、公开展示哪些东西不在这个 cycle 做 — 防止 scope creep，给 stakeholder 明确预期
- **依赖地图**: 大型 roadmap 一定要有明确的 cross-team 依赖图，ownership 清晰 — 否则阻塞时无人负责

### 向 leadership 汇报 roadmap 的原则

- 用业务语言，不用技术语言：不说"我们要升级 K8s"，说"我们要消除影响 eBay developers 日常部署的风险，timeline 是 Q2"
- 领先一个 quarter：Q1 开始就要开始 Q2 roadmap 的沟通，不要在执行前一周才对齐
- 风险透明化：主动说"这件事有这些风险，我的 mitigation 是这个" — 比被 leadership 发现风险更好
- 用数据支持：用 DORA、SLO、customer feedback 支持优先级决策，不依赖主观判断

<!-- 你在 eBay 有没有遇到 stakeholder 对 roadmap 的强烈分歧？怎么处理的？
     你是怎么向 VP/Director 汇报 technical roadmap 的？有没有具体的案例？
     有没有遇到 mid-year 需要大幅调整 roadmap 的情况？你怎么处理的（沟通、重新排优先级）？ -->

---
eBay采用RASCI Model来定义每个roadmap item的管理，会定义dependence，看谁依赖我们feature，我们依赖谁的feature，我们product manager会和客户有定期的沟通，了解他们全年的roadmap，知道大概的timeline，再我们做quarterly plan的时候会充分考虑，尽量满足客户的需求，但是如果真的有priorty和resource的问题，我们也会提前沟通，用数据说话- DORA,SLO，可能会对item进行拆解，先满足最重要的。如果我们的feature依赖于其他team，我们也会早于一个季度做沟通，会从对方的角度，创造win-win solution，会考虑plan B如果另一个team不能按时满足我们的要求。我们有weekly status update，给VP/Director 按照Delivery/Commitment/Blocker做简短update，特别是blocker部分，会寻求VP/Director的帮助。
有遇到mid-year要大幅调整roadmap，去年的DoJ/Jade project，因为和goverment的order有关，有hard timeline，也是年中的时候临时决定要build isolated environment。我做了大量对内，对外的沟通，重排优先级，和受影响的stakeholder做沟通，让他们这个是整个公司的策略调整，再对内也做调整。

## 五、我的 Experience 素材

### 5.1 Platform Engineering at Scale — 从 Ops 到 Platform 的 Roadmap 转型

**背景（已有 experience note）：**
- 200+ clusters, 5000+ apps, 50K nodes, 2M instances
- 每年：2 次 K8s 大版本升级、+33% 新 cluster、数百个 app onboard、每月 OS patching
- 手工 ops 方式已经到上限：每个新需求都要重写 automation，每次 incident 都靠少数人救火

**Roadmap 决策：**
- 核心判断：不能再在现有 ops 模式上"优化"，需要 mental model 的转变（ops thinking → platform thinking）
- Phase 1: declarative desired state — CRD + controller，工程师 spec 需求，平台自动 enforce
- Phase 2: 标准化 patch spec，支持 audit trail 和 AI 辅助生成 upgrade PR
- Phase 3: self-service validation platform，团队自行测 upgrade compatibility，不用排队等 central team
- Phase 4: admission webhooks + policy-as-code，把 guardrail 从 runbook 移到技术约束层

**结果：**
- 2 个工程师维护整个 fleet，zero incidents
- 月度 patching 和半年 K8s 升级变成常规非事件

<!-- 补充：
- 这个 roadmap 是怎么跟 leadership 沟通的？他们一开始是否 buy-in？
- 有没有遇到中途的阻力？比如某个团队不配合迁移到新模式？
- 这个 roadmap 大概持续了多少时间？你是怎么分阶段 commit 的（不是一次性 big bang）？ -->

---
因为 OS Patching和K8s Upgrade涉及到合规，leadership也是非常理解重要性，我三年前刚接手的时候，incident很多，所以要做合规和reliability的平衡，这个光靠Ops是不够的，从上到下有共识要从Ops到platform做转型, 所以我很容易得到了leadership的支持。
比较艰难的是在team member这边，他们之前incient频发，忙于应付，不太有信心来做这个的转化。我先identify了一个team member，她虽然不够资深，但是很有潜力，很有想法。我们先做platform breakdown，把upgrade分解为，build，validation和release 三部分。当时release很容易出问题，因为之前的validation没做好。我们先做validation platform，然后再做build patch标准化，最后做release的优化。根据这个框架来定义roadmap。是分阶段的commit。

declarative desired state — CRD + controller - 是在OS Patching项目做的

### 5.2 Engineering Velocity Program — 数据驱动的跨团队 Roadmap 执行

**背景（已有 experience note）：**
- 公司级 velocity 提升计划，CI/CD pipeline 最长需要一周
- 我负责 cloud infra 层：10+ 开发域、5 个 cloud infra 团队、3 个 platform 团队
- 目标：65% 应用达到 DORA elite tier，95th 部署时长 < 60 min，infra reliability > 99%

**Roadmap 方法：**
- 先做 metrics 分析确定真正的 bottleneck（不是拍脑袋）
- 发现 security policy initialization 是关键瓶颈，但只影响 ~5% 的应用
- 分三桶：无 security policy / 小 policy / 大复杂 policy
- 优先 fast win（95%），给 security team roadmap 解决大 policy（5%）
- 做了 phased agreement：immediate improvement + roadmap commitment for harder cases

**DORA 改善数据：**
- External（platform 侧）：2025 年 65% 应用达到 elite tier（deploy within 1 day, on-demand, sub-hour rollback, 95%+ success rate）
- 95th 部署时长从 >90 min 降到 75 min（excluding large-security-policy apps）

<!-- 补充：
- 这个 program 的 roadmap 是怎么跟 10+ development domains 沟通的？有没有统一的 roadmap 文档？
- 这个 program 最终是达到了全部目标吗？有没有哪个 item 没做完？为什么？
- 数据怎么收集的？是已有 dashboard 还是你们自己搭的？ -->

---
这是一个公司层面的program，每周有scrum of scrum，每个domain都有人参与。有统一的roadmap，而我们cloud infra的提升是作为其中很重要的一部分。
这个program达到了全部目标，DORA有了很大的提升，65% elite，但是涉及到复杂security policy部分的application，deploy duration还是比较长，不能达到elite。
公司有专门的DORA doshboard，也有统一的eBay CD平台，所以数据都是自动收集的。而作为infra team，我们会针对infra部分做进一步的breakdown，利用K8s的metrics/log/tracing的特性

### 5.3 Automated Cluster Management Overhaul — Vision 到落地的 Roadmap 管理

**背景（来自 raw_material/experience）：**
- 每年 20+ cluster build/decommission，每个需要 2 周到 1 个月
- 新硬件闲置、旧硬件高 discount，直接财务影响
- 现有流程：手工步骤 + 脚本，复杂且高风险

**Roadmap 决策：**
- 分三阶段：decommission（先做，风险最低）→ cluster build → tech refresh
- 从 decommission 先做：可以快速交付、证明方案可行、给 capacity team 早期价值
- 与 capacity team 谈判：换取他们在 transition 期间的耐心（给他们一个 self-service capability 的 timeline 承诺）
- 向 leadership 汇报进度以争取资源支持

**结果：**
- decommission 自动化完成，从数周缩到数天
- cluster build 主流程完成，支持 API gateway cluster 一周内完成
- 为未来 immutable cluster/infra capability 打下基础

<!-- 补充：
- 这个 roadmap 是多长 horizon 的规划？你是如何 balance 开发工作和日常 ops 工作的？
- Capacity team 是你的 customer 还是你的 dependency？这个关系怎么管理？
- 中途有没有 scope 变化？如何处理？ -->

---
这是一个跨度一年半的roadmap，要做整个cluster lifecycle management很复杂，我也没足够的人手，所以我们大约是40%在新feature开发，60%在目前的ops 工作做cluster management。我们先从一个容易改变的地方做，decommission，大约花了两个quarter，做出来的结果不错，就交给了capacity team用，他们是我们的客户，他们管理所有的clusters。以前只能等着我们做好，干着急，现在他们可以self service来decomm cluster。有了这个成功案例，做cluster build更复杂，我们先取得capacity team的支持，让他们只规划必须要build的cluster，剩余的delay一点时间，然后再和capacity team一起向leadership汇报decomm的成功进展，取得支持用更多的resource做cluster build
scope实际上是不断expand的，因为我们在成功的基础上做了更多的feature

### 5.4 DoJ/Jade Programs — 合规驱动的 Roadmap（外部 deadline 不可变）

**背景（已有 experience note）：**
- DoJ policy：covered persons 必须从 staging/prod 环境移除
- 需要：建两个新 cloud 环境（SDDZ、DCPX）+ 转移数千个 namespace/app + 保持现有 infra 正常运行

**Roadmap 特点：**
- 外部 deadline 固定（legal compliance，不可谈判）
- 三轨并行：Technical / Process / People
- 每轨有 owner + dependency graph
- 多轮 rehearsal 降低 cutover 风险
- 结果：按时完成，zero critical incidents

<!-- 补充：
- 这个 roadmap 是你单独制定的还是联合其他 team 一起做的？
- 三轨并行是怎么 coordinate 的？有没有某个轨成为瓶颈？
- 最大的风险是什么？你怎么 mitigate 的？ -->

---
这个也是公司层面的program，大的roadmap不是我制订的，但是时间紧，有很多unknown，好处是其他team都会配合。大的逻辑是，能技术解决的用技术解决，不然就是改变现有流程，最后才考虑人员调动，对于我们team，重点还是在techical，要怎么和其他团队协作快速的建两个新的cloud 环境。
最大的风险是unknown，所以我们break down每个子步骤，做了多轮rehearsal，确保cutover不会出问题。

### 5.5 Global Team Expansion — 人员 Roadmap（hiring + ramp-up）

**背景（已有 experience note）：**
- China team 失去 prod 访问权限后，US team 独自承担 24/7 on-call
- 3 个月内完成 Europe 和 India 团队的 hiring
- 6 个月内让新团队独立处理 production incidents

**Roadmap 方法：**
- 把 hiring + onboarding 当成 engineering project 来 manage：有 timeline、milestone、quality bar
- 标准化 hiring 流程（AI 辅助），不依靠每个 manager 自己摸索
- 建立文档体系（day-by-day ramp plan），让 ramp-up 可预测、可衡量
- 设定具体独立性目标（3 个月内独立处理 production incidents）并 track against it

**结果：**
- Europe：3 个月完成 hiring，3 个月后独立 on-call
- India：3 个月完成 hiring，正在 ramp
- 8+ engineers hired across two regions
- Hiring/onboarding framework 被其他团队采用

<!-- 补充：
- 这个 timeline 是你提出的还是 leadership 给的？有没有被压缩？
- 这种 people roadmap 和 technical roadmap 管理方式有什么本质不同？
- 3 个月的独立性目标是如何设定和追踪的？ -->

---
这个timeline是我根据leadership的期望设定的，同时也结合了现实的情况，US Team is not sustainable 承担24/7 on-call，但是我们平衡了tenant quality和time，并不是说为了满足时间要求就降低了招聘质量。
people roadmap需要很多的协调工作，而且有的时候取决于candidate的时间，remote也有很多unknown，需要根据情况很快做调整。
标准化体系可以控制质量。
3个月独立性目标还是和尽快不让US Team 24/7 oncall结合起来的。追踪的话，是一步步获取数据，比如1个月熟悉domain和runbook，knowledge没问题，1个月熟悉流程，1个月shadow。

### 5.6 SRE 可靠性 Roadmap — 从危机到稳定

**背景（已有 experience note）：**
- 接手团队：reliability < 90%，每周多次 critical incidents，24h+ 恢复时间
- 从零建立 SRE 实践：SLO/SLI、error budget policy、runbook、on-call rotation

**Roadmap 方法（graduated approach）：**
- 没有一次性 big bang 的目标，而是设计了 graduated targets
- SLO 从 99% 开始（不是 99.9%），因为从坏的 baseline 直接设 99.9% 会立刻 burn error budget，打击团队
- Error budget threshold 从 95% 开始，保守设定给团队时间了解系统行为
- 等 infra 稳定、团队对 methodology 有信心后，才 graduate 到更高 target（99% → 99.9%）

**结果：**
- 3 个月内 reliability 从 < 90% → 99%+
- Incident 恢复时间 24h+ → < 1h
- 6 个月后生产环境 99.9% sustained

<!-- 补充：
- 这个 SRE roadmap 是怎么跟 customer（eBay developers）沟通的？他们是否认可 99% 的初始目标？
- Error budget 政策是怎么用的？有没有具体的例子：burn rate 高了之后实际改变了优先级？
- 你怎么向 leadership 展示 SRE roadmap 的进展？用了什么指标？ -->

---
因为之前<90%, 用户的体验很差，所以他们觉得99%就是一个很好的进步。
error budget是看burn rate的，大于10倍的话就会被page，oncall就会优先处理
给leadership看Incident 的数量显著下降，customer feedback，最后才看SLI/SLO dashboard

## 六、Roadmap 执行中的常见挑战

<!-- 以下是常见挑战，请结合你的 experience 补充具体案例 -->

### 6.1 Mid-execution scope change
*Theory:* 当 scope 变化时，需要显式地重新 prioritize，而不是默默加进来。"加一件事"意味着"推一件事"，这个 trade-off 需要让 stakeholder 明确看到。

<!-- 你有没有遇到 leadership 要求临时加 scope 的情况？你是怎么处理的？ -->
为了DoJ/Jade project，我们只好推掉了不少plan的项目，比如ECR的upgrade

### 6.2 Tech debt vs. feature requests 的永久博弈
*Theory:* 技术债不可见，feature 可见。需要主动量化技术债的代价（lead time 增加了多少、incident 比例是多少）才能在 prioritization 会议中有说话的分量。

<!-- 你有没有成功争取到 tech debt investment 的经历？你是怎么 make the case 的？ -->
设定固定的比例给技术债

### 6.3 依赖团队未按时交付
*Theory:* 依赖管理：早期暴露依赖（roadmap 里显式标注），建立 early warning system（不要等 deadline 才发现 slip），有 fallback plan。

<!-- eBay 有没有某个大项目因为 dependency slip 而影响了你的 roadmap？你怎么处理的？ -->
cloud security team希望切换到新的security policy平台，对于已有应用的security policy性能优化他们放在比较低的优先级，影响了blue/green deployment的adoption。因为blue/green需要短期内新建大量的polices。
做了分类，除了很复杂的pool，让他们对一般的application的做了调优（这个不会化很多时间）

### 6.4 Roadmap 与实际交付差距过大
*Theory:* 如果每个 quarter 的 roadmap completion rate 都很低，说明 estimation 有问题、scope 管理有问题或 interruption 太多。DX Core 4 里的 "Stable priorities" 是高绩效团队的重要预测指标。

<!-- 你怎么追踪 roadmap completion rate？有没有采取过措施提高它（比如前面 AI-Augmented EM 里 OKR 从 50% 到 80% 的故事）？ -->

---
我们是根据OKR来评估completion rate，分为complete和parical complete，并且每个sprint的retro都会review risk。

## 七、Key Questions（待补充到 skill note 的 Q&A）

> 这些是当前 skill note 中缺少或需要加强的题目，结合上面的材料来写完整 answer。

**Q: Walk me through how you build a technical roadmap for your team. What's your process from start to finish?**
<!-- 从"理解 input（OKR/customer feedback/tech debt）"到"prioritize"到"format + communicate"到"track"整个流程。
     结合 Platform Engineering at Scale 或 Engineering Velocity Program 作为 anchor。 -->

**Q: How do you balance short-term reliability/maintenance work against long-term feature investments?**
<!-- 结合 error budget policy + SRE roadmap graduated approach。
     关键点：用数据（SLO burn rate、lead time 影响）量化技术债代价，让 trade-off 可见。 -->

**Q: Describe a time you had to significantly change course on a roadmap mid-execution. What happened?**
<!-- 结合 Engineering Velocity Program（security policy phased approach）或 DoJ/Jade（scope from China access change）。 -->

**Q: How do you get stakeholder buy-in for a roadmap that includes significant infrastructure investment with no visible user-facing features?**
<!-- 结合 Platform Engineering at Scale（ops → platform thinking 转型）或 Automated Cluster Management。
     关键点：translate to business impact（cost, risk, velocity）；use data；show graduated wins early。 -->

**Q: How do you manage a roadmap when there are multiple stakeholders with competing priorities?**
<!-- 结合 Engineering Velocity Program（CD vs Security standoff，phased agreement）。 -->

**Q: How do you plan a multi-year technical transformation (e.g., large-scale platform migration)?**
<!-- 结合 Cloud Migration to K8s 或 Platform Engineering at Scale。
     关键点：phase by risk（start where failure is cheapest）；有 rollback plan per phase；明确 done criteria per phase；早期交付 wins 建立信誉。 -->

---

## 八、补充材料（可继续粘贴）

<!-- 可以继续粘贴文章、书摘、想法。raw-material-processor 会一并处理。 -->
