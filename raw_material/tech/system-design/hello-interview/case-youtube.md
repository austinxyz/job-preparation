---
title: "Hello Interview — Case: YouTube"
source: "https://www.notion.so/1e4afa27ec7280f9a2e1d197e00a07a9"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - YouTube]]"
---

# Case: YouTube

## Key Design Questions & Answers

### How will users stream videos?

1. User uploads video → S3 notification event sent
2. Video processor watches video events: splits video into segments, converts segments to different formats
3. Segments stored in S3; video metadata DB updated
4. User sends watch request → video service returns video metadata
5. Client selects right encoded format based on network conditions (bandwidth, quality); downloads first segment from S3 directly
6. During video playing, backend continually downloads segments incrementally

### Handling poor/fluctuating network connections

1. Video processor splits video into segments and transcodes with different bitrates (360p, 480p, 720p, 1080p); updates manifest file with all bitrate format information
2. Client detects network quality and dynamically chooses/switches to suitable bitrates/formats
3. Downloads first segment to play; downloads remaining segments incrementally

**Adaptive Streaming Protocols**: HLS or DASH. Monitor after each segment: throughput, buffer fill rate. Switch thresholds (e.g., switch to lower resolution if throughput falls below 2 Mbps or buffer drops below 10 seconds). Hysteresis mechanism to prevent frequent switching.

### Severe network degradation fallback

1. Continue downloading segmentation until allowed to watch
2. Client pauses playback; shows downloading message
3. Retry with exponential interval; ask video service for other S3 URLs (CDN nearest links)
4. Downgrade video quality: audio only, or fixed frames

### Resumable uploads (chunked upload)

1. Client splits file into multiple chunks
2. Video service provides multiple presigned URLs per chunk ID; updates chunk information into Video Metadata DB
3. S3's multipart upload API with persistent upload ID (CreateMultipartUpload → UploadPart → CompleteMultipartUpload)
4. If upload interrupted: client calls video service → checks chunk status → returns only incomplete chunk URLs → client resumes

### Resume watching from where left off (across devices)

1. UserVideoRecord table: user ID + video ID + playedAt timestamp
2. Client sends heartbeat PUT calls to update playedAt regularly
3. User PAUSE/EXIT: client sends PUT with event type → video service updates UserVideoRecord
4. User switches devices: client queries UserVideoRecord by user+videoId → gets playedAt timestamp → finds suitable chunk → resumes

### Multiple devices watching simultaneously

Add device ID in UserVideoRecord + lastUpdatedAt to track latest device. Client can prompt user to select strategy: resume from this device's position or from latest device.

## CDN Considerations

- Specify edge locations in key regions (North America, Europe, Asia, Australia) with providers like Cloudflare, Akamai, CloudFront
- Cache invalidation: purge specific URLs, versioned URLs, stale-while-revalidate
- DNS-based routing or anycast IP addressing directs users to nearest edge
