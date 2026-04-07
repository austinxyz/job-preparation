---
title: Terraform 核心知识复习
source: internal
date_saved: 2026-04-06
processed: true
skill_note: "[[skills/tech/infra/Terraform]]"
---

# Terraform 核心知识复习

> 覆盖主题：概述（声明式 / Provider / DAG）→ HCL 语法（resource / variable / data / output / count / for_each）→ 生命周期（init → validate → plan → apply → destroy）→ State 管理（Remote Backend / S3+DynamoDB / 多环境隔离 / import）→ 模块化设计（目录结构 / 来源 / Provider 传入）→ 进阶特性（lifecycle / CI/CD / 工具链）

---

## 一、Terraform 概述

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 1 | 为什么用 Terraform 而不是手动点控制台或写 Shell 脚本？ | Terraform 是**声明式** IaC，描述期望的最终状态，有完整生命周期和工作流，**可重入、可验证**，比脚本（命令式）更可控；脚本只描述"怎么做"，不知道最终状态是否满足要求 | 声明式 vs 命令式；可重入；状态验证 |
| 2 | 声明式和命令式（脚本式）的本质区别？ | 声明式描述"希望达到的状态"，系统持续校验是否达到；命令式描述"如何做"，是一次性执行，无法感知结果状态；Terraform 的可重入性让多次运行结果一致 | 幂等性；最终状态收敛 |
| 3 | Terraform 如何同时支持 AWS / GCP / Azure 等 3000+ 平台？ | 引入 **Provider** 抽象层：Provider 是一套规范，各云厂商 / 社区 / 自研均可针对该规范实现；通过 **Terraform Registry** 发布和分发，用户在配置中声明后由 `terraform init` 自动下载，类似 npm install | Provider = 抽象中间层；Registry；init 下载 |
| 4 | Provider 是谁来维护？怎么引入到项目里？ | HashiCorp 官方提供部分，云厂商自己维护对应 Provider，也有社区和自研 Provider；通过 Terraform Registry 注册发布；在 `required_providers` 块中声明，`terraform init` 自动下载安装 | 官方 / 社区 / 自研；Registry；required_providers |
| 5 | Terraform 如何决定资源的创建顺序？什么是依赖图？ | Terraform 扫描资源定义中的**引用关系**自动发现隐式依赖，也支持 `depends_on` 显式声明；基于此构建 **DAG（有向无环图）**，按拓扑序执行；无依赖关系的资源**并行执行** | 隐式依赖（引用）；显式依赖（depends_on）；DAG；并行 |

---

## 二、HCL 语法

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 6 | `resource` / `variable` / `data` / `output` 各自职责是什么？ | **resource**：声明要创建/管理的资源；**variable**：用户可输入的参数（输入）；**data**：读取已存在的外部资源（只读）；**output**：暴露模块或配置的输出值 | resource = 管理；variable = 输入；data = 只读查询；output = 输出 |
| 7 | 如何在 `resource` 中分别引用 variable、另一个 resource、data 源？ | 引用变量：`var.变量名`；引用资源属性：`资源类型.资源名.属性名`（如 `aws_vpc.main.id`）；引用 data：`data.资源类型.资源名.属性`（如 `data.aws_ami.ubuntu.id`） | var.x；资源类型.资源名.属性；data.类型.名.属性 |
| 8 | `count` 和 `for_each` 批量创建资源有何区别？各自适用场景？ | **count**：给定数字，按索引 0~n-1 创建；**for_each**：按 key 迭代，引用当前元素用 `each.key` / `each.value`；**关键区别**：删除 count 中间某个元素，后续资源全部删除重建（高危！）；for_each 按 key 精确删除，更安全 | count = 索引；for_each = key；count 删中间元素触发重建 |
| 9 | 如何防止敏感变量（如密码）被打印到终端？变量传值优先级是什么？ | 用 **`sensitive = true`** 标记变量，输出时自动隐藏明文；传值优先级从高到低：**CLI `-var`** > **环境变量 `TF_VAR_变量名`** > **`*.auto.tfvars`** > **`terraform.tfvars`** > **默认值** > 交互式输入 | sensitive；TF_VAR_变量名；传值优先级 |

---

## 三、生命周期 / 工作流

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 10 | 拿到一份新的 `.tf` 配置，第一步应该运行什么命令？为什么？ | 先运行 **`terraform init`**：初始化工作目录、下载 Provider 插件、初始化模块、配置 Backend；不运行 init 直接 plan 会因缺少依赖报错 | init = 下 Provider + 下模块 + 初始化 Backend |
| 11 | `terraform plan` 输出的 `+` / `~` / `-` 分别代表什么？为何要加 `-out` 保存 plan 文件？ | `+` 新建；`~` 修改；`-` 删除；用 `-out` 保存 plan 文件可**固化**本次 plan 结果，apply 时严格按此执行，避免两次运行之间状态变化导致实际操作与预期不符 | +新建 ~修改 -删除；-out 固化 plan；防止状态漂移 |
| 12 | `terraform fmt -check` / `terraform validate` / `terraform plan` 三者有何层级关系？ | **fmt**：检查格式（纯本地，最轻）；**validate**：检查 HCL 语法逻辑（本地，无需访问云）；**plan**：需访问云 API 计算变更（重操作）；CI 流水线按此顺序做快速失败，把轻量检查放前面 | fmt = 格式；validate = 语法；plan = 调云 API；快速失败原则 |
| 13 | 绕过 Terraform 直接在控制台删除资源，下次 plan 会发生什么？什么是 State Drift？ | 真实资源和 State 文件不一致称为 **State Drift（状态漂移）**；下次 `terraform plan` 检测到漂移后会试图"修正"——可能在你不知情的情况下**重建资源**；应始终通过 Terraform 管理受控资源，可用 `terraform refresh` 同步真实状态到 State | State Drift；terraform refresh；绕过 Terraform 是危险的 |

---

## 四、State 管理

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 14 | 多人协作时 State 放本地有什么问题？需要解决哪三个维度？ | 本地 State 多人同时 apply 会冲突导致基础设施混乱；需要解决：① **存储**（集中共享）② **并发锁**（防止同时 apply）③ **加密**（State 内含敏感信息） | 存储 + 锁 + 加密 = Remote Backend 三要素 |
| 15 | AWS 技术栈下 Remote Backend 的标准方案是什么？ | **S3** 存储 State 文件 + **S3 SSE** 静态加密 + **DynamoDB** 提供分布式锁（`LockID` 主键）；这是面试必考的 AWS 标准方案 | S3 存储；S3 SSE 加密；DynamoDB 锁 |
| 16 | dev / staging / prod 三套环境如何隔离 State？目录隔离 vs Workspace 各有何适用场景？ | **目录隔离**：每套环境独立目录，可以用不同 Provider、不同代码，灵活性高，更安全，适合差异大的多环境；**Workspace**：同一套代码、不同 State（S3 key 加 workspace 名前缀，如 `env:/prod/terraform.tfstate`），适合差异小的多环境 | 目录隔离 = 灵活安全；Workspace = 同代码多 State |
| 17 | 如何将手动在控制台创建的资源纳入 Terraform 管理？State 记录丢失但云资源还在怎么处理？ | 手动资源纳入：**`terraform import`**（import 后 State 有记录，但 `.tf` 配置需手动补写，plan 验证无 diff 才算完成；Terraform 1.5+ 支持自动生成配置）；State 记录误删：用 **`terraform state rm/mv/list`** 等命令操作 State | terraform import；terraform state 系列命令；import 后必须补写 .tf |

---

## 五、模块化设计

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 18 | 什么是 Terraform 模块？标准目录结构包含哪些文件？ | 模块是**可复用的业务代码封装**；标准目录：`main.tf`（主逻辑）、`variables.tf`（输入变量）、`outputs.tf`（输出，遵循最小暴露原则）、`versions.tf`（版本约束）、`examples/`（示例）、`README.md`（说明文档） | main / variables / outputs / versions / examples / README |
| 19 | 模块有哪几种来源？各自版本管理有何差异？ | **本地目录**（`./modules/vpc`，无版本约束）；**Git**（支持版本 tag）；**S3 / HTTP 远端**（支持版本）；**Terraform Registry**（命名 / 参数 / 版本有严格规范，必须指定版本）；远端模块建议锁定版本防止漂移 | 本地 / Git / S3 / HTTP / Registry；远端必须锁版本 |
| 20 | 模块内应不应该声明 Provider？如何传入 alias Provider？ | **不应该**在模块内声明 Provider，否则失去复用性（Provider 带有特定参数如 region、credentials）；应由**调用方**传入；多 Provider 通过 `providers` 参数显式映射传入 alias Provider（如 `providers = { aws = aws.us-east-1 }`） | 模块内不声明 Provider；调用方传入；providers 参数传 alias |

---

## 六、进阶特性

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 21 | 如何防止生产 RDS 被误删？如何忽略外部对资源属性的自动修改？ | **`lifecycle { prevent_destroy = true }`**：设置后 destroy 操作会报错阻止删除；**`lifecycle { ignore_changes = [desired_size] }`**：忽略指定属性的变更，避免 Auto Scaler 等外部系统修改触发 diff | prevent_destroy；ignore_changes |
| 22 | 如何实现更新 EC2 AMI 时不中断服务（先建后删）？有什么注意事项？ | 使用 **`lifecycle { create_before_destroy = true }`**：先创建新资源、确认 Ready 后再删旧资源；注意新旧资源会短暂共存，可能触发**命名冲突**（如 Security Group 名唯一性约束），需配合 `random_pet` / `random_id` 加随机后缀 | create_before_destroy；短暂共存；命名冲突需随机后缀 |
| 23 | 如何将 Terraform 接入 CI/CD 流水线？PR 阶段和合并后分别跑什么？ | **PR 阶段**：`fmt -check` → `validate` → `init` → `plan`（只看不执行，供 Review）；**合并到 main 后**：`init` → `plan` → `apply`（自动部署）；只读检查前置，破坏性操作在合并后执行 | PR = 只 plan 不 apply；合并后 apply；快速失败前置 |
| 24 | CI/CD 流水线中有哪些第三方工具可以增强 Terraform 流程？ | **tflint**：代码规范 / 最佳实践检查；**tfsec / Checkov**：安全漏洞扫描；**infracost**：成本估算（在 PR 阶段预估变更费用）；**Atlantis**：PR 驱动的 GitOps 自动化工具，自动在 PR 评论中展示 plan 并触发 apply | tflint = 规范；tfsec/Checkov = 安全；infracost = 成本；Atlantis = GitOps 自动化 |

---

## 七、术语速查

| 术语 | 一句话解释 |
|------|-----------|
| **声明式 IaC** | 描述期望的最终状态，系统自动收敛，可重入幂等 |
| **Provider** | 针对某个云 / 平台的 Terraform 实现插件，通过 Registry 分发 |
| **Terraform Registry** | Provider 和 Module 的公共仓库，类似 npm registry |
| **DAG** | 有向无环图，Terraform 用它表示资源依赖关系和执行顺序 |
| **depends_on** | 显式声明资源依赖，Terraform 无法自动从引用推断时使用 |
| **resource** | 声明要 Terraform 创建 / 管理的云资源 |
| **variable** | 模块 / 配置的输入参数，支持 sensitive / validation |
| **data** | 只读查询已存在的外部资源或数据 |
| **output** | 暴露模块或根配置的输出值，可被其他模块引用 |
| **count** | 按索引批量创建资源，删除中间元素会导致后续资源重建 |
| **for_each** | 按 key 批量创建资源，用 `each.key`/`each.value` 引用，安全删除 |
| **sensitive** | 标记变量为敏感，输出时隐藏明文 |
| **TF_VAR_xxx** | 通过环境变量传入 Terraform 变量值的格式 |
| **terraform init** | 初始化工作目录：下载 Provider、模块、配置 Backend |
| **terraform plan** | 计算变更计划，+新建 ~修改 -删除；`-out` 可固化计划 |
| **terraform apply** | 执行变更，建议使用 plan 文件以防止中间状态漂移 |
| **terraform destroy** | 有序删除 Terraform 管理的所有资源（按依赖关系反向删除） |
| **terraform fmt** | 格式化 HCL 代码，`-check` 仅检查不修改 |
| **terraform validate** | 本地语法 / 逻辑校验，无需访问云 API |
| **terraform refresh** | 同步真实云资源状态到 State 文件，不做任何变更 |
| **State Drift** | 真实资源与 State 文件不一致的状态，plan 时会被检测并试图修正 |
| **Remote Backend** | 集中存储 State 的后端，解决多人协作的存储 / 锁 / 加密三要素 |
| **DynamoDB Lock** | 用 DynamoDB 实现 Terraform 分布式锁，防止并发 apply 冲突 |
| **terraform import** | 将手动创建的资源纳入 Terraform 管理，import 后需手动补写 `.tf` 配置 |
| **terraform state** | 操作 State 文件的命令集：rm / mv / list / show |
| **Workspace** | 同一套代码管理多套环境的 State，State key 自动加 workspace 名前缀 |
| **terraform_remote_state** | 跨项目读取另一个 Terraform 项目 Output 的 data source |
| **Module** | 可复用的 Terraform 配置封装，包含 main / variables / outputs 等文件 |
| **prevent_destroy** | lifecycle 参数，阻止资源被 destroy，保护关键资源 |
| **ignore_changes** | lifecycle 参数，忽略指定属性的外部修改，避免误 diff |
| **create_before_destroy** | lifecycle 参数，先建新资源再删旧资源，减少停机时间 |
| **tflint** | Terraform 代码规范和最佳实践静态检查工具 |
| **tfsec / Checkov** | Terraform 安全漏洞扫描工具 |
| **infracost** | Terraform 变更的云成本预估工具，可集成到 PR 流程 |
| **Atlantis** | 基于 PR 的 Terraform GitOps 自动化工具 |
