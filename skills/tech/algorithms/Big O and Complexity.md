---
title: Big O and Complexity
category: tech/algorithms
tags: [algorithms, complexity, big-o, time-complexity, space-complexity]
status: stub
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Big O and Complexity

## Knowledge Map
- Prerequisites（前置知识）：
- Related Topics（延伸话题）：[[Sorting Algorithms]], [[Graph Algorithms]], [[Dynamic Programming]]
- Management（管理关联）：

## Core Concepts

**Big O Notation**
- Describes the upper bound on time/space complexity as input size grows; ignores constants and lower-order terms
- Common complexities (fastest to slowest): O(1) → O(log n) → O(n) → O(n log n) → O(n²) → O(2ⁿ)

**Common Data Structure Operations**
| Structure | Access | Search | Insert | Delete |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) |
| Hash Map | O(1) avg | O(1) avg | O(1) avg | O(1) avg |
| Binary Search Tree | O(log n) | O(log n) | O(log n) | O(log n) |
| Heap (binary) | O(1) peek | O(n) | O(log n) | O(log n) |

**Sort Algorithms**
| Algorithm | Best | Average | Worst | Space |
|---|---|---|---|---|
| Quick Sort | O(n log n) | O(n log n) | O(n²) bad pivot | O(log n) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Bubble/Insertion | O(n) | O(n²) | O(n²) | O(1) |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n+k) |

- Quick Sort worst case: already-sorted input with first-element pivot → O(n²); mitigated by random pivot selection
- Merge Sort: stable sort, good for linked lists or when guaranteed O(n log n) is required

**Heap**
- Complete binary tree; min-heap: parent ≤ children (peek min in O(1)); max-heap: parent ≥ children
- Insert/delete: O(log n) — heapify up/down; build heap from array: O(n) (heapify from bottom up)
- Use cases: priority queue, top-K problems (k smallest/largest in a stream), median finding (two-heap trick)

**LRU Cache**
- Implementation: doubly linked list (O(1) move to head/remove from tail) + hash map (O(1) lookup by key)
- get/put both O(1); evict LRU item from tail when capacity exceeded

**BFS / DFS**
- BFS: queue-based, level-order traversal; finds shortest path in unweighted graphs; use for "nearest" problems
- DFS: stack/recursion-based, pre/in/post-order; use for connectivity, cycle detection, topological sort
- BFS finds the nearest leaf node because it explores level by level (level-order guarantee)

**Consistent Hashing**
- Nodes and keys mapped onto a hash ring; key is served by the first node clockwise from its position
- When a node is added/removed, only the keys on that segment are remapped (vs. O(n) remapping in modular hashing)
- Virtual nodes: each physical node owns multiple positions on the ring → better load balance
- Use cases: distributed caches, CDN routing, database sharding

## Key Questions

**Q: What is the heap data structure? What problems does it solve? What's the Big O complexity?**
Answer framework: Min-heap / max-heap (complete binary tree); used for priority queues, top-K problems (maintain a heap of size K), median-of-stream (two heaps — max-heap for lower half, min-heap for upper half); insert/delete O(log n), peek O(1), heapify O(n).
> 中文提示：Top-K 用 size-K 堆；流式中位数用双堆（左大右小）；heapify 是 O(n) 不是 O(n log n)

**Q: Name several sort algorithms and their Big O complexity.**
Answer framework: Quick O(n log n) avg / O(n²) worst; Merge O(n log n) all cases (stable); Heap O(n log n) all cases (in-place); Bubble/Insertion O(n²); Radix O(nk). Know when to use each: Merge for stability, Heap for guaranteed O(n log n) in-place.

**Q: What's the average vs worst-case Big O for quicksort? How do you mitigate the worst case?**
Answer framework: Average O(n log n) with good pivot; worst O(n²) when pivot is always min/max (sorted input + first-element pivot). Mitigation: random pivot selection, median-of-three, or switch to Introsort (hybrid Quick + Heap for depth limit).
> 中文提示：已排序数组用首元素 pivot → O(n²)；随机 pivot 是标准解法

**Q: How do you implement an LRU cache?**
Answer framework: Doubly linked list (most recent at head, LRU at tail) + hash map (key → node pointer); get: lookup in map, move node to head, O(1); put: if key exists update + move to head; if at capacity, delete tail node + its map entry, then insert at head; all operations O(1).
> 中文提示：双向链表 + 哈希表；链表维护顺序（O(1) 插删），哈希表维护 O(1) 查找

**Q: What is BFS and DFS? Can you use BFS to find the nearest leaf node in a tree?**
Answer framework: BFS uses a queue, explores level by level → guaranteed shortest distance in unweighted graph; DFS uses stack/recursion, goes deep first. BFS finds the nearest leaf because it visits all nodes at distance d before any at distance d+1; first leaf encountered is shallowest.
> 中文提示：BFS 按层遍历，第一次遇到叶节点就是最浅叶节点

**Q: What is consistent hashing and why is it used in distributed systems?**
Answer framework: Hash ring maps both nodes and keys to positions; each key is served by the first clockwise node; adding/removing a node only remaps keys on one segment (vs. total rehash in modular approach). Virtual nodes solve uneven distribution. Real uses: Redis Cluster, CDN edge routing, Cassandra partitioning.
> 中文提示：普通取模增删节点重哈希整体，一致性哈希只影响一段；虚拟节点解决负载不均

## Summary

Big O and complexity analysis is the language of algorithm trade-off discussions. For infrastructure interviews, the most common coding patterns are: heap for top-K and priority problems, consistent hashing for distributed system design, LRU for caching implementations, and BFS/DFS for graph/tree traversal. Quick Sort is the workhorse sort but its O(n²) worst case on sorted inputs is a classic gotcha. Understand not just the formula but *why* — heapify is O(n) not O(n log n) because lower-level nodes do less work; LRU is O(1) because the doubly linked list avoids O(n) traversal for head/tail operations.

> 面试重点：能说清楚"为什么"是 O(x) 比背公式更重要；consistent hashing 是系统设计高频考点；LRU 双数据结构组合是经典实现题

## Raw Material
