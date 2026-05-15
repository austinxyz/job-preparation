---
title: Hello Interview — Case: Instagram (Social Media Feed)
source: "https://www.notion.so/1f6afa27ec7280c6acedfbb8d03319dd"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Instagram]]"
---

# Case: Instagram (Social Media Feed)

## Key Design Questions & Answers

### Create Posts with Media

1. `POST /posts` → Post Service creates record in DynamoDB (status=pending)
2. Post Service calls S3 to generate pre-signed URL (TTL: 1 hour)
3. Returns pre-signed URL to user → client uploads directly to S3
4. S3 sends completion notification → Post Service updates status=completed + stores mediaURL

### Follow System

1. `POST /follow` (followUserId) → Follow Service
2. Creates `(follower, followee, createdTime)` record in Follow table (DynamoDB or PostgreSQL)

### Chronological Feed

**Fan-out on Write (with Celebrity Hybrid)**:
1. Normal users (<10K followers): on new post, **Fanout Service** listens to post queue → queries Follow table for followers → updates Timeline table (`userId, postId, createdAt`)
2. userId as partition key + `createdAt+postId` as sort key
3. Celebrity users (>10K followers): Fanout Service does NOT update Timeline table; instead stores celebrity posts in Redis cache (`celebrity → sorted set of posts`)
4. On `GET /feed`: Post Service queries Timeline table (paginated, sorted by `createdAt`) for normal followee posts + fetches celebrity followee posts from Redis cache → merges both lists

### Large-Scale Feed Generation

**Why Fan-out on Write for normal users**:
- Reading + merging thousands of accounts per request is too slow
- Pre-computed timeline enables O(1) feed reads
- Celebrity exclusion avoids write amplification (millions of follower feeds to update)

### Large Media Upload (Up to 4GB)

1. Post Service calls S3: create **multipart upload** (CreateMultipartUpload → per-chunk UploadPart URLs → CompleteMultipartUpload)
2. Client splits file into chunks (5-10MB each), uploads in parallel via pre-signed URLs
3. Progress shown to user; failed chunks retried with exponential backoff (max 7 days, then mark as failed)
4. S3 completion notification → Post Service updates mediaURL + status=completed
5. Reconcile Service periodically checks pending posts in Post DB → verifies S3 status → reconciles

### S3 Notification Failure Handling

1. Client sends update request to Post Service confirming upload completion
2. Post Service checks S3 for object key; if completed → updates post record
3. If S3 returns incomplete status → return failure; client retries upload
4. Reconcile Service handles orphaned pending records

### Fast Global Media Delivery

1. **Media Processing Service**: generates multiple resolution/format variants per upload (WebP for images, multiple bitrates for video)
2. **CDN** (CloudFront) globally distributed edge locations
3. Client selects appropriate variant based on device type (mobile/laptop) + network condition (WiFi/mobile)
4. TTL-based CDN cache; on update/delete: CloudFront invalidation API or versioned URLs (`/media/v2/image123.jpg`)
