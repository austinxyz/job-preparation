---
title: Vector Databases
category: tech/ai-infra
tags: [vector-db, embeddings, ann, hnsw, ivf, lsh, similarity-search, rag, pinecone, pgvector, semantic-search]
status: draft
priority: high
last_updated: 2026-04-10
created_from_jd:
---

# Vector Databases

## Knowledge Map
- 前置知识：[[Distributed Systems]], [[Cache and Consistency]], embeddings / ML fundamentals
- 延伸话题：[[LLMOps and AI Pipeline Engineering]], [[Agentic AI Frameworks]], RAG systems, Elasticsearch, pgvector, Pinecone, Milvus
- 管理关联：AI Infra platform team scope, ML platform engineering

## Core Concepts

**What vectors (embeddings) are**
- An embedding is a fixed-length array of floats (128–3072 dims) that represents an object (text, image, user, product) such that semantically similar objects have geometrically close vectors.
- Typical sizes: OpenAI text-embedding-3-large = 3072 dims; many OSS models = 384–768 dims. A 1536-dim vector is ~6KB in float32.
- Similarity is defined by the embedding model, not the database. Pre-trained models capture "semantic" similarity; custom models can target domain-specific similarity (e.g., items bought together).

**Similarity metrics**
- **Cosine similarity**: angle between vectors, ignoring magnitude. Best for normalized embeddings (most text/image models normalize by default).
- **Dot product**: cosine × magnitudes. Slightly faster; used when magnitude encodes relevance (e.g., ranking models).
- **L2 (Euclidean)**: straight-line distance. Cares about both direction and magnitude; common for image search.
- **Hamming distance**: XOR bit count between binary vectors; extremely fast. Used in LSH schemes.
- Interview answer: "we'd use cosine similarity or whatever metric the embedding model was trained with" is almost always sufficient.

**The KNN problem — exact vs. approximate**
- Exact KNN: compare query against every vector; O(n) per query. For 1M vectors at 1536 dims = ~6B float ops/query. Too slow for most applications.
- **ANN (Approximate Nearest Neighbor)**: trade off a small accuracy loss for dramatic speed gain. Quality measured by **recall@K**: fraction of true top-K results actually returned. 95%+ recall is acceptable for most applications.
- The recall / latency / memory triangle: you can optimize any two at the cost of the third.

**HNSW (Hierarchical Navigable Small World) — the production default**
- Multi-layer graph where each vector is a node connected to its nearest neighbors. Upper layers are sparse ("express lanes"); Layer 0 is dense with all vectors.
- Search: start at top layer, greedily move toward query, drop to next layer when stuck, repeat; do thorough local search at Layer 0. Complexity: O(log n).
- Achieves 95%+ recall with sub-10ms latency. If you remember one indexing algorithm, it's this one.
- Cost: ~2× memory overhead (graph structure on top of vectors); slow index builds; insert overhead (new node must find its place and establish connections at each layer). Index quality can degrade with many incremental inserts.

**IVF (Inverted File Index)**
- Partitions vectors into clusters (k-means); at query time searches only `nprobe` nearest clusters. Higher `nprobe` = better recall but more work.
- Faster to build than HNSW; lower memory (no graph); handles inserts more gracefully (assign to cluster).
- Tradeoff: typically lower recall for the same latency, especially at cluster boundaries (high-dimensional space has many "edges").

**LSH (Locality Sensitive Hashing) and Annoy**
- LSH: random hyperplanes hash similar vectors to the same bucket (intentional collisions); multiple hash tables improve recall. Simpler, fast to build, good for Hamming distance / streaming data. Largely supplanted by HNSW in production.
- **Annoy** (Spotify): forest of random projection trees; immutable after build but supports **memory-mapping** (mmap) — index is a single file shared across processes, larger-than-RAM indexes possible. Good for static datasets updated in batches.

**Filtering and hybrid search**
- Most real queries require filters: "find similar products *that are in stock*".
- **Post-filter**: ANN first, filter results. Risk: don't find K results if filter is restrictive.
- **Pre-filter**: filter first, then ANN on subset. Risk: can't use index on arbitrary subset.
- Practical approach: most vector DBs (Pinecone, Elasticsearch kNN) integrate filtering into index traversal rather than doing it before or after. pgvector delegates to Postgres query planner.
- **Hybrid search**: combine vector similarity with keyword/BM25 scoring in parallel; merge results with a ranking function. Elasticsearch and Weaviate support this natively.

**Insert / update / index maintenance**
- HNSW inserts are expensive; frequent inserts degrade graph quality. Common pattern: maintain a small **"hot" index** (even a flat list for exhaustive search) for recent inserts + large **"cold" HNSW index** for older data. Queries search both and merge. Periodically merge hot → cold with a full rebuild.
- Updates = soft delete + insert. Soft deletes (mark as deleted) leave tombstones in the index that consume space and slow queries until rebuild.
- Index rebuild for 10M+ vectors can take hours. Strategy: rolling rebuild (build new index alongside old, then swap atomically), partitioned rebuild, or background reindexing.
- **Embedding drift**: changing the embedding model invalidates all stored vectors. Either re-embed everything or maintain parallel indexes during transition. Store model version with each embedding to detect mismatches.

**When to use which tool**
| Scenario | Recommendation |
|----------|----------------|
| Already on PostgreSQL, < 10M vectors | pgvector (HNSW or IVF) |
| Already on Elasticsearch | Elasticsearch kNN (+ hybrid search) |
| Redis in stack, low-latency needs | Redis Vector Search |
| Static dataset, memory-mapped sharing | Annoy |
| 100M+ vectors, dedicated vector search | Pinecone (managed) or Milvus (self-hosted) |
| Prototype / LLM / RAG | Chroma (simple to operate) |

Rule of thumb: **start with pgvector**. A dedicated vector DB adds operational overhead — reach for one only when extensions can't handle your scale or filtering requirements.

**Key numbers for interviews**
- Embedding dims: 128–1536 typical; OpenAI = 3072 max.
- Memory: 4 bytes/dim (float32). 1536-dim = 6KB/vector. 1M vectors ≈ 6GB raw; ~12GB with HNSW index.
- Query latency: 1–5ms common; sub-10ms achievable for in-memory indexes.
- Recall target: 95%+ typical; 99%+ possible at cost of latency/memory.
- Scale threshold: pgvector handles millions fine; dedicated vector DB for 100M+.

**Common gotchas**
- Vector DB is not a source of truth — it's an index. Authoritative data lives in the primary DB; vector DB is the similarity layer.
- Cold start: new users/items have no history to embed — need fallback strategies (popularity-based, content-based).
- Exact match ≠ vector search: if you need document lookup by ID, use a regular DB.
- Don't over-dimension: 128 dims is often sufficient. Bigger embeddings = slower search + more memory for marginal quality gain.

## Key Questions

**Q: What is a vector database and when would you use one instead of a traditional database?**
Answer framework: Define the problem — traditional DBs do exact lookups; vector DBs do similarity search ("find things like this"). Describe the core mechanism: embed data as high-dimensional vectors, then use ANN indexes to find nearest neighbors efficiently. Use cases: semantic search, recommendations, RAG, image similarity, deduplication. Key distinction: vector DB is an index, not a source of truth — authoritative data stays in the primary store.

**Q: How does HNSW work? Why is it the dominant algorithm?**
Answer framework: Analogy to skip lists — multi-layer graph with sparse upper layers (express lanes) and dense Layer 0. Search greedily navigates top-down, then does thorough local search at Layer 0. O(log n) complexity, 95%+ recall, sub-10ms latency. Why dominant: better recall/latency than IVF for most workloads, simpler than LSH for deployment. Cost: 2× memory, slow builds, expensive inserts. If you need fast builds or write-heavy workloads, IVF is the alternative.

**Q: How do you handle filtered vector search (e.g., "find similar items that are in stock")?**
Answer framework: State the problem — post-filter risks not finding K results if filter is restrictive; pre-filter can't use the ANN index on an arbitrary subset. Best approach depends on filter selectivity: for highly selective filters, pre-filter then brute-force on small set; for less selective, post-filter with oversample. Purpose-built DBs (Pinecone, ES kNN) integrate filtering into index traversal. Close with: "I'd benchmark with real data — filter selectivity varies too much to make a general rule."

**Q: Your team is building a RAG system for a knowledge base. Which vector database would you choose and why?**
Answer framework: Start with pgvector if already on Postgres — handles millions of documents, ACID, familiar tooling, one query joins vector results with metadata. If scale > 10M+ chunks or advanced filtering is central, consider Weaviate or Pinecone. For prototype / LLM-native stack, Chroma. State what drives the decision: existing infra, scale, filtering requirements, operational complexity budget. Never choose a dedicated vector DB if an extension suffices.

**Q: How do you handle embedding model updates in production?**
Answer framework: Changing the model invalidates all stored vectors (embedding drift). Strategy: store model version alongside each vector; build new index in parallel with old one; gradually migrate traffic (A/B or by query type); batch re-embed all documents; once migration complete, decommission old index. Key: never mix embeddings from different models in the same index — similarity scores become meaningless.

**Q: Explain the recall / latency / memory tradeoff in vector search. How would you tune it?**
Answer framework: Define recall@K (fraction of true nearest neighbors found), latency (query time), and memory (index size). HNSW knobs: `ef_construction` (build quality, affects recall), `ef_search` (search depth, affects recall vs. latency), `M` (graph connectivity, affects memory vs. recall). IVF knob: `nprobe` (clusters to search). Start with a recall target (e.g., 95%), benchmark index configurations, select the one that meets recall with lowest latency. If memory is the binding constraint, use quantization (float32 → int8) to compress vectors 4×.

**Q: How would you design a "similar products" recommendation feature at scale (100M+ products)?**
Answer framework: Embed all products offline in batch; store in dedicated vector DB (Milvus or Pinecone) given scale. Two-stage retrieval: (1) ANN search returns top-1000 candidates, (2) reranker model applies business rules (in-stock, user history, price filter) to select final top-N. Update pipeline: new products trigger embedding job → hot index; periodic batch rebuilds merge hot → cold. Discuss hot key risk if query distribution is skewed (popular categories). Mention eventual consistency: new products may not be searchable for minutes — acceptable for recommendations.

## Summary

Vector databases solve the nearest-neighbor search problem at scale: given a query embedding, find the K most similar vectors in a collection of millions or billions. The core mechanism is Approximate Nearest Neighbor (ANN) search — trading a small accuracy loss (measured by recall@K) for dramatically faster queries. HNSW is the dominant production algorithm, building a multi-layer graph with O(log n) search complexity and 95%+ recall. The recall / latency / memory triangle is the central design constraint: every tuning decision involves moving along one dimension at the cost of another.

For AI infra work, vector databases are load-bearing in three patterns: RAG (retrieve relevant document chunks before LLM generation), semantic search (natural language query → similar documents), and recommendations (find items similar to user behavior). In interviews, start with the simplest option: if you're already on PostgreSQL, pgvector handles millions of vectors with no additional infrastructure. Only graduate to a purpose-built vector DB (Pinecone, Milvus, Weaviate) when you're past 100M vectors or need advanced filtering capabilities that extensions can't provide. The operational overhead of another system is real.

Three gotchas to mention in interviews: (1) vector DBs are indexes, not sources of truth — authoritative data stays in the primary store, IDs flow back for the real data fetch; (2) embedding drift — a model upgrade invalidates all stored vectors and requires a costly full re-embed with parallel index migration; (3) filtering integration — pre/post filtering tradeoffs require real-data benchmarking, and most purpose-built vector DBs handle this in the index traversal layer rather than as a separate step. Understanding these separates candidates who've used vector DBs in production from those who've only read about them.

## Raw Material
- [[raw_material/tech/ai-basics/Vector Databases]]
