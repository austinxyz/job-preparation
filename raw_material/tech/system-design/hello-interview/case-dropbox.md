---
title: "Hello Interview — Case: Dropbox (File Sync)"
source: "https://www.notion.so/1f8afa27ec728070b1a6f71fe9985170"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Dropbox]]"
---

# Case: Dropbox (File Sync)

## Key Design Questions & Answers

### Upload Files

1. Client sends `POST /files` → File Service creates metadata record (status=pending) in File Metadata DB
2. File Service calls S3 → gets pre-signed URL (expires in hours, user-specific)
3. Returns pre-signed URL to client → client uploads directly to S3
4. S3 completion notification → File Service updates status=completed + S3FileURL

### Download Files

1. `GET /files/:id` → File Service queries File Metadata DB for S3FileURL
2. Returns S3 URL to client → client downloads directly from S3 (CDN may cache for speed)

### Sync Local Changes to Remote

1. Client monitors local Dropbox folder via OS file system events → change queue (local DB)
2. Client calls Upload Service with file metadata → Upload Service updates status=pending + gets S3 pre-signed URL
3. Client uploads directly to S3 via pre-signed URL
4. S3 notifies Upload Service → updates metadata (status=completed, updatetime, S3FileURL)
5. Client receives success → updates local DB

### Sync Remote Changes to Local

1. Client periodically `GET /files?lastSyncTime=X` → Sync Service
2. Sync Service queries File Metadata DB: files with `updateTime > lastSyncTime` for this client
3. Returns changed file metadata list (including download URLs)
4. Client compares with local DB → downloads only changed files from S3
5. After download: client sends PATCH to update `lastSyncTime` in ClientSync DB

### Large Files (Up to 50GB) — Chunked Upload

1. Client splits file into 5-10MB chunks; calculates **fingerprint (hash)** per chunk
2. `POST /files` with file metadata + chunk info → Upload Service creates file record + chunk records (status=pending)
3. Upload Service calls S3 for separate pre-signed URL per chunk
4. Client uploads chunks in **parallel** via pre-signed URLs
5. S3 notifies on each chunk completion → Upload Service recalculates fingerprint to verify integrity; mismatch → return error, client re-uploads that chunk
6. On interruption: client gets chunk status from Upload Service → resumes only incomplete chunks
7. Cross-device resume: chunk status in File Metadata DB (server-side) → new device queries status → uploads only remaining chunks

### Resumable Upload After Network Interruption

1. Fingerprint (MD5/SHA-256) per chunk stored in File Metadata DB
2. On resume: client sends chunk info → Upload Service compares fingerprints → only returns incomplete chunks
3. S3 ETag compared to stored hash for integrity verification after each chunk

### Delta Sync (Bandwidth Optimization)

1. Server returns changed files after lastSyncTime + chunk fingerprints
2. Client compares chunk fingerprints with local DB: only chunks with different fingerprints need syncing
3. **Content-aware chunking** (Rabin fingerprinting / rolling hash): natural content boundaries rather than fixed offsets → insertions in middle of file don't shift all subsequent chunks
4. Compression (different algorithms per file type; skip already-compressed files like images/video)

### Real-Time Change Detection (Polling Strategy)

1. Active connection: reuse connection, server pushes notifications when `lastSyncTime < fileUpdateTime`
2. No active connection: client polls Sync Service at adaptive intervals (increases with idle time)
3. User-configurable high-priority files/folders: shorter polling intervals
4. **Desktop**: more frequent sync, longer WebSocket duration (better battery/bandwidth)
5. **Mobile**: user selects "important" folders; sync only high-priority content; longer intervals
6. Active users (>5 syncs in last 7 days) get higher polling frequency; file-type-based strategy (docs: high frequency; video: low frequency)
