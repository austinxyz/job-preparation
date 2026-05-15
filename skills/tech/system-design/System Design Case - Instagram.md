---
title: System Design Case - Instagram
category: tech/system-design
tags: [system-design-case, fan-out, social-feed, s3-presigned-url, multipart-upload, cdn, dynamodb, celebrity-problem]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Instagram

## Knowledge Map
- 前置知识：Fan-out on write vs fan-out on read, S3 pre-signed URLs, multipart upload, CDN invalidation, DynamoDB (partition key + sort key), feed generation at scale
- 延伸话题：[[System Design Case - Dropbox]] (large file upload with chunking), [[System Design Case - Tinder]] (pre-computed feed), [[System Design Case - WhatsApp]] (S3 media pattern)
- 管理关联：

## Core Concepts

- **Fan-out on write for normal users**: When a user posts, the Fanout Service proactively pushes the postId into each follower's Timeline table. At read time, `GET /feed` is a single indexed DynamoDB query — O(1) read cost regardless of how many accounts you follow. This is the standard approach for most users.
- **Celebrity exemption from fan-out**: Celebrities with >10K followers would generate millions of Timeline writes per post — write amplification makes fan-out impractical. Celebrity posts are stored separately in Redis (per-celebrity sorted set). At feed read time, the client merges the pre-computed timeline (for normal followees) with live celebrity posts from Redis.
- **Hybrid fan-out pattern is the key design insight**: The threshold (e.g., 10K followers) is configurable. Below threshold: fan-out on write (precomputed timeline). Above threshold: fan-out on read at query time, from Redis cache. This hybrid approach handles the 80/20 case efficiently without a single strategy breaking at scale.
- **DynamoDB Timeline table design**: `userId` as partition key, `createdAt+postId` as sort key. This enables efficient paginated feed reads sorted by recency — a range query on the sort key. Partition key is userId, so each user's timeline is co-located on one shard.
- **S3 pre-signed URL for media upload**: Post Service never handles media bytes directly. It generates a pre-signed URL from S3 with TTL (1 hour), returns it to the client, and the client uploads directly. S3 sends a completion notification; Post Service then marks the post as completed. This keeps Post Service bandwidth for metadata only.
- **Multipart upload for large files (up to 4GB)**: S3's multipart upload splits large files into 5-10MB chunks. Chunks upload in parallel (multiple pre-signed URLs). Failed chunks are retried independently with exponential backoff. Completion only after all parts are assembled by S3.
- **CDN with versioned URLs for media delivery**: Media files are served via CDN (CloudFront). For cache invalidation on updates/deletes, either use the CDN invalidation API (expensive, takes minutes) or use versioned URLs (`/media/v2/image.jpg`) — the old URL stays cached (stale but rarely accessed) and the new version is at a new URL.

## Key Questions

**Q: Why not use fan-out on read (pull model) for all users instead of a hybrid approach?**
Answer framework: Fan-out on read means `GET /feed` must query the Follow table (who does this user follow?), then fetch the latest posts from each followee — potentially hundreds of accounts. At Instagram scale, this is too slow and creates hot-reads on popular followees' post tables. Fan-out on write pre-computes this, making reads O(1). The celebrity exception is needed because fan-out on write creates O(follower_count) writes per post — millions of writes for a celebrity post.

**Q: How does the system determine when a user crosses the celebrity threshold?**
Answer framework: The Fanout Service can check follower count before deciding to fan-out. Alternatively, a background job classifies users as "celebrity" when their follower count crosses the threshold and updates a flag in the User table. The Fanout Service reads this flag and routes accordingly. Threshold crossing is a rare event, so occasional misclassification (fanning out for a user who just crossed the threshold) is acceptable.

**Q: How does the feed merge work for a user who follows both normal accounts and celebrities?**
Answer framework: `GET /feed` triggers two parallel queries: (1) Timeline table for the normal followee posts (DynamoDB range query by userId, sorted by createdAt); (2) Redis cache for each celebrity followee's sorted set (fetching recent posts). The Post Service merges both result sets by `createdAt`, then paginates. This merge is in-memory on the Post Service and is O(K log C) where K is page size and C is number of celebrity followees.

**Q: What happens if S3 doesn't send the completion notification?**
Answer framework: Two recovery paths: (1) the client sends an explicit confirmation to the Post Service after its direct upload completes; Post Service verifies with S3. (2) A Reconcile Service periodically queries Post DB for records stuck in `status=pending` and checks S3 for the corresponding object key — if it exists, the post is marked completed.

**Q: How do you handle a 4GB video upload that gets interrupted mid-way?**
Answer framework: Multipart upload tracks chunk status server-side (Upload Service stores per-chunk `status` and `fingerprint` in File/Post Metadata DB). On resume, the client sends its chunk info to the Upload Service, which returns only incomplete chunks' pre-signed URLs. The client re-uploads only those chunks. This works cross-device because chunk state is in the server's DB.

**Q: How does CDN cache invalidation work when a post is deleted?**
Answer framework: Option 1: Call CloudFront Invalidation API — deletes the cached item at all edge nodes, but takes minutes and costs per-call. Option 2: Versioned URLs — the deleted post's URL becomes a 404 after Post Service DB update; CDN still serves the old version until TTL expires (acceptable for soft-delete). Option 3: Short TTL (1-5 minutes) — cache naturally expires, acceptable for most content. For immediate removal (DMCA, safety), the Invalidation API is the only reliable path.

**Q: Why store both `userId` and `createdAt+postId` as partition/sort key in the Timeline table?**
Answer framework: `userId` as partition key means all of one user's timeline entries are on the same DynamoDB partition — enabling efficient range queries. `createdAt+postId` as sort key enables: (1) temporal ordering (feed is chronological), (2) uniqueness (two posts at same millisecond are distinguished by postId), (3) pagination cursor (use last seen sort key value as the "starting point" for the next page).

## Summary

Instagram's feed system is the canonical example of the fan-out pattern and the celebrity problem. The naive fan-out-on-write approach breaks for celebrities; the naive fan-out-on-read approach is too slow for high-follow-count accounts. The hybrid solution — fan-out on write for normal users, Redis-backed fan-out on read for celebrities — is the non-obvious design that makes both work.

The media upload flow (S3 pre-signed URLs, multipart for large files, S3 completion notifications, Reconcile Service for gaps) is a self-contained pattern that appears in Dropbox, WhatsApp, and other media-handling systems. Understanding this pattern end-to-end (including failure modes) is a high-value interview skill.

What interviewers are testing: deep understanding of the celebrity/write-amplification problem, ability to design a hybrid approach with a clear threshold and merge strategy, and knowledge of S3 pre-signed URL and multipart upload mechanics.

## Key Terms

**Technologies**
- `DynamoDB` · `S3 pre-signed URL` · `S3 multipart upload` · `CDN (CloudFront)` · `Redis sorted sets` · `Fanout Service`

**Patterns**
- `fan-out on write` · `fan-out on read` · `hybrid fan-out (celebrity exemption)` · `pre-signed URL media upload` · `chunked parallel upload` · `reconcile service for orphaned records`

**Decision Points**
- `fan-out on write vs fan-out on read vs hybrid` · `celebrity threshold` · `CDN invalidation API vs versioned URLs` · `S3 completion notification vs client confirmation`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-instagram.md]]
