---
title: System Design Case - Dropbox
category: tech/system-design
tags: [system-design-case, file-sync, chunked-upload, delta-sync, s3-presigned-url, content-addressable, fingerprinting, resumable-upload]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Dropbox

## Knowledge Map
- 前置知识：S3 pre-signed URLs, chunked/multipart upload, content-addressable storage, rolling hash (Rabin fingerprinting), CDN, adaptive polling
- 延伸话题：[[System Design Case - Instagram]] (S3 pre-signed URL + multipart upload), [[System Design Case - WhatsApp]] (S3 media pattern)
- 管理关联：

## Core Concepts

- **S3 pre-signed URL pattern for uploads and downloads**: The File Service never handles file bytes. For uploads, it generates a pre-signed URL and the client uploads directly to S3. For downloads, it returns the S3 URL (or CDN URL). S3 sends a completion notification on upload finish. This decouples file transfer from service load and keeps the File Service stateless relative to bytes.
- **Chunked parallel upload for large files (up to 50GB)**: Files are split into 5-10MB chunks on the client. Each chunk gets its own pre-signed URL. Chunks upload in parallel, dramatically reducing upload time vs. sequential. The server tracks per-chunk status in the File Metadata DB, enabling cross-device resumability.
- **Fingerprint (hash) per chunk for integrity and delta sync**: Each chunk's MD5/SHA-256 is stored in the File Metadata DB. On upload, the server verifies the received chunk's ETag matches the stored hash. On delta sync, the client compares its local chunk hashes with the server's stored hashes — only chunks with different hashes need to be transferred.
- **Content-aware chunking (Rabin fingerprinting / rolling hash)**: Fixed-offset chunking fails when content is inserted in the middle of a file — it shifts all subsequent chunk boundaries, making every downstream chunk "different." Rolling hash (Rabin fingerprinting) finds natural content boundaries, so an insertion only creates a new chunk boundary locally. This dramatically improves delta sync efficiency for edited documents.
- **Pull-based sync via lastSyncTime**: Remote-to-local sync uses a simple polling model: `GET /files?lastSyncTime=X` returns all files updated after time X. The client compares returned metadata with its local DB and downloads only changed files. After sync, the client updates `lastSyncTime` in the ClientSync DB. No persistent connection required.
- **Adaptive polling frequency based on activity**: Active users (>5 syncs in 7 days) get higher polling frequency. File-type-based strategy: docs sync frequently; videos sync infrequently. Mobile: user-selected "important folders" sync at high frequency; rest deferred. This balances responsiveness with battery/bandwidth conservation.
- **Reconcile Service for pending orphans**: Files stuck in `status=pending` beyond a timeout are checked by the Reconcile Service. It queries S3 for the object key's existence — if found, it marks the file completed. This handles the case where the S3 completion notification was lost.

## Key Questions

**Q: Why does content-aware chunking (Rabin fingerprinting) outperform fixed-size chunking for delta sync?**
Answer framework: Fixed-size chunking splits a file at byte offsets 0-5MB, 5-10MB, etc. If you insert 100 bytes at position 1MB, every subsequent chunk boundary shifts by 100 bytes. The server sees all downstream chunks as "different" from the stored hashes and retransfers them — even though most content is unchanged. Rabin fingerprinting uses content patterns to find natural boundaries, so an insertion only affects the local chunk, leaving all downstream chunks unchanged. Delta sync transfers O(change_size) bytes instead of O(file_size - change_position).

**Q: How does cross-device resumable upload work?**
Answer framework: Chunk status (pending/completed, fingerprint) is stored server-side in the File Metadata DB — not on the uploading device. When a new device (or the same device after reconnect) wants to resume, it sends the file metadata to the Upload Service. The Upload Service looks up per-chunk status in DB, returns only the pre-signed URLs for incomplete chunks. The client only uploads those chunks. The server-side tracking is the key: the state lives in the cloud, not on the device.

**Q: What's the difference between pulling changes with `lastSyncTime` vs WebSocket push?**
Answer framework: `lastSyncTime` polling is simpler, doesn't require persistent connections, and is resilient to client restarts (clients always know where they left off). The trade-off is latency between a remote change and local awareness — up to one polling interval. WebSocket push is lower latency but requires maintaining persistent connections (battery, network), and the server must track all active client connections. The design uses polling as the default but can reduce interval for active users.

**Q: How do you handle a scenario where two devices edit the same file simultaneously (conflict)?**
Answer framework: The design focuses on sync, not conflict resolution, but the standard approach is: the server accepts the last-writer-wins based on `updateTime`. Conflicted versions are saved as separate files (e.g., `document (John's conflicted copy 2026-05-14).docx`), and the user can manually merge. This is Dropbox's actual behavior. Operational Transform or CRDTs could provide automatic merge but add significant complexity.

**Q: Why use a client-side local DB (change queue) for detecting local file changes?**
Answer framework: The client monitors the local Dropbox folder via OS file system events (inotify on Linux, FSEvents on macOS, ReadDirectoryChangesW on Windows). Changes are buffered in a local SQLite DB (change queue). This decouples detection from upload: if the network is unavailable, changes queue locally and upload when connectivity returns. The local DB also serves as the record of `lastSyncTime` for the upload direction.

**Q: What are the bandwidth optimization techniques and when does each apply?**
Answer framework: Three techniques: (1) chunked upload with delta sync — only transfer changed chunks (applies to any file type, most impactful for large edited files); (2) compression — apply per file type (skip for already-compressed formats like JPEG, MP4); (3) adaptive polling frequency — reduces unnecessary network activity when files aren't changing. All three are complementary; delta sync has the highest impact for frequently edited documents.

**Q: How does the design handle storage deduplication across users?**
Answer framework: Not explicitly addressed in this design, but the standard approach is content-addressable storage: compute the hash of each chunk, use the hash as the S3 object key. If two users upload identical content, they share the same S3 object (deduplication). The File Metadata DB maps user file paths to chunk hashes. This is the basis for Dropbox's "online copy" feature (if another user already uploaded the same file, your upload completes instantly).

## Summary

Dropbox is a file synchronization system with two core challenges: handling large files (up to 50GB) efficiently and syncing changes across devices with minimal bandwidth. Both problems are solved by the same mechanism: chunking + per-chunk fingerprinting. Chunking enables parallel upload and partial resumption; fingerprinting enables delta sync (only transfer changed chunks) and integrity verification.

The non-obvious design insight is content-aware chunking via rolling hash. Fixed-size chunking is the obvious first approach, but its catastrophic failure mode on in-place edits (shifting all downstream chunk boundaries) makes delta sync useless for edited documents. Rolling hash boundaries make delta sync O(change_size) — exactly what bandwidth-sensitive mobile users need.

What interviewers are testing: understanding of the full file upload/sync lifecycle, knowledge of the rolling hash / Rabin fingerprinting technique, ability to design resilient resumable upload with server-side chunk tracking, and the trade-offs between push (WebSocket) and pull (polling) for remote change propagation.

## Key Terms

**Technologies**
- `S3 pre-signed URLs` · `S3 multipart upload` · `CDN` · `Rabin fingerprinting / rolling hash` · `MD5/SHA-256` · `SQLite (client-side local DB)`

**Patterns**
- `chunked parallel upload` · `per-chunk fingerprint` · `content-aware chunking` · `delta sync` · `lastSyncTime pull-based sync` · `adaptive polling` · `server-side chunk tracking for resumability`

**Decision Points**
- `fixed-size vs content-aware chunking` · `WebSocket push vs lastSyncTime polling` · `client-side vs server-side chunk state` · `deduplication via content-addressable storage`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-dropbox.md]]
