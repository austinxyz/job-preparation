---
title: System Design Case - YouTube
category: tech/system-design
tags: [system-design-case, video-streaming, cdn, adaptive-bitrate, object-storage, chunked-upload]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - YouTube

## Knowledge Map
- 前置知识：S3 multipart upload, CDN architecture, adaptive bitrate streaming (HLS/DASH), video transcoding, presigned URLs
- 延伸话题：live streaming (vs. VOD), video recommendation systems, comment systems, monetization/ad serving, DRM
- 管理关联：

## Core Concepts

- **Upload → Transcode → Segment Pipeline**: Raw video upload triggers an async pipeline. The Video Processor splits the file into segments, transcodes each to multiple bitrates (360p, 480p, 720p, 1080p), stores segments in S3, and updates the metadata manifest. This separation means transcoding doesn't block the upload path.
- **Adaptive Bitrate Streaming (ABR) via HLS/DASH**: The manifest file lists all available bitrate formats. The client monitors throughput and buffer fill rate after each segment, switching quality based on thresholds (e.g., drop to lower resolution if throughput < 2 Mbps or buffer < 10s). Hysteresis prevents rapid quality oscillation.
- **Resumable Chunked Upload with S3 Multipart API**: The client splits the file into chunks and gets presigned URLs per chunk. S3's multipart upload API (`CreateMultipartUpload → UploadPart → CompleteMultipartUpload`) provides a persistent upload ID. On interruption, the client queries which chunks completed and only re-uploads incomplete ones.
- **Client-Side First Segment for Fast Start**: The client downloads and begins playing the first segment immediately while the rest loads incrementally in the background. Perceived startup latency is just the first segment download — not the whole video.
- **UserVideoRecord for Cross-Device Resume**: A table with `userId + videoId → playedAt timestamp`. The client sends periodic heartbeats and explicit PAUSE/EXIT events. On a new device, the client fetches this record and seeks to the saved timestamp.
- **CDN Multi-Region Distribution**: Edge nodes in key regions (NA, Europe, Asia, Australia). DNS-based routing or anycast IP directs users to the nearest edge. Cache invalidation: purge specific URLs, versioned URLs, or stale-while-revalidate. Versioned segments never need invalidation — they're immutable by construction.
- **Severe Network Degradation Fallback**: Client pauses playback and shows a loading message. Exponential retry with requests to the Video Service for alternative CDN URLs (geographically closer). Last resort: downgrade to audio-only or keyframe-only delivery.

## Key Questions

**Q: A user starts watching on mobile and switches to their laptop. How do they resume from the same point?**
Answer framework: UserVideoRecord table keyed by userId + videoId stores playedAt timestamp, updated via periodic client heartbeats and explicit PAUSE/EXIT events. On new device login, client queries this record, finds the correct segment index from the timestamp, and seeks to that position. Device ID + lastUpdatedAt in the record handles concurrent multi-device viewing.

**Q: A user's network drops from 50 Mbps to 0.5 Mbps mid-stream. Walk through what happens.**
Answer framework: After each segment, the ABR client measures throughput and buffer fill rate. At 0.5 Mbps, throughput falls below the threshold for even 360p. The client switches to the lowest bitrate immediately (with hysteresis to avoid oscillation). If buffer empties, playback pauses. Client retries with exponential interval and requests alternate CDN URLs from the Video Service. Fallback: audio-only or fixed-frame delivery.

**Q: How does transcoding work and why does the client need multiple bitrate versions?**
Answer framework: The Video Processor is triggered by the S3 upload event. It segments the video and transcodes each segment to multiple bitrates. Multiple versions are needed because different clients have different bandwidth capacities — forcing all users to download 1080p wastes bandwidth for mobile users and causes buffering on poor connections. The manifest file is the client's index of what's available.

**Q: How do you handle a large file upload that gets interrupted halfway?**
Answer framework: S3 multipart upload gives a persistent upload ID. The client tracks chunk status against that ID. On resume, it calls the Video Service to check which chunks already landed in S3 and only re-uploads the missing chunks. Presigned URLs per chunk are generated fresh so they don't expire during long uploads.

**Q: Why serve video directly from S3/CDN rather than through your application servers?**
Answer framework: Video segments are large, static, read-heavy blobs. Application servers would be a bottleneck and cost-inefficient. S3 presigned URLs allow the client to download directly from S3 or CDN. CDN edge nodes absorb the geographic latency and bandwidth load. Application servers only handle metadata (manifests, records), not bytes.

**Q: How would you handle a popular video going viral and hitting millions of concurrent views?**
Answer framework: CDN handles most of this — popular segments are cached at edge nodes worldwide. The bottleneck shifts to: metadata service (add Redis caching for video metadata), UserVideoRecord writes (partition by userId), and transcoding pipeline (queue-based async, not user-path). Monitor CDN cache hit rate; pre-warm CDN for known high-traffic events (new episode drops).

## Summary

YouTube's core challenge is delivering video at variable quality to users with different network conditions, across devices, without buffering. Functional requirements: upload, transcode, stream, resume across devices. Scale: billions of views, petabytes of storage, users on mobile in low-bandwidth regions.

The upload-to-stream pipeline separates concerns: S3 handles raw storage, an async Video Processor transcodes to multi-bitrate segments, and CDN delivers them globally. The client uses HLS/DASH adaptive bitrate streaming — measuring throughput after each segment and selecting the appropriate quality tier. This is the core non-obvious design: the client, not the server, decides video quality, based on local network conditions.

The interview tests whether candidates understand the full chain of decisions: why segment (fast start + quality switching), why presigned URLs (bypass app servers for blobs), why client-side ABR (server can't know client bandwidth), why multipart upload (resumability), and why CDN (geographic latency + bandwidth at scale). Cross-device resume and multi-device concurrent viewing are common follow-up probes.

## Key Terms

**Technologies**
- `HLS` · `DASH` · `S3 Multipart Upload` · `Presigned URLs` · `CDN (Cloudflare/Akamai/CloudFront)` · `Video Processor`

**Patterns**
- `Adaptive Bitrate Streaming (ABR)` · `Chunked Upload with Resume` · `Manifest File` · `Client-Side Quality Selection` · `Hysteresis for Quality Switching`

**Decision Points**
- `client-side ABR vs. server-directed` · `segment size trade-offs` · `CDN cache invalidation strategy` · `UserVideoRecord update frequency`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-youtube.md]]
