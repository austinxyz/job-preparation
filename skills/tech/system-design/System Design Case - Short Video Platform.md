---
title: System Design Case - Short Video Platform
category: tech/system-design
tags: [system-design, video-platform, cdn, hls, presigned-url, transcoding, recommendation, cache-stampede, read-replica, back-of-envelope]
status: draft
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# System Design Case - Short Video Platform

## Knowledge Map
- Prerequisites（前置知识）：[[Cache and Consistency]], [[Message Queue]], [[NoSQL Databases]], [[Redis]], [[Sharding and Scalability]], [[Networking Fundamentals]]
- Related Topics（延伸话题）：[[GPU Cluster Management]], [[LLM Inference Optimization]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**Requirements Clarification — Interview Step 1（需求澄清）**
- Functional requirements: upload videos (≤500MB), scroll Feed (infinite scroll), play video (<2 sec start), like and comment
- Non-functional requirements: 500M DAU, read/write ratio ~1000:1, 99.99% availability, video start time <2 sec
- **Interview key statement**: TikTok is an extremely read-heavy system; the architecture focuses on using Cache + CDN to handle read pressure, with async message queues to decouple the write path

**Data Model（数据模型）**
- Video Metadata → relational database (sharded by video_id hash)
- Video File → object storage (S3): large binary files, not suitable for database storage
- User → relational database (structured, needs join queries)
- User → Video list → KV store (denormalized, O(1) lookup, message queue maintains eventual consistency)

**API Design — Key: Presigned URL（预签名 URL）**
- `POST /api/upload`: returns a **Presigned URL** (a temporary signed upload link from the server) — does not upload directly to the application server
- `PUT /{presignedURL}`: client uploads video file directly to S3, bypassing the application server — saves bandwidth and server load （客户端直传 S3）
- `GET /api/feeds`: returns a video list with **directly usable CDN Streaming URLs** — client can start prefetching immediately without extra requests

**Upload and Transcoding Pipeline（上传转码流水线）**
1. API service saves metadata (status=processing), returns Presigned URL
2. Client uploads directly to S3 (bypasses application server)
3. S3 upload completion event triggers a message queue
4. Transcoding service consumes the message: video is split into chunks and **transcoded in parallel** to multiple formats (360p/720p/1080p) + HLS
5. Transcoding complete → update metadata (status=ready) + update KV (user video list)
- Why async: transcoding takes minutes; synchronous blocking would freeze the upload endpoint; message queue decouples, failures can be retried

**Feed Playback Path（Feed 播放链路）**
- `User → API Gateway → Feed Service → Redis cache (hot metadata) → DB (on cache miss) → return video list with CDN URLs → client prefetches HLS chunks`
- 500M DAU → Redis caches hot video metadata (personalized Feed differs per user, caching the Feed list itself is not practical)
- **Cache Stampede**: a viral video's cache expires — massive requests flood DB → **Request Coalescing (Single Flight)** (one request rebuilds from DB, the rest wait for the result)
- **Hot Key**: a viral video creates a Redis hotspot → add read replicas for that key to distribute read traffic

**Database Sharding Design（数据库分片）**
- Shard by **video_id hash** (most even distribution; user_id sharding would overheat the shard containing popular creators; created_at sharding would overheat the current time shard)
- Querying a user's own video list → video_ids are spread across all shards, can't single-shard query → separate KV store (`user_id → [video_id list]`), O(1) lookup
- Two-phase writes (metadata DB + KV update) use a message queue for eventual consistency (video appears in personal home page a few seconds after upload — acceptable to users)

**Streaming Optimization — Sub-2-Second Start（视频秒开优化）**
- **HLS chunking**: video split into small chunks (2–10 sec); play starts while downloading; no need to wait for the entire file
- **CDN**: chunks cached at the nearest node (GeoDNS routing) （就近缓存）
- **Adaptive Bitrate (ABR)**: real-time network detection, dynamically switches between 360p/720p/1080p; degrades gracefully on poor network
- **Prefetching**: while the user watches video N, the system starts downloading the first few chunks of N+1/N+2 in the background; cost: wasted bandwidth if prediction is wrong

**Recommendation System（推荐系统）**
- **Implicit signals > explicit signals**: completion rate (most important), watch duration, skip behavior vs likes, comments (users may act randomly on those)
- **Two-stage pipeline**: Recall (simple rules, 10 billion → thousands of candidates) → Ranking (complex ML model, candidates → Top K); reason for two stages: scoring 10 billion videos with a complex model in real time is computationally impossible
- **Exploration vs Exploitation**: randomly insert 1–2 non-recommended-type videos into the Feed (avoids filter bubbles, discovers new interests, improves long-term retention) （探索与利用平衡）

## Key Questions

**Q: How should you design video upload to prevent the server from becoming a bottleneck?**
Answer framework: Presigned URL (server issues a temporary link, client uploads directly to S3); application server only handles metadata, not the video stream; S3 upload completion event triggers message queue; transcoding service consumes asynchronously (avoids synchronously waiting minutes for transcoding); chunked parallel transcoding reduces wait time.
> 中文提示：Presigned URL 让客户端直传 S3，绕过业务服务器；转码异步解耦，S3 事件触发消息队列

**Q: TikTok with 500M DAU — how do you guarantee video start time under 2 seconds?**
Answer framework: Four-layer optimization: ① HLS chunking (play while downloading, no need for the full file); ② CDN GeoDNS (nearest caching, reduces physical latency); ③ ABR adaptive bitrate (degrade quality on poor network); ④ Prefetching (preload the next video proactively); Feed API returns directly usable CDN URLs (client can prefetch immediately, no extra request needed).
> 中文提示：四层：HLS 分片 → CDN GeoDNS → ABR 自适应 → 预加载；Feed API 返回直接可用的 CDN URL

**Q: How do you handle Cache Stampede and Hot Key from a viral video?**
Answer framework: Cache Stampede (cache expires, massive requests flood DB) → Request Coalescing Single Flight (one request rebuilds from DB, others wait for the result — lighter and more direct than Circuit Breaker); Hot Key (excessive load on a single Redis shard) → add read replicas for that key to distribute traffic; two different problems in different scenarios — keep them distinct.
> 中文提示：Cache Stampede 用 Single Flight 单飞锁；Hot Key 用读副本分散流量；两种问题不同应对

**Q: How do you efficiently query a user's own videos when video_id hash sharding scatters them across the cluster?**
Answer framework: Denormalization: separate KV store (`user_id → [video_id list]`), O(1) lookup without scanning all shards; pay one extra write cost (write to both metadata DB and KV); use message queue for eventual consistency; accept that videos appear in personal home page a few seconds after upload (business-acceptable).
> 中文提示：反范式化独立 KV 存储换 O(1) 查询；消息队列保最终一致性；接受几秒延迟

**Q: Why does the recommendation system split into recall and ranking stages? Why is completion rate more important than likes?**
Answer framework: Scoring 10 billion videos with a complex model in real time is computationally impossible; Recall first (simple rules, fast) → Ranking then (complex ML, accurate); completion rate = implicit signal, it's a subconscious behavior (harder to game), more accurately reflects preference; likes are explicit signals, users may act randomly. Also mention Exploration (randomly inserting non-recommended videos) to avoid filter bubbles.
> 中文提示：两阶段原因是 100 亿视频无法全量精排；完播率是隐式信号，比显式点赞更准；Exploration 防信息茧房

## Summary

The short video platform system design covers nearly all core components — object storage, message queues, CDN, caching, sharding, recommendation systems — making it one of the most comprehensive topics in system design interviews. The core design philosophy is **read-write separation**: the read path (Cache + CDN to handle 1000x read traffic) and the write path (message queue for async decoupling) are completely independent and don't interfere with each other.

Number-driven design is the key habit: 500M DAU + 1000:1 read-write ratio → derive "need Redis caching + CDN + video_id hash sharding + 10B videos require sharding"; 99.99% availability → multi-AZ deployment + DB replica + CDN redundancy. Every technology choice should point to a specific numerical constraint, not intuition.

From an AI Infra perspective, the short video platform architecture maps to AI training/inference systems: ① video transcoding pipeline (async messages + parallel processing) ≈ distributed training pipeline (DataLoader + multi-GPU parallelism); ② recommendation system two-stage (recall + ranking) ≈ LLM inference two-stage (Prefill + Decode); ③ video CDN distribution ≈ model weight distribution to inference nodes; ④ Cache Stampede protection ≈ inference service request batching optimization. These mappings are the mental bridge from web system design to AI Infra thinking.

> 面试重点：Presigned URL → 转码异步流水线 → Feed 读路径（Redis+CDN）→ Cache Stampede 单飞锁 → 推荐两阶段（召回+排序）→ 数字驱动每个技术决策

## Raw Material
- [[raw_material/tech/system-design/sd-douyin]]
