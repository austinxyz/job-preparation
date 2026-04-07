---
title: 系统设计复习：NoSQL 数据库
source: internal
date_saved: 2026-04-06
processed: true
skill_note: "[[skills/tech/system-design/NoSQL Databases]]"
---

# 系统设计复习：NoSQL 数据库

> 覆盖主题：NoSQL vs 关系型数据库（取舍原则）→ Cassandra 宽列模型（Partition Key / Clustering Key）→ 聊天系统表设计 → Hot Key / Salting → DynamoDB（Provisioned vs On-Demand）→ 选型决策框架

---

## 一、为什么需要 NoSQL

| # | 问题 | 核心答案 | 关键词 / 扩展点 |
|---|------|----------|----------------|
| 1 | 关系型数据库已经这么成熟，为什么还需要 NoSQL？ | ① **数据模型不适配**：字段不固定、文档型、图结构、KV 结构等不适合固定 schema 的关系型数据库；② **规模瓶颈**：每秒百万写入、PB 级数据量，关系型数据库难以横向扩展 | NoSQL = 数据模型灵活 + 天然横向扩展 |
| 2 | 关系型数据库也可以分库分表，NoSQL 和"手动分库分表的关系型数据库"真正的区别是什么？ | NoSQL **牺牲了 ACID**（强一致性 + 事务），换来分片的自动化和更好的扩展性。关系型数据库保留 ACID，分库分表需要手动设计，且跨分片事务极难处理 | **CAP 取舍**：大多数 NoSQL 选 AP（可用性 + 分区容错），关系型数据库选 CP |

---

## 二、Cassandra：宽列模型（Wide Column Store）

| # | 问题 | 核心答案 | 关键词 / 扩展点 |
|---|------|----------|----------------|
| 3 | Cassandra 的数据模型是什么？ | **宽列模型**：Keyspace → Table → Row → Column。每行可以有不同的 Column（不像关系型数据库每行 schema 固定） | Keyspace ≈ Database；每行 Column 可变 |
| 4 | Cassandra 为什么要把 key 分成 Partition Key 和 Clustering Key 两种？ | **Partition Key** 决定数据存在哪个节点（决定路由）；**Clustering Key** 决定同一 Partition 内数据的排序。两层查找：先找节点，再在节点内按序查找 | 先路由到节点，再二分查找定位记录 |
| 5 | 为什么 Cassandra 的写入性能极高？ | Cassandra 用 **WAL（Write-Ahead Log）**：写操作先顺序追加到日志，不需要随机写磁盘，大幅提升写并发量。只写不改，天然适合大量写入场景 | WAL = 顺序写日志 → 高写入吞吐；这是 Cassandra vs 关系型数据库的核心性能差异 |

---

## 三、Cassandra 聊天系统表设计实战

**需求**：查询用户 A 和用户 B 之间的聊天记录，按时间倒序排列

**表设计**：

| 字段 | 角色 | 理由 |
|------|------|------|
| `min(userA_id, userB_id) + "_" + max(userA_id, userB_id)` | **Partition Key** | 同一对话的所有消息存同一节点；用 min/max 排序保证 A→B 和 B→A 查询到相同 key，不会找不到数据 |
| `created_at DESC` | **Clustering Key** | 同一 Partition 内按时间倒序排列，查询直接返回，无需额外排序 |

| # | 问题 | 核心答案 |
|---|------|----------|
| 6 | Partition Key 用 `userA_id + userB_id`，但 B 发起查询用 `userB_id + userA_id` 会找不到数据，怎么解决？ | 用 `min(id1, id2) + "_" + max(id1, id2)` 作为 key，不管谁发起查询，生成的 key 相同 |
| 7 | 某用户和 10000 人都有聊天记录，所有对话都在同一 Partition，造成 Hot Key，怎么办？ | **Salting / Partition Splitting**：人为在 key 后面加编号后缀（如 `userA_001`、`userA_002`），每个后缀对应一批对话，把热点 Partition 拆分到多个节点 |
| 8 | Salting 后，查询用户 A 的所有对话列表需要查多个 Partition，怎么解决？ | ① **缓存**：把对话列表缓存到 Redis，降低查询频率；② **分页**：用户一次看不到所有对话，分页加载，减少每次查询的范围 |

---

## 四、DynamoDB vs Cassandra

| 维度 | Cassandra | DynamoDB |
|------|-----------|----------|
| 架构 | **去中心化**，所有节点平等，无主节点 | **AWS 托管**，基础设施由 AWS 管理 |
| 运维 | 需要专门基础设施团队，自己处理部署/扩容/故障 | 零运维，AWS 全托管 |
| 成本 | 可预测，团队规模大时更经济 | 按使用量计费，小团队方便但大流量可能昂贵 |
| 风险 | 自主可控 | **Vendor Lock-in**（被 AWS 绑定） |
| 选择时机 | 有强基础设施团队，需要完全控制 | 团队小/快速迭代/不想管运维 |

### DynamoDB 容量模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **Provisioned Mode** | 预先设定 RCU/WCU，价格便宜 | **可预测**流量，如每天固定高峰时段 |
| **On-Demand Mode** | 自动扩展，按实际使用量计费，价格贵 | **不可预测**突发流量，如偶发峰值（每年几次） |

> **判断原则**：峰值每年只出现 3 次 → On-Demand（峰值占比低，按需付费更省）；每天固定晚高峰 → Provisioned（可预测，提前配置更便宜）

---

## 五、NoSQL vs 关系型数据库：选型决策框架

**选关系型数据库（PostgreSQL / MySQL）**
- 涉及**钱、库存**等需要 ACID 事务（如订单、支付）
- 需要**复杂查询**和多字段索引（如多维度筛选）
- 数据之间关系复杂，需要 Join

**选 NoSQL（Cassandra / DynamoDB）**
- 数据量超大，需要**自动分片**横向扩展
- **写入量极高**（利用 WAL 顺序写）
- 数据结构灵活，**字段经常变化**（Schema-free）
- 查询模式**简单固定**（如按 Partition Key 直接查）

### 三系统对比

| 系统 | 数据 | 推荐选型 | 理由 |
|------|------|----------|------|
| **抖音** | Video Metadata | NoSQL（Cassandra/DynamoDB）| 100 亿视频，写入量大，查询模式固定（按 video_id） |
| **Ticketmaster** | 订单 / 支付 | **必须关系型** | 涉及钱，ACID 不可妥协 |
| **Ticketmaster** | 场馆信息 / 活动详情 | 关系型或 NoSQL 均可 | 数据量中等，查询不复杂 |
| **微信聊天** | 聊天记录 | **NoSQL（Cassandra）**| 消息量海量，按对话 Partition，最终一致性足够 |

---

## 六、术语速查

| 术语 | 中文 | 一句话解释 |
|------|------|-----------|
| Wide Column Store | 宽列存储 | NoSQL 模型，每行可有不同列，如 Cassandra |
| Partition Key | 分区键 | 决定数据存在哪个节点（路由） |
| Clustering Key | 聚集键 | 决定同一 Partition 内数据的排序 |
| WAL | 预写式日志 | 写操作先顺序追加日志，实现高写入吞吐 |
| Salting | 加盐 / 分区拆分 | 人为在 key 后加后缀，把热点 Partition 拆分到多个节点 |
| Provisioned Mode | 预置容量模式 | DynamoDB 预先设定读写容量，适合可预测流量 |
| On-Demand Mode | 按需模式 | DynamoDB 自动扩展，按实际使用量计费，适合突发流量 |
| RCU / WCU | 读/写容量单位 | DynamoDB 的计费和限流单位 |
| Vendor Lock-in | 供应商锁定 | 深度依赖某个云服务（如 DynamoDB），迁移成本极高 |
| ACID | 原子/一致/隔离/持久 | 关系型数据库事务保证，NoSQL 通常只支持最终一致性 |

---

## 七、面试答题习惯提醒

> AI 反馈：本节一个需改进的习惯：

1. **选型判断要主动说出具体标准，不要停在"看情况"**：面试官一定会追问。直接说："如果数据量超过 X 亿、写入量超过 Y/s，或者字段结构会频繁变化，我选 NoSQL；如果涉及事务、复杂查询或强一致性，我选关系型数据库。"用具体数字和场景支撑判断，不要等追问。
