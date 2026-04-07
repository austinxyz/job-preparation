# 面试准备方法论

这套系统以 Obsidian 知识库为核心，结合 AI 辅助工具，帮助系统化地准备 AI Infra Manager 方向的技术面试。整个准备分三个阶段：**建立知识库 → 巩固知识 → 针对 JD 冲刺**。

---

## 第一阶段：建立知识库

> 目标：构建一个类 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 风格的个人知识库。
> 每个 skill note 都要能独立阅读，覆盖核心概念、常见面试问题和个人理解。

知识库结构分两大类：

- **Tech**：算法与数据结构 / 系统设计 / Infra / 软件工程 / AI 基础 / AI Infra
- **Management**：Behavior / People Management / Project Management

### 路径一：从 JD 出发，发现知识缺口

适合不知道该学什么的时候，用 JD 倒推需要掌握的知识点。

```
1. 把 JD 原文保存到 raw_material/positions/
2. 运行 /jd-importer → 生成 positions/ 笔记
3. 运行 /jd-analyzer → 自动识别 skill 缺口，创建 stub 笔记
4. 根据 stub 清单，去找对应的学习材料
5. 将材料保存到 raw_material/tech/ 或 raw_material/management/
6. 运行 /raw-material-processor → 提炼核心内容填入 skill note
```

### 路径二：从材料出发，主动积累知识

适合看到好文章或视频时，随手沉淀为可复用的笔记。

```
1. 将原文/笔记保存到 raw_material/ 对应子目录
2. 在文件 frontmatter 中填写 skill_note 字段（指向对应 skill 笔记）
3. 运行 /raw-material-processor → 提炼内容，自动更新 skill note
```

### Skill Note 状态流转

```
stub（空架子）→ draft（有内容）→ in-progress（持续完善）→ reviewed（面试就绪）
```

每个状态都有明确的"完成条件"和对应的操作：

#### stub → draft：填入核心内容

1. 根据 stub 的 `title` 和 `tags`，在网上找 1–2 篇高质量参考文章（推荐：官方文档、paper、知名博客）
2. 将原文保存到 `raw_material/` 对应子目录，设置 `skill_note` 字段
3. 运行 `/raw-material-processor` → Claude Code 自动提炼 Core Concepts、Key Questions、Summary，状态推进到 `draft`

**Claude Code 能帮什么：** 自动从原始材料中提炼结构化内容，不需要手动摘抄；识别知识图谱中的关联 skill，补充 Knowledge Map 的延伸话题。

#### draft → in-progress：加入自己的理解

1. 通读整篇笔记，检查内容是否准确、完整
2. 补充个人理解：类比、踩过的坑、与其他 skill 的关联
3. 把 Key Questions 里的答案框架用自己的语言改写一遍
4. 用费曼学习法测试自己（见下文第二阶段）

**Claude Code 能帮什么：**
- 追加更多面试高频问题（提示词：`"针对 [Skill]，补充 5 道 FAANG Senior EM 面试中可能追问的深度问题"`）
- 检查 Core Concepts 有无遗漏（提示词：`"以下是我对 [Skill] 的笔记，请指出有哪些重要概念没有覆盖"`）

#### in-progress → reviewed：验证开口能力

1. 不看笔记，用英文把整个 skill 从头讲一遍（费曼法）
2. 用 AI 模拟面试官追问（见第三阶段 Step 4）
3. 能流畅回答所有 Key Questions → 手动将 `status` 改为 `reviewed`

**Claude Code 能帮什么：** 扮演面试官做追问，发现表达上的逻辑漏洞；对英文回答做润色，提炼更专业的技术表述。

用 `_meta/index.md` 的 Dataview 表格随时查看整体进度和优先级。

---

## 第二阶段：巩固知识

知识库建好只是第一步，真正的准备在于能否**开口表达清楚**。以下四种方式递进使用：

### 1. Obsidian 复习

打开 `_meta/index.md`，根据 Dataview 表格按优先级逐条复习：
- 先看 `high priority + stub/draft`（最需要补充的）
- 再看 `reviewed`（维持熟悉度）

推荐用 Obsidian Graph View 浏览知识图谱，建立概念之间的关联感。

### 2. 费曼学习法（Feynman Technique）

> 核心原则：能用简单语言讲明白，才算真的懂。

详细方法和完整提示词模板见 → [[methodology/Feyman.md]]

**四种练习模式（配合 Claude）：**

| 模式 | 适合场景 | 简述 |
|------|---------|------|
| 扮演十岁孩子 | 第一遍学完，测试能否讲清楚 | Claude 扮演零背景学生，你来解释，它追问不清楚的地方 |
| 差距分析 | 自以为懂但讲不出细节 | Claude 通过循序渐进的追问定位你的逻辑断层 |
| 生成类比 | 概念太抽象、记不住 | Claude 提供生活化类比 + 出 3 道递进测试题 |
| 苏格拉底式对话 | 想真正搞懂原理 | Claude 只问"为什么"，不给答案，引导你自己推导 |

**最快的日常用法：**
> "我想通过费曼学习法掌握 [skill 名]。请扮演一名完全没有背景知识的 10 岁学生。我会向你解释这个概念，请在我解释后，指出我讲得不清楚的地方，或者问一些你觉得困惑的问题。"

### 3. 实战练习

| 工具 | 适合练什么 | 说明 |
|------|-----------|------|
| **LeetCode** | 算法题 | 重点练习 Medium 级别，注重讲解思路 |
| **Hello Interview** | 系统设计 + Behavior | 有 AI 面试官模式，支持计时练习 |
| **Growing** | 以上两个的日程管理 | 用 Growing 与 LeetCode / Hello Interview 联动，建立每日练习计划 |

建议节奏：算法题每周 3 题，系统设计每周 1 题，Behavior 每周梳理 1 个故事。

### 4. 提升英文表达

AI Infra Manager 面试以英文为主，流利表达和专业词汇同样重要。

**日常积累：**
- 每次用 raw-material-processor 处理材料时，**留意英文原文的表述方式**，特别是技术动词和短语（e.g. "horizontally partition", "evict stale entries", "back-pressure mechanism"）
- 把好的表述记录到 skill note 的 Key Questions 里，作为回答框架的一部分

**口语练习（配合费曼法）：**
- 用英文完整讲一遍 skill note，录音后回听
- 重点练：数字表达（"reduced latency by 40%"）、结构化回答（Situation-Task-Action-Result）

**AI 辅助润色：**
> 提示词模板：
> "以下是我对 [主题] 的英文解释，请帮我润色，保持技术准确性，让表达更自然，像 FAANG 面试中 Senior Engineer 的说话方式。[粘贴内容]"

---

## 第三阶段：针对 JD 冲刺

拿到目标 JD 后，系统给出一套从分析到模拟的完整流程。

### Step 1：分析 JD

```
raw_material/positions/ → /jd-importer → positions/ 笔记
positions/ 笔记 → /jd-analyzer → match score + gap 分析
```

根据 `match_score` 决定投入力度：

| 分数 | 建议 |
|------|------|
| `strong-matched` | 直接进入简历打磨和模拟面试 |
| `matched` | 补齐 in-progress 笔记，更新简历关键词 |
| `matched-with-gaps` | 优先攻克 high priority stub，针对性学习 2–3 周 |
| `not-matched` | 评估是否值得长期投入，暂不深入准备 |

### Step 2：基于 Gap 的学习计划

jd-analyzer 会生成 Prep Checklist，按以下顺序执行：

1. **stub（最优先）**：找材料 → raw-material-processor → draft
2. **draft**：补全 Key Questions，用费曼法讲一遍
3. **in-progress**：做 Hello Interview 实战练习
4. **reviewed**：用 AI 模拟面试做最终确认

### Step 3：简历针对性修改

jd-analyzer 的 Resume Tailoring 部分会给出：
- 关键词映射表（JD 词 → 简历改写建议）
- 建议强调的经历（按优先级排序）
- 建议弱化的内容

修改后用以下提示词做最终检查：
> "请对比这份 JD 和我的简历，指出还有哪些 JD 关键词没有体现，以及哪些地方表述可以更贴近目标职位语言风格。"

### Step 4：AI 模拟面试

运行 `/mock-interview`，支持三种模式：

| 模式 | 适合练什么 |
|------|-----------|
| `technical` | 针对某个 skill note 的技术深度问答 |
| `behavioral` | STAR 格式的管理经历问答 |
| `system-design` | 开放式系统设计题，全程由你主导 |

可选参数：指定 `positions/` 笔记（设定公司和角色语境）、目标 skill、难度级别（mid / senior / staff）。面试结束后自动给出 Strengths、Gaps 和英文表达建议。

---

## 辅助阅读

- **Karpathy LLM Wiki**：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  — 这个项目的 skill note 风格的主要参考，展示了如何用简洁的 wiki 风格覆盖 LLM 全栈知识
- **费曼学习法**：[[methodology/Feyman.md]] — 提示词模板和 Claude 结合用法详见此文件；原始方法论背景参考 [Farnam Street 指南](https://fs.blog/feynman-technique/)
- **Hello Interview**：https://www.hellointerview.com — 系统设计和 Behavior 题库，有 AI 面试官模式
