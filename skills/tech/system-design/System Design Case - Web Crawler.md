---
title: System Design Case - Web Crawler
category: tech/system-design
tags: [system-design-case, distributed-systems, message-queue, object-storage, deduplication, crawling]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Web Crawler

## Knowledge Map
- 前置知识：distributed queues, DNS resolution, object storage (S3), consistent hashing, bloom filters, hashing algorithms
- 延伸话题：search engine indexing, PageRank, sitemap parsing, robots.txt compliance, URL deduplication at scale
- 管理关联：

## Core Concepts

- **Frontier Queue (BFS/Priority Queue)**: The central scheduling mechanism. Seed URLs → queue → crawl → extract new URLs → re-enqueue. The design challenge is making this queue scalable and avoiding repeated crawls.
- **Near-Duplicate Detection via SimHash/MinHash**: Exact hashing misses pages that are 80-90% similar (ads, timestamps, formatting). SimHash generates fingerprints where similar docs have similar hashes (Hamming distance). MinHash estimates Jaccard similarity. Both are far more storage-efficient than storing full content for comparison.
- **Shingling for Content Comparison**: Breaking documents into overlapping k-grams before applying MinHash. Enables set-based similarity comparisons that tolerate partial content changes.
- **Domain-Based Rate Limiting**: Without it, a crawler hammers social media sites while ignoring small sites. Domain-specific queues + work-stealing across queues balances load. Also required for robots.txt compliance.
- **Adaptive Crawl Frequency**: Static sites occasionally spike in activity (events, news). Monitoring rate-of-change per URL + anomaly detection lets the crawler temporarily increase frequency, then normalize — more efficient than uniform polling.
- **URL Metadata DB**: Tracks crawl status (pending, crawled, failed), last-crawled timestamp, crawl frequency. The state store that drives re-crawl scheduling decisions.
- **HTML → Text + URL Extraction Pipeline**: After fetching and storing raw HTML in object storage, a separate parser component extracts clean text (for indexing) and new URLs (for queueing). Keeping this separate from the fetcher allows independent scaling.

## Key Questions

**Q: How do you prevent re-crawling the same URL or near-duplicate content at scale?**
Answer framework: Two separate problems. Exact URL deduplication uses a distributed bloom filter or hash set (canonical URL normalization first). Near-duplicate content detection uses SimHash/MinHash after parsing — store fingerprints in metadata DB and compare before indexing new pages.

**Q: A domain has 10M pages and your crawlers are overwhelmed, while another domain has 50 pages and sits idle. How do you handle this?**
Answer framework: Domain-based partitioned queues with per-domain rate limits. Work-stealing allows idle crawlers to pull from overloaded queues. URL shuffling distributes pages across crawlers. Rate limits also enforce politeness (robots.txt).

**Q: How do you decide how often to re-crawl a given URL?**
Answer framework: Track rate-of-change per URL in metadata DB. Use exponential back-off for rarely-changing pages, more frequent polling for news sites. Add anomaly detection to catch sudden spikes (event coverage). Return to baseline once event passes.

**Q: Why store raw HTML in object storage rather than a database?**
Answer framework: HTML pages are large, unstructured blobs. Object storage (S3) is orders of magnitude cheaper per GB than databases and scales horizontally. Metadata (URL, status, timestamps) goes in a structured DB; the raw content is a blob that only the parser needs.

**Q: What happens when a crawler node dies mid-crawl?**
Answer framework: URLs should be leased from the frontier queue with a TTL (similar to SQS visibility timeout). If the crawler doesn't acknowledge success within TTL, the URL re-enters the queue. Metadata DB tracks in-flight status to prevent duplicate indexing on re-delivery.

**Q: How would you scale this to crawl 1 billion pages?**
Answer framework: Horizontally scale crawler workers behind the queue. Partition the frontier queue by domain hash. Use Cassandra or DynamoDB for metadata (wide-column, high write throughput). DNS caching at the crawler level reduces resolver load. CDN-aware crawling reduces latency to geographically distributed sites.

## Summary

A web crawler must continuously discover, fetch, and process web pages at scale, starting from seed URLs. Functional requirements include: crawling pages, extracting links, storing content, and supporting re-crawl scheduling. The core loop is: dequeue URL → DNS resolve → fetch HTML → store raw HTML → parse (extract text + URLs) → update metadata DB → enqueue new URLs.

The non-obvious architectural challenges lie in deduplication and scheduling, not in the fetching itself. Exact URL deduplication is solved with canonical normalization + bloom filters. Near-duplicate content detection requires SimHash or MinHash — critical because web pages frequently share 80-90% of content across different URLs (mirrors, timestamps, ads). A separate parser component after storage separates concerns and allows independent scaling of fetch vs. extraction throughput.

What makes this case tricky in interviews is the crawl scheduling dimension: static crawl intervals are wasteful. Production crawlers monitor per-URL rate-of-change and apply adaptive frequency with anomaly detection. Domain-based rate limiting is simultaneously a politeness requirement (robots.txt) and a load-balancing mechanism — interviewers probe whether candidates understand this dual purpose.

## Key Terms

**Technologies**
- `SimHash` · `MinHash` · `Shingling` · `Bloom Filter` · `S3 / Object Storage` · `DynamoDB / Cassandra` · `SQS / Kafka`

**Patterns**
- `BFS Frontier Queue` · `Work Stealing` · `Lease-Based URL Dequeuing` · `Near-Duplicate Detection`

**Decision Points**
- `exact dedup vs. near-dedup` · `adaptive crawl frequency` · `domain-based rate limiting` · `blob storage vs. DB for HTML`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-crawler.md]]
