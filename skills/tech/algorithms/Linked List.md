---
title: Linked List
category: tech/algorithms
tags: [linked-list, data-structures, algorithms, two-pointers]
status: draft
priority: medium
last_updated: 2026-04-11
created_from_jd:
---

# Linked List

## Knowledge Map
- 前置知识：Pointers / references, recursion basics
- 延伸话题：[[skills/tech/algorithms/Big O and Complexity]], Two Pointers, Recursion, Priority Queue / Heap
- 管理关联：

## Core Concepts

- **Node structure**: each node holds a value and a `next` pointer; doubly-linked lists also have `prev`. No random access — traversal is O(n).
- **Dummy head pattern**: prepend a sentinel node (`dummy.next = head`) to avoid edge-case handling when the result list's head might change (e.g., partition, merge).
- **Two-pointer (fast/slow)**: slow moves 1 step, fast moves 2 steps. Detects cycles (meet = cycle exists), finds mid-point, and — after meeting — finds cycle entry by resetting one pointer to head and stepping both at speed 1.
- **Floyd's cycle detection applied to arrays**: treats `nums[i]` as a "next pointer" to index `nums[i]`, converting duplicate-detection (LC 287) into a cycle-finding problem on an implicit linked list.
- **Reverse in-place**: iterative with `prev/cur/next` pointers is O(n) time, O(1) space. Recursive version: `head.next.next = head; head.next = null; return last` — elegant but O(n) stack space.
- **Merge k sorted lists**: use a min-heap (PriorityQueue) seeded with each list's head; repeatedly extract the min, append to result, and push its `.next`. Time O(N log k), space O(k).
- **Intersection of two lists**: equalize path lengths by having each pointer walk both lists (a→b, b→a) — they meet at the intersection node after at most m+n steps, no extra space needed.
- **Swap pairs / in-place re-link**: maintain `prev`, `first`, `second` pointers; re-wire as `second.next=first; first.next=second.next_original; prev.next=second` then advance `prev=first`.
- **Palindrome check without extra space**: find mid with slow/fast, reverse second half in-place, compare from both ends, restore if needed.

## Key Questions

**Q: Explain Floyd's cycle detection. How do you find the cycle entry point?**
Answer framework: Describe slow/fast pointer mechanics → prove they must meet inside a cycle → explain why resetting one pointer to head and walking both at speed 1 reaches the entry. Key insight: distance from head to entry equals distance from meeting point to entry.

**Q: How would you merge k sorted linked lists efficiently?**
Answer framework: Brute-force (merge pairwise) is O(Nk). Min-heap approach: push all k heads, pop min, push its next → O(N log k). State the tradeoff with divide-and-conquer merge (same complexity, simpler to reason about).

**Q: Reverse a linked list — iterative vs recursive, which do you prefer?**
Answer framework: Iterative is O(1) space, safe for large inputs. Recursive is cleaner but O(n) stack — can stack-overflow on very long lists. In production prefer iterative; in an interview, can show both.

**Q: Find the middle of a linked list in one pass.**
Answer framework: Slow/fast pointer — slow stops at middle when fast reaches the end. For even-length lists, clarify whether you want the first or second middle node (controls whether fast checks `fast.next` or `fast.next.next`).

**Q: Detect if two linked lists intersect, and find the intersection node.**
Answer framework: Length-difference approach (O(m+n) time, O(1) space) vs hash set (O(m+n) time, O(m) space). Dual-traversal trick (a→b, b→a) achieves O(1) space elegantly.

**Q: What invariants do you always maintain when doing in-place linked list manipulation?**
Answer framework: Save `next` before re-wiring; use dummy head to avoid null-head edge cases; always verify loop termination condition covers both even and odd lengths.

## Summary

Linked lists are a foundational data structure tested heavily in FAANG interviews because they expose pointer manipulation skills cleanly. The core operations — traversal, reversal, merging, cycle detection — each have canonical O(n) time / O(1) space solutions that reward internalizing a small set of pointer patterns rather than memorizing code.

The two most important patterns are the **dummy-head sentinel** (eliminates special-casing for head changes) and the **two-pointer / slow-fast technique** (solves middle-finding, cycle detection, and intersection in one pass). Floyd's algorithm specifically is worth understanding deeply: it appears in disguise on non-obvious problems like LC 287, where the array itself is reinterpreted as an implicit linked list.

For merge-k-sorted-lists, understanding the min-heap approach demonstrates knowledge of when to bring in auxiliary data structures for O(N log k) vs naïve O(Nk) — the kind of complexity trade-off conversation expected in system design and coding rounds alike.

## Raw Material
- [[raw_material/tech/algorithms/算法与数据结构笔记 - 链表]]
