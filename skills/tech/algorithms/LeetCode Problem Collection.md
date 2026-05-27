---
title: LeetCode Problem Collection
category: tech/algorithms
tags: [leetcode, algorithms, data-structures, interview]
status: in-progress
priority: high
last_updated: 2026-05-27
created_from_jd: false
---

# LeetCode Problem Collection

## Raw Material
- [[raw_material/tech/algorithms/leetcode-collection]]

---

## Problem Table

### Linked List

| Problem | Key Approach |
|---------|-------------|
| [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Iterate both lists simultaneously carrying sum digit; handle remaining carry |
| [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Dummy result pointer; advance through both lists picking smaller value |
| [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Min-heap comparing node values; repeatedly extract minimum |
| [19. Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end/) | Dummy head; keep gap of N between fast/slow pointers to land on predecessor |
| [25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Recursive; grab successor head, set `head.next = successor` after reversing k nodes |
| [61. Rotate List](https://leetcode.com/problems/rotate-list/) | Reverse whole list, then reverse first-K and last-K segments separately |
| [82. Remove Duplicates II](https://leetcode.com/problems/remove-duplicates-ii/) | Fast/slow with prev tracker; or split into dup/noDup lists |
| [83. Remove Duplicates](https://leetcode.com/problems/remove-duplicates/) | Fast/slow pointers |
| [86. Partition List](https://leetcode.com/problems/partition-list/) | Two dummy lists (low, high); join at end, nullify tail |
| [92. Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/) | Recursive; advance to position m, then trigger reverse-k logic |
| [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Two-pass: create all new nodes in map; assign next and random |
| [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Fast/slow pointers; fast catches slow when cycle exists |
| [142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | Fast/slow meet, reset one to head, step both by 1; second meeting = cycle entry |
| [143. Reorder List](https://leetcode.com/problems/reorder-list/) | Store list in stack; alternate original forward nodes with reversed tail nodes |
| [160. Intersection of Two Lists](https://leetcode.com/problems/intersection-of-two-lists/) | Concatenate A+B and B+A; alignment makes them meet at intersection |
| [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Recursive: `head.next.next = head; head.next = null` |
| [234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | Recursive traversal with global left pointer compared against right (post-order) |
| [445. Add Two Numbers II](https://leetcode.com/problems/add-two-numbers-ii/) | Reverse both lists, then apply #2 approach |
| [876. Middle of Linked List](https://leetcode.com/problems/middle-of-linked-list/) | Fast/slow; slow is at middle when fast reaches end |

---

### Two Pointers

| Problem | Key Approach |
|---------|-------------|
| [1. Two Sum](https://leetcode.com/problems/two-sum/) | Hash map storing complement indices |
| [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Left/right pointers; move shorter side inward; track max area |
| [15. 3Sum](https://leetcode.com/problems/3sum/) | Sort, deduplicate, reduce to two-sum with left/right pointers |
| [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Fast/slow; slow advances only on unique values |
| [27. Remove Element](https://leetcode.com/problems/remove-element/) | Fast/slow; overwrite target elements in place |
| [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Left/right max arrays; water = min(leftMax, rightMax) - height |
| [75. Sort Colors (Dutch National Flag)](https://leetcode.com/problems/sort-colors-dutch-national-flag/) | Track p0 and p2; swap elements, handle p < p0 case |
| [80. Remove Duplicates II](https://leetcode.com/problems/remove-duplicates-ii/) | Fast/slow with count variable allowing up to 2 duplicates |
| [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | Two pointers from the end; fill in reverse |
| [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Strip to alphanumeric lowercase; left/right pointer check |
| [167. Two Sum II - Sorted Array](https://leetcode.com/problems/two-sum-ii-sorted-array/) | Left and right pointers; move inward based on sum vs target |
| [228. Summary Ranges](https://leetcode.com/problems/summary-ranges/) | Two pointers (start, end); extend end while consecutive; format range |
| [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Fast/slow; compact non-zeros, fill tail with zeros |
| [344. Reverse String](https://leetcode.com/problems/reverse-string/) | Left/right pointers swapping toward center |
| [392. Is Subsequence](https://leetcode.com/problems/is-subsequence/) | Two pointers on s and t; advance t for every match |
| [977. Squares of Sorted Array](https://leetcode.com/problems/squares-of-sorted-array/) | Left/right; place larger square from end |
| [986. Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | Advance pointer whose interval ends earlier; collect overlaps |

---

### Sliding Window

| Problem | Key Approach |
|---------|-------------|
| [3. Longest Substring Without Repeating](https://leetcode.com/problems/longest-substring-without-repeating/) | Window map tracks char counts; move left until no count exceeds 1 |
| [30. Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) | Sliding window with word-count maps; multiple starting offsets (0 to word length) |
| [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Shrink left when valid == need.size; track min window length and start |
| [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Shrink left while sum ≥ target; track min length |
| [219. Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | Use set; remove element at left when window exceeds k |
| [220. Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/) | Use TreeSet; check ceiling/floor within value range |
| [395. Longest Substring with At Least K Repeating](https://leetcode.com/problems/longest-substring-with-at-least-k-repeating/) | Enumerate 1–26 unique char counts; find longest window for each |
| [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Track max-freq char; shrink left when (window - maxFreq) > k |
| [438. Find All Anagrams](https://leetcode.com/problems/find-all-anagrams/) | Need/window maps + valid counter; record left index when valid == need.size |
| [567. Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Same as #438; return true when valid == need.size |
| [713. Subarray Product Less than K](https://leetcode.com/problems/subarray-product-less-than-k/) | Each valid window of size (right-left) contributes (right-left) subarrays |
| [1004. Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | Move left when zero-count exceeds k; track max window |
| [1658. Minimum Operations to Reduce X to Zero](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/) | Convert to finding longest subarray with sum = total - x |

---

### Binary Search

| Problem | Key Approach |
|---------|-------------|
| [4. Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Binary search on smaller array; partition to find median |
| [34. Find First and Last Position](https://leetcode.com/problems/find-first-and-last-position/) | Two binary searches: left boundary (tighten right) and right boundary (tighten left) |
| [35. Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Binary search; return left when target not found |
| [69. Sqrt(x)](https://leetcode.com/problems/sqrtx/) | Binary search in [1, x/2+1]; find largest mid where mid ≤ x/mid |
| [162. Find Peak Element](https://leetcode.com/problems/find-peak-element/) | Compare mid with neighbors to determine which side has a peak |
| [528. Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) | Prefix sum array; binary search for rightmost index ≥ random in [1, total] |
| [704. Binary Search](https://leetcode.com/problems/binary-search/) | Standard closed-interval binary search |
| [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Binary search on eating speed; minimize hours |
| [1011. Capacity to Ship Packages](https://leetcode.com/problems/capacity-to-ship-packages/) | Binary search on load; minimize days function |
| [1235. Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Sort by start; DP with binary search for next available job |
| [1539. Kth Missing Positive](https://leetcode.com/problems/kth-missing-positive/) | Linear scan comparing expected vs actual; adjust with remaining k |
| [410. Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Binary search on max subarray sum; minimize splits |

---

### Prefix Sum / Difference Array

| Problem | Key Approach |
|---------|-------------|
| [303. Range Sum Query](https://leetcode.com/problems/range-sum-query/) | Precompute prefix sums; query with `preSum[j+1] - preSum[i]` |
| [304. Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d/) | 2D prefix sum; inclusion-exclusion for rectangle queries |
| [1094. Car Pooling](https://leetcode.com/problems/car-pooling/) | Difference array on stops; capacity must not be exceeded at each position |
| [1109. Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/) | Difference array on flights; increment from `first` to `end-1` |

---

### Stack

| Problem | Key Approach |
|---------|-------------|
| [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Push matching closing brackets; pop and verify on each closing bracket |
| [71. Simplify Path](https://leetcode.com/problems/simplify-path/) | Push dir names; pop on `..`; ignore `.`; join remaining stack |
| [150. Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Push numbers; on operator pop two, compute, push result |
| [155. Min Stack](https://leetcode.com/problems/min-stack/) | Dual stacks; min stack records current minimum at every push |
| [225. Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/) | Track top; to pop, dequeue all but last element |
| [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | Two stacks (top, bottom); pour top into bottom on pop |
| [388. Longest Absolute File Path](https://leetcode.com/problems/longest-absolute-file-path/) | Use `\t` depth to manage stack; compute length on file nodes |
| [895. Maximum Frequency Stack](https://leetcode.com/problems/maximum-frequency-stack/) | freq-to-stack map + val-to-freq map; pop from highest-frequency stack |
| [933. Number of Recent Calls](https://leetcode.com/problems/number-of-recent-calls/) | Queue; poll all entries older than 3000ms window |
| [1249. Minimum Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/) | Stack of indices for `(`; unmatched `)` to delete list; remove all marked |

---

### Monotonic Stack

| Problem | Key Approach |
|---------|-------------|
| [402. Remove K Digits](https://leetcode.com/problems/remove-k-digits/) | Monotonically increasing stack; remove k elements from top; handle leading zeros |
| [496. Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | Build next-greater map from nums2; look up nums1 values |
| [503. Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | Double array for circular traversal; build next-greater map |
| [581. Shortest Unsorted Continuous Subarray](https://leetcode.com/problems/shortest-unsorted-continuous-subarray/) | Sort copy; find leftmost/rightmost where original differs from sorted |
| [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Monotonic stack storing indices; pop when warmer temperature found |
| [853. Car Fleet](https://leetcode.com/problems/car-fleet/) | Sort by position; compute arrival times; count increasing sequences from rear |
| [901. Online Stock Span](https://leetcode.com/problems/online-stock-span/) | Stack storing (value, span); accumulate span of popped elements |
| [1019. Next Greater Node in Linked List](https://leetcode.com/problems/next-greater-node-in-linked-list/) | Convert list to array; apply monotonic stack |
| [1475. Final Prices with Special Discount](https://leetcode.com/problems/final-prices-with-special-discount/) | Find next smaller price; subtract |
| [1944. Number of Visible People in Queue](https://leetcode.com/problems/number-of-visible-people-in-queue/) | Count elements popped from monotonic stack |

---

### Binary Tree

| Problem | Key Approach |
|---------|-------------|
| [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Pass min/max bounds down; return false if node violates bounds |
| [102. Level Order Traversal](https://leetcode.com/problems/level-order-traversal/) | Standard BFS level by level |
| [103. Zigzag Level Order](https://leetcode.com/problems/zigzag-level-order/) | BFS; alternate addFirst/addLast based on level parity |
| [104. Maximum Depth](https://leetcode.com/problems/maximum-depth/) | Depth = max(left, right) + 1 |
| [105. Construct from Preorder+Inorder](https://leetcode.com/problems/construct-from-preorderinorder/) | Preorder root first; find root in inorder to split left/right |
| [106. Construct from Inorder+Postorder](https://leetcode.com/problems/construct-from-inorderpostorder/) | Postorder root last; find root in inorder to split left/right |
| [107. Level Order Traversal II](https://leetcode.com/problems/level-order-traversal-ii/) | BFS with addFirst for reversed output |
| [114. Flatten to Linked List](https://leetcode.com/problems/flatten-to-linked-list/) | Flatten left/right; attach left subtree tail to right; set left = null |
| [116. Populating Next Right Pointers](https://leetcode.com/problems/populating-next-right-pointers/) | Traverse (node1, node2) pairs covering three sibling relationships |
| [117. Populating Next Right Pointers II](https://leetcode.com/problems/populating-next-right-pointers-ii/) | BFS with next pointer assignment |
| [129. Sum Root to Leaf Numbers](https://leetcode.com/problems/sum-root-to-leaf-numbers/) | DFS with accumulated numeric value; add at leaves |
| [144. Preorder Traversal](https://leetcode.com/problems/preorder-traversal/) | Standard preorder |
| [199. Right Side View](https://leetcode.com/problems/right-side-view/) | BFS record last element per level; or preorder DFS going right first |
| [222. Count Complete Tree Nodes](https://leetcode.com/problems/count-complete-tree-nodes/) | Compare left/right depths; if equal, subtree is full (2^level - 1) |
| [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Recursively swap left and right children at every node |
| [236. Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor/) | Return node if equals p or q; LCA where both left and right non-null |
| [257. Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths/) | DFS with path prefix; record when both children null |
| [297. Serialize and Deserialize](https://leetcode.com/problems/serialize-and-deserialize/) | Preorder with null nodes; or BFS level-order |
| [331. Verify Preorder Serialization](https://leetcode.com/problems/verify-preorder-serialization/) | Non-null: in -1, out +2; null: in -1; start edge=1, end at 0 |
| [337. House Robber III](https://leetcode.com/problems/house-robber-iii/) | Tree DP: each node returns (rob, skip); rob = val + grandchildren sums |
| [515. Find Largest Value per Row](https://leetcode.com/problems/find-largest-value-per-row/) | BFS; track max per level |
| [543. Diameter](https://leetcode.com/problems/diameter/) | Max diameter at node = left depth + right depth; global max variable |
| [637. Average of Levels](https://leetcode.com/problems/average-of-levels/) | BFS; average each level |
| [652. Find Duplicate Subtrees](https://leetcode.com/problems/find-duplicate-subtrees/) | Serialize each subtree (postorder); frequency map detects duplicates |
| [654. Maximum Binary Tree](https://leetcode.com/problems/maximum-binary-tree/) | Find max-value index as root; recursively build left/right |
| [662. Maximum Width](https://leetcode.com/problems/maximum-width/) | BFS with node IDs (left=2*id, right=2*id+1); width = last - first + 1 |
| [889. Construct from Preorder+Postorder](https://leetcode.com/problems/construct-from-preorderpostorder/) | Preorder start=root; find preorder[start+1] in postorder for left subtree size |
| [894. All Possible Full Binary Trees](https://leetcode.com/problems/all-possible-full-binary-trees/) | Memoized recursion; split n-1 nodes into left(i) and right(n-1-i) |
| [958. Check Completeness](https://leetcode.com/problems/check-completeness/) | BFS; once null seen, all subsequent must be null |
| [988. Smallest String from Leaf](https://leetcode.com/problems/smallest-string-from-leaf/) | DFS with string prefix; compare and keep minimum at leaves |
| [998. Maximum Binary Tree II](https://leetcode.com/problems/maximum-binary-tree-ii/) | If new val > root.val, new root with old root as right child; else recurse right |
| [1022. Sum of Root to Leaf Binary Numbers](https://leetcode.com/problems/sum-of-root-to-leaf-binary-numbers/) | DFS accumulating binary value; add at leaves |
| [1110. Delete Nodes Return Forest](https://leetcode.com/problems/delete-nodes-return-forest/) | DFS tracking hasParent; children of deleted become new roots |
| [1161. Maximum Level Sum](https://leetcode.com/problems/maximum-level-sum/) | BFS; sum each level, find maximum |
| [1302. Deepest Leaves Sum](https://leetcode.com/problems/deepest-leaves-sum/) | BFS; sum last level |
| [1457. Pseudo-Palindromic Paths](https://leetcode.com/problems/pseudo-palindromic-paths/) | DFS with count array [10]; at leaf check at most one digit odd count |
| [1609. Even Odd Tree](https://leetcode.com/problems/even-odd-tree/) | BFS; validate even/odd level constraints |
| [1644. LCA II (p/q may not exist)](https://leetcode.com/problems/lca-ii-pq-may-not-exist/) | Track whether both p and q found; return LCA only when both confirmed |
| [1650. LCA III (parent pointers)](https://leetcode.com/problems/lca-iii-parent-pointers/) | Parent pointers form linked lists; find intersection of two lists |
| [1676. LCA IV (set of targets)](https://leetcode.com/problems/lca-iv-set-of-targets/) | If node in target set, return node; merge left/right results |

---

### BST

| Problem | Key Approach |
|---------|-------------|
| [95. Unique BSTs II](https://leetcode.com/problems/unique-bsts-ii/) | Enumerate roots 1–n; combine left/right subtree lists; memoize |
| [96. Unique BSTs](https://leetcode.com/problems/unique-bsts/) | Catalan number DP: dp[n] = sum of dp[i-1] * dp[n-i] |
| [230. Kth Smallest Element](https://leetcode.com/problems/kth-smallest-element/) | Inorder traversal with global counter |
| [235. LCA of BST](https://leetcode.com/problems/lca-of-bst/) | Use BST ordering: if node is between val1 and val2, it's the LCA |
| [450. Delete Node in BST](https://leetcode.com/problems/delete-node-in-bst/) | Recurse to find node; if two children, replace with left subtree's max |
| [530. Minimum Absolute Difference](https://leetcode.com/problems/minimum-absolute-difference/) | Inorder traversal; track previous node and compute min difference |
| [538. Convert BST to Greater Tree](https://leetcode.com/problems/convert-bst-to-greater-tree/) | Reverse inorder (right→root→left); accumulate running sum |
| [700. Search in BST](https://leetcode.com/problems/search-in-bst/) | Inorder-style recursion using BST ordering |
| [701. Insert into BST](https://leetcode.com/problems/insert-into-bst/) | Recurse left or right; create node when null reached |
| [1038. BST to Greater Sum Tree](https://leetcode.com/problems/bst-to-greater-sum-tree/) | Same as #538 |

---

### Graph

| Problem | Key Approach |
|---------|-------------|
| [127. Word Ladder](https://leetcode.com/problems/word-ladder/) | BFS from beginWord; try all 1-char mutations; filter by dictionary |
| [130. Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | Connect border 'O's to dummy node; flip all 'O's not connected to dummy |
| [133. Clone Graph](https://leetcode.com/problems/clone-graph/) | BFS with old→new node map; replicate adjacency lists |
| [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | DFS flood-fill; count and flatten each island |
| [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | DFS with onPath array to detect cycles; or BFS Kahn's on in-degrees |
| [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | BFS: append in-degree-0 in order; DFS: postorder append then reverse |
| [310. Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) | Iteratively remove leaf nodes (degree 1) until ≤ 2 remain |
| [329. Longest Increasing Path in Matrix](https://leetcode.com/problems/longest-increasing-path-in-matrix/) | DFS with memoization; each cell = 1 + max of valid neighbors |
| [399. Evaluate Division](https://leetcode.com/problems/evaluate-division/) | Build weighted graph; BFS multiplying edge weights along path |
| [547. Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | Union-Find; count connected components |
| [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Union-Find; if two endpoints already connected, that edge is redundant |
| [694. Number of Distinct Islands](https://leetcode.com/problems/number-of-distinct-islands/) | DFS recording direction sequence as string; set counts distinct shapes |
| [695. Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | DFS flood-fill; track area during recursion |
| [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Dijkstra from source; return maximum shortest path |
| [785. Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) | BFS/DFS coloring; return false if adjacent nodes share same color |
| [863. All Nodes Distance K](https://leetcode.com/problems/all-nodes-distance-k/) | Build parent map via DFS; BFS from target tracking depth |
| [886. Possible Bipartition](https://leetcode.com/problems/possible-bipartition/) | Same as #785 |
| [924. Minimize Malware Spread](https://leetcode.com/problems/minimize-malware-spread/) | BFS from each initial node; candidate = largest component with no other initial node |
| [947. Most Stones Removed](https://leetcode.com/problems/most-stones-removed/) | Union stones sharing row or column; answer = stones - component count |
| [990. Satisfiability of Equality Equations](https://leetcode.com/problems/satisfiability-of-equality-equations/) | Union equal variables; check no unequal pair in same component |
| [1020. Number of Enclaves](https://leetcode.com/problems/number-of-enclaves/) | Fill border-connected land; count remaining 1s |
| [1254. Number of Closed Islands](https://leetcode.com/problems/number-of-closed-islands/) | Fill border-connected 0-islands; count remaining 0-island floods |
| [1361. Validate Binary Tree Nodes](https://leetcode.com/problems/validate-binary-tree-nodes/) | One node with in-degree 0 (root); others in-degree 1; traverse from root |
| [1514. Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/) | Dijkstra variant with max-heap; multiply probabilities |
| [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) | Kruskal's: sort all edges, union if not connected |
| [1631. Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | Dijkstra variant; edge weight = max absolute difference |
| [1905. Count Sub Islands](https://leetcode.com/problems/count-sub-islands/) | DFS: if grid2's island has cell where grid1=0, not sub-island; count |
| [2101. Detonate Maximum Bombs](https://leetcode.com/problems/detonate-maximum-bombs/) | Build directed graph by blast radius; BFS count reachable from each |

---

### BFS

| Problem | Key Approach |
|---------|-------------|
| [433. Minimum Genetic Mutation](https://leetcode.com/problems/minimum-genetic-mutation/) | BFS; each mutation one char change toward bank; return step count |
| [542. 01 Matrix](https://leetcode.com/problems/01-matrix/) | Multi-source BFS from all 0s; propagate distances outward |
| [752. Open the Lock](https://leetcode.com/problems/open-the-lock/) | BFS from "0000"; each step turns one wheel ±1; filter deadends and visited |
| [773. Sliding Puzzle](https://leetcode.com/problems/sliding-puzzle/) | BFS on state strings; generate all next states by swapping 0 with neighbors |
| [841. Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/) | BFS from room 0 collecting keys; check if all rooms visited |
| [909. Snakes and Ladders](https://leetcode.com/problems/snakes-and-ladders/) | BFS on 1D index with boustrophedon conversion; count steps |
| [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Multi-source BFS from all rotten simultaneously; check any fresh remain |
| [1091. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | BFS in 8 directions; count steps to (n-1, n-1) |
| [1306. Jump Game III](https://leetcode.com/problems/jump-game-iii/) | BFS; from index jump to `index ± arr[index]`; check target reached |
| [1926. Nearest Exit from Entrance](https://leetcode.com/problems/nearest-exit-from-entrance/) | BFS from entrance; first empty border cell (not entrance) is answer |

---

### Backtracking

| Problem | Key Approach |
|---------|-------------|
| [17. Letter Combinations of Phone Number](https://leetcode.com/problems/letter-combinations-of-phone-number/) | Backtracking; iterate all letters mapped to each digit |
| [37. Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) | 1D array (i=index/9, j=index%9); try digits, validate row/col/box, recurse |
| [39. Combination Sum](https://leetcode.com/problems/combination-sum/) | Backtracking allowing reuse (recurse with same start) |
| [40. Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | Sort + skip `nums[i] == nums[i-1]`; each element used once |
| [46. Permutations](https://leetcode.com/problems/permutations/) | Backtracking with `used` boolean array |
| [47. Permutations II](https://leetcode.com/problems/permutations-ii/) | Sort + skip `nums[i] == nums[i-1] && !used[i-1]` |
| [51. N-Queens](https://leetcode.com/problems/n-queens/) | Track column, main diagonal, anti-diagonal sets; place queen per row |
| [52. N-Queens II](https://leetcode.com/problems/n-queens-ii/) | Same as #51 but count solutions only |
| [77. Combinations](https://leetcode.com/problems/combinations/) | Backtracking with start index ensuring no repeats |
| [78. Subsets](https://leetcode.com/problems/subsets/) | Backtracking with start index; record every prefix |
| [79. Word Search](https://leetcode.com/problems/word-search/) | Backtracking on grid; track visited; check boundaries |
| [89. Gray Code](https://leetcode.com/problems/gray-code/) | Backtracking from 0; change one bit at a time; check if visited |
| [90. Subsets II](https://leetcode.com/problems/subsets-ii/) | Sort + skip duplicate elements at same recursion depth |
| [93. Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/) | Pick 1–3 chars, validate, collect exactly 4 valid segments |
| [131. Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | Try all substrings from start; add to list if palindrome |
| [216. Combination Sum III](https://leetcode.com/problems/combination-sum-iii/) | Backtracking with start; exactly k numbers summing to n |
| [301. Remove Invalid Parentheses](https://leetcode.com/problems/remove-invalid-parentheses/) | Try keeping or removing each bracket; prune when leftCount < 0 |
| [473. Matchsticks to Square](https://leetcode.com/problems/matchsticks-to-square/) | Backtracking into 4 equal-sum buckets; bitmask memoization |
| [491. Non-Decreasing Subsequences](https://leetcode.com/problems/non-decreasing-subsequences/) | Prune if value < last or already used at this depth |
| [526. Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/) | Backtracking 1–n; check `start % i == 0 \|\| i % start == 0` |
| [638. Shopping Offers](https://leetcode.com/problems/shopping-offers/) | Backtracking through special offers; compare with non-offer buying |
| [784. Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/) | Branch on uppercase and lowercase for each character |
| [967. Numbers With Same Consecutive Differences](https://leetcode.com/problems/numbers-with-same-consecutive-differences/) | Backtracking digit by digit; branch by ±k from last digit |
| [980. Unique Paths III](https://leetcode.com/problems/unique-paths-iii/) | DFS with `used` grid; count paths visiting all non-obstacle cells |
| [996. Number of Squareful Arrays](https://leetcode.com/problems/number-of-squareful-arrays/) | Sort + permutation backtracking; prune if adjacent sum not perfect square |
| [1079. Letter Tile Possibilities](https://leetcode.com/problems/letter-tile-possibilities/) | Sort tiles; backtracking with `used`; prune duplicate tiles |
| [1219. Path with Maximum Gold](https://leetcode.com/problems/path-with-maximum-gold/) | DFS with visited set; try all starting cells |
| [1593. Split String Into Max Unique Substrings](https://leetcode.com/problems/split-string-into-max-unique-substrings/) | Backtracking; skip if substring already used; maximize unique count |
| [1723. Find Minimum Time to Finish All Jobs](https://leetcode.com/problems/find-minimum-time-to-finish-all-jobs/) | Backtracking k workers; prune if exceeding best or worker load matches previous |
| [1849. Splitting Into Descending Consecutive Values](https://leetcode.com/problems/splitting-into-descending-consecutive-values/) | Backtracking; prune if not strictly decreasing by 1 |
| [2305. Fair Distribution of Cookies](https://leetcode.com/problems/fair-distribution-of-cookies/) | Distribute to k children minimizing maximum |
| [2850. Minimum Moves to Spread Stones](https://leetcode.com/problems/minimum-moves-to-spread-stones/) | Backtracking from cells with >1 stone to empty cells; track total steps |

---

### Dynamic Programming

| Problem | Key Approach |
|---------|-------------|
| [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Expand around each center (i,j); track longest |
| [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Track current and next farthest; increment steps when current reached |
| [53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | `dp[i] = max(dp[i-1] + nums[i], nums[i])`; track overall max |
| [55. Jump Game](https://leetcode.com/problems/jump-game/) | Track max reachable index; ensure i ≤ max |
| [63. Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | `dp[i][j] = dp[i-1][j] + dp[i][j-1]`; set to 0 at obstacles |
| [64. Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | `dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]` |
| [72. Edit Distance](https://leetcode.com/problems/edit-distance/) | If chars equal, inherit diagonal; else min(insert, delete, replace) + 1 |
| [97. Interleaving String](https://leetcode.com/problems/interleaving-string/) | `dp[i][j]` true if s1[0..i] and s2[0..j] interleave to form s3[0..i+j] |
| [120. Triangle](https://leetcode.com/problems/triangle/) | `dp[i][j] = min(dp[i-1][j-1], dp[i-1][j]) + triangle[i][j]` |
| [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | State machine DP with k transactions; track hold/not-hold states |
| [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Sort or hash set; if next number exists, dp + 1; else reset to 1 |
| [143. Integer Break](https://leetcode.com/problems/integer-break/) | `dp[i] = max(j * max(dp[i-j], i-j))` |
| [152. Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Track both dpMax and dpMin; new max/min = max of three candidates |
| [174. Dungeon Game](https://leetcode.com/problems/dungeon-game/) | Reverse DP from bottom-right; `dp[i][j] = max(1, min(down, right) - grid[i][j])` |
| [198. House Robber](https://leetcode.com/problems/house-robber/) | `dp[i] = max(dp[i-2] + nums[i], dp[i-1])` |
| [213. House Robber II](https://leetcode.com/problems/house-robber-ii/) | Max of rob(0..n-2) and rob(1..n-1) |
| [221. Maximal Square](https://leetcode.com/problems/maximal-square/) | `dp[i][j] = min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1` when cell is 1 |
| [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | For each i, compare all j < i where nums[j] < nums[i]; max length |
| [322. Coin Change](https://leetcode.com/problems/coin-change/) | `dp[amount] = min(dp[amount - coin] + 1)` over all coins |
| [354. Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | Sort by width desc, height asc; LIS on heights |
| [368. Largest Divisible Subset](https://leetcode.com/problems/largest-divisible-subset/) | Sort; `dp[i]` = largest subset ending at nums[i] where each element divides next |
| [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | 0/1 knapsack; target = sum/2; boolean DP array |
| [494. Target Sum](https://leetcode.com/problems/target-sum/) | Reduce to subset sum: goal = (target + sum) / 2 |
| [509. Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | Iterative DP from dp[0]=0, dp[1]=1 |
| [518. Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Unbounded knapsack; `dp[j] += dp[j - coin]` |
| [583. Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) | `len1 + len2 - 2 * LCS` |
| [712. Minimum ASCII Delete Sum](https://leetcode.com/problems/minimum-ascii-delete-sum/) | 2D DP similar to edit distance; initialize with ASCII sums |
| [718. Maximum Length of Repeated Subarray](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) | `dp[i][j] = dp[i-1][j-1] + 1` when match; track max |
| [740. Delete and Earn](https://leetcode.com/problems/delete-and-earn/) | Aggregate same-value sums; then house-robber DP |
| [918. Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) | max(Kadane result, totalSum - min subarray) |
| [931. Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/) | DP row by row; dp[i][j] = min of three above neighbors + grid |
| [983. Minimum Cost for Tickets](https://leetcode.com/problems/minimum-cost-for-tickets/) | Memoized DFS; at each travel day try 1/7/30-day passes |
| [1024. Video Stitching](https://leetcode.com/problems/video-stitching/) | Sort by start; greedily extend coverage choosing furthest end |
| [1049. Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/) | Find subset closest to sum/2 (0/1 knapsack); answer = total - 2*subset |
| [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | If chars equal add 1 from diagonal; else max of left/up |
| [1235. Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Sort by start; DP with binary search for next available job |
| [1262. Greatest Sum Divisible by Three](https://leetcode.com/problems/greatest-sum-divisible-by-three/) | Track dp0/dp1/dp2; update on each number |
| [2140. Solving Questions with Brainpower](https://leetcode.com/problems/solving-questions-with-brainpower/) | Reverse DP: `dp[i] = max(dp[i + brainpower[i] + 1] + points[i], dp[i+1])` |
| [2320. Count Ways to Place Houses](https://leetcode.com/problems/count-ways-to-place-houses/) | `dp[i] = dp[i-1] + dp[i-2]`; square the 1-side result |

---

### Greedy / Interval

| Problem | Key Approach |
|---------|-------------|
| [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Track current and next farthest; increment steps at boundary |
| [55. Jump Game](https://leetcode.com/problems/jump-game/) | Track max reachable index |
| [134. Gas Station](https://leetcode.com/problems/gas-station/) | Prefix sums; position with min prefix sum + 1 is start |
| [135. Candy](https://leetcode.com/problems/candy/) | Two-pass greedy: left-to-right then right-to-left; sum |
| [253. Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | Dual pointer on sorted starts/ends; count peak concurrent |
| [274. H-Index](https://leetcode.com/problems/h-index/) | Sort descending; h-index = largest i where citations[i] ≥ papers so far |
| [435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Sort by end; greedily keep non-overlapping; count removals |
| [452. Minimum Arrows to Burst Balloons](https://leetcode.com/problems/minimum-arrows-to-burst-balloons/) | Count non-overlapping regions; equal endpoints overlap |
| [502. IPO](https://leetcode.com/problems/ipo/) | Sort by capital; max-heap for profits; greedily pick highest-profit available |
| [57. Insert Interval](https://leetcode.com/problems/insert-interval/) | Merge overlapping with new interval; pass non-overlapping through |
| [791. Custom Sort String](https://leetcode.com/problems/custom-sort-string/) | Count chars; output in order's sequence first, then remaining |
| [2611. Mice and Cheese](https://leetcode.com/problems/mice-and-cheese/) | Sort by `reward1[i] - reward2[i]` desc; give top k to cheese1 |

---

### Heap

| Problem | Key Approach |
|---------|-------------|
| [264. Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) | Track indices for multiples of 2,3,5; pick min next ugly; increment index |
| [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Max-heap (lower half) + min-heap (upper half); balance sizes |
| [313. Super Ugly Number](https://leetcode.com/problems/super-ugly-number/) | PriorityQueue of (value, index, prime) tuples; merge and deduplicate |
| [373. Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) | PriorityQueue for K-sorted-array merging |
| [378. Kth Smallest in Sorted Matrix](https://leetcode.com/problems/kth-smallest-in-sorted-matrix/) | PriorityQueue merging sorted rows/diagonals |
| [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Sort by Euclidean distance squared; take first k |

---

### Design

| Problem | Key Approach |
|---------|-------------|
| [146. LRU Cache](https://leetcode.com/problems/lru-cache/) | HashMap + doubly-linked list; move accessed entries to head |
| [380. Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | Map (value→index) + list; on remove swap with last element |
| [919. Complete Binary Tree Inserter](https://leetcode.com/problems/complete-binary-tree-inserter/) | BFS-based insertion queue; maintain nodes with empty children |

---

### Math / String

| Problem | Key Approach |
|---------|-------------|
| [6. Zigzag Conversion](https://leetcode.com/problems/zigzag-conversion/) | Assign chars to rows with direction flag; reverse at row 0 and numRows-1 |
| [9. Palindrome Number](https://leetcode.com/problems/palindrome-number/) | Convert to string; left/right pointer check |
| [12. Integer to Roman](https://leetcode.com/problems/integer-to-roman/) | Map each thousands/hundreds/tens/ones digit to Roman |
| [13. Roman to Integer](https://leetcode.com/problems/roman-to-integer/) | Iterate right-to-left; subtract if current < previous |
| [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | Compare char by char at index i across all strings |
| [28. Find First Occurrence](https://leetcode.com/problems/find-first-occurrence/) | Slide through haystack; compare substring when first chars match |
| [50. Pow(x, n)](https://leetcode.com/problems/powx-n/) | Fast exponentiation: `pow(x, n/2)^2`; handle negative n and odd n |
| [58. Length of Last Word](https://leetcode.com/problems/length-of-last-word/) | Trim trailing spaces; count from end until space found |
| [67. Add Binary](https://leetcode.com/problems/add-binary/) | Simulate binary addition from right with carry |
| [68. Text Justification](https://leetcode.com/problems/text-justification/) | Group words; distribute spaces (last line and single-word: left-justified) |
| [149. Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) | For each point i, map slope (dx/gcd, dy/gcd) to count |
| [151. Reverse Words in String](https://leetcode.com/problems/reverse-words-in-string/) | Reverse entire string; reverse each word; trim spaces |
| [202. Happy Number](https://leetcode.com/problems/happy-number/) | Simulate digit-square sum; detect cycle with visited set |
| [204. Count Primes](https://leetcode.com/problems/count-primes/) | Sieve of Eratosthenes; mark multiples starting at i² |
| [263. Ugly Number](https://leetcode.com/problems/ugly-number/) | Divide by 2,3,5 repeatedly; ugly if result equals 1 |
| [372. Super Pow](https://leetcode.com/problems/super-pow/) | Modular exponentiation with base 1337; recursively compute |
| [383. Ransom Note](https://leetcode.com/problems/ransom-note/) | Compare character frequency arrays (size 26) |
| [877. Stone Game](https://leetcode.com/problems/stone-game/) | Always true; first player can always choose optimal parity |
| [1201. Ugly Number III](https://leetcode.com/problems/ugly-number-iii/) | Binary search on answer; count multiples with inclusion-exclusion and LCM |

---

### Bit Manipulation / Matrix / Randomized

| Problem | Key Approach |
|---------|-------------|
| [48. Rotate Image](https://leetcode.com/problems/rotate-image/) | Transpose along diagonal, then reverse each row |
| [54. Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Maintain left/right/top/bottom boundaries; shrink after each pass |
| [59. Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) | Same boundary approach as #54, filling values |
| [73. Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | Record if first row/col has zeros; use them as markers |
| [137. Single Number II](https://leetcode.com/problems/single-number-ii/) | Count array indexed by value/10000; filter entries with count 1 |
| [201. Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) | Repeatedly AND right with right-1 until right ≤ left |
| [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Left-pass prefix products × right-pass postfix products |
| [289. Game of Life](https://leetcode.com/problems/game-of-life/) | Three-row sliding window tracks neighbor counts |
| [382. Linked List Random Node](https://leetcode.com/problems/linked-list-random-node/) | Reservoir sampling: replace with probability 1/index |
| [384. Shuffle an Array](https://leetcode.com/problems/shuffle-an-array/) | Fisher-Yates: swap position i with random position ≥ i |
| [398. Random Pick Index](https://leetcode.com/problems/random-pick-index/) | Reservoir sampling over indices matching target |
| [427. Construct Quad Tree](https://leetcode.com/problems/construct-quad-tree/) | Recursively split into 4 quadrants; merge if all children same-value leaves |
| [867. Transpose Matrix](https://leetcode.com/problems/transpose-matrix/) | New m×n array swapping rows and columns |
| [1260. Shift 2D Grid](https://leetcode.com/problems/shift-2d-grid/) | Flatten to 1D, reverse, reverse sub-segments |
| [1329. Sort Matrix Diagonally](https://leetcode.com/problems/sort-matrix-diagonally/) | Use `i-j` as diagonal key; sort each diagonal and reconstruct |
| [2073. Time Needed to Buy Tickets](https://leetcode.com/problems/time-needed-to-buy-tickets/) | People before k buy up to `tickets[k]`; after buy up to `tickets[k]-1` |
