---
title: Hello Interview — Case: Crawler
source: "https://www.notion.so/1eaafa27ec7280ce8be9cd5988a48e04"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Web Crawler]]"
---

# Case: Crawler

## High-Level Flow

1. Create Frontier Queue based on Seed URLs
2. DNS resolver to find IPs
3. Crawler fetches web pages and stores HTML pages into object storage
4. Update URL status into metadata DB
5. Extract text and URL from HTML page; store text data into object storage and put URLs into Frontier Queue
6. Repeat 1-5 until frontier queue is empty

## Key Deep Dive Points

### Near-Duplicate Detection

For near-duplicate detection: shingling (breaking content into overlapping n-grams) and locality-sensitive hashing (LSH) which groups similar items together. Unlike exact hashing, these methods detect when pages are 80-90% similar despite small differences in formatting, ads, or timestamps.

- **SimHash** — generates a fingerprint where similar documents have similar hashes; measures bit-wise Hamming distance
- **MinHash** — estimates Jaccard similarity between document sets
- **Shingling** — breaks documents into k-grams to compare overlapping content

Implementation: add a dedicated component after parsing that applies these algorithms, stores similarity metrics in metadata database.

### Load Balancing Across Domains

Some domains (social media) may have millions of pages while others have only a few. Without smart load balancing, crawlers assigned to popular domains become overwhelmed.

Strategies:
- Domain-based rate limiting
- URL shuffling across queues
- Work-stealing mechanisms where idle crawlers take tasks from overloaded ones

### Adaptive Crawl Frequency

Detect sudden changes in update patterns (e.g., normally static sites begin publishing frequent updates during special events). Implement by:
- Monitoring rate of change for each URL
- Anomaly detection algorithms to identify when update frequency deviates from historical pattern
- Temporarily increase crawl frequency; return to normal patterns once event concludes
