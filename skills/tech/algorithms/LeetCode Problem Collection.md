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
| 2. Add Two Numbers | Iterate both lists simultaneously carrying sum digit; handle remaining carry |
| 21. Merge Two Sorted Lists | Dummy result pointer; advance through both lists picking smaller value |
| 23. Merge k Sorted Lists | Min-heap comparing node values; repeatedly extract minimum |
| 19. Remove Nth Node From End | Dummy head; keep gap of N between fast/slow pointers to land on predecessor |
| 25. Reverse Nodes in k-Group | Recursive; grab successor head, set `head.next = successor` after reversing k nodes |
| 61. Rotate List | Reverse whole list, then reverse first-K and last-K segments separately |
| 82. Remove Duplicates II | Fast/slow with prev tracker; or split into dup/noDup lists |
| 83. Remove Duplicates | Fast/slow pointers |
| 86. Partition List | Two dummy lists (low, high); join at end, nullify tail |
| 92. Reverse Linked List II | Recursive; advance to position m, then trigger reverse-k logic |
| 138. Copy List with Random Pointer | Two-pass: create all new nodes in map; assign next and random |
| 141. Linked List Cycle | Fast/slow pointers; fast catches slow when cycle exists |
| 142. Linked List Cycle II | Fast/slow meet, reset one to head, step both by 1; second meeting = cycle entry |
| 143. Reorder List | Store list in stack; alternate original forward nodes with reversed tail nodes |
| 160. Intersection of Two Lists | Concatenate A+B and B+A; alignment makes them meet at intersection |
| 206. Reverse Linked List | Recursive: `head.next.next = head; head.next = null` |
| 234. Palindrome Linked List | Recursive traversal with global left pointer compared against right (post-order) |
| 445. Add Two Numbers II | Reverse both lists, then apply #2 approach |
| 876. Middle of Linked List | Fast/slow; slow is at middle when fast reaches end |

---

### Two Pointers

| Problem | Key Approach |
|---------|-------------|
| 1. Two Sum | Hash map storing complement indices |
| 11. Container With Most Water | Left/right pointers; move shorter side inward; track max area |
| 15. 3Sum | Sort, deduplicate, reduce to two-sum with left/right pointers |
| 26. Remove Duplicates from Sorted Array | Fast/slow; slow advances only on unique values |
| 27. Remove Element | Fast/slow; overwrite target elements in place |
| 42. Trapping Rain Water | Left/right max arrays; water = min(leftMax, rightMax) - height |
| 75. Sort Colors (Dutch National Flag) | Track p0 and p2; swap elements, handle p < p0 case |
| 80. Remove Duplicates II | Fast/slow with count variable allowing up to 2 duplicates |
| 88. Merge Sorted Array | Two pointers from the end; fill in reverse |
| 125. Valid Palindrome | Strip to alphanumeric lowercase; left/right pointer check |
| 167. Two Sum II - Sorted Array | Left and right pointers; move inward based on sum vs target |
| 228. Summary Ranges | Two pointers (start, end); extend end while consecutive; format range |
| 283. Move Zeroes | Fast/slow; compact non-zeros, fill tail with zeros |
| 344. Reverse String | Left/right pointers swapping toward center |
| 392. Is Subsequence | Two pointers on s and t; advance t for every match |
| 977. Squares of Sorted Array | Left/right; place larger square from end |
| 986. Interval List Intersections | Advance pointer whose interval ends earlier; collect overlaps |

---

### Sliding Window

| Problem | Key Approach |
|---------|-------------|
| 3. Longest Substring Without Repeating | Window map tracks char counts; move left until no count exceeds 1 |
| 30. Substring with Concatenation of All Words | Sliding window with word-count maps; multiple starting offsets (0 to word length) |
| 76. Minimum Window Substring | Shrink left when valid == need.size; track min window length and start |
| 209. Minimum Size Subarray Sum | Shrink left while sum ≥ target; track min length |
| 219. Contains Duplicate II | Use set; remove element at left when window exceeds k |
| 220. Contains Duplicate III | Use TreeSet; check ceiling/floor within value range |
| 395. Longest Substring with At Least K Repeating | Enumerate 1–26 unique char counts; find longest window for each |
| 424. Longest Repeating Character Replacement | Track max-freq char; shrink left when (window - maxFreq) > k |
| 438. Find All Anagrams | Need/window maps + valid counter; record left index when valid == need.size |
| 567. Permutation in String | Same as #438; return true when valid == need.size |
| 713. Subarray Product Less than K | Each valid window of size (right-left) contributes (right-left) subarrays |
| 1004. Max Consecutive Ones III | Move left when zero-count exceeds k; track max window |
| 1658. Minimum Operations to Reduce X to Zero | Convert to finding longest subarray with sum = total - x |

---

### Binary Search

| Problem | Key Approach |
|---------|-------------|
| 4. Median of Two Sorted Arrays | Binary search on smaller array; partition to find median |
| 34. Find First and Last Position | Two binary searches: left boundary (tighten right) and right boundary (tighten left) |
| 35. Search Insert Position | Binary search; return left when target not found |
| 69. Sqrt(x) | Binary search in [1, x/2+1]; find largest mid where mid ≤ x/mid |
| 162. Find Peak Element | Compare mid with neighbors to determine which side has a peak |
| 528. Random Pick with Weight | Prefix sum array; binary search for rightmost index ≥ random in [1, total] |
| 704. Binary Search | Standard closed-interval binary search |
| 875. Koko Eating Bananas | Binary search on eating speed; minimize hours |
| 1011. Capacity to Ship Packages | Binary search on load; minimize days function |
| 1235. Maximum Profit in Job Scheduling | Sort by start; DP with binary search for next available job |
| 1539. Kth Missing Positive | Linear scan comparing expected vs actual; adjust with remaining k |
| 410. Split Array Largest Sum | Binary search on max subarray sum; minimize splits |

---

### Prefix Sum / Difference Array

| Problem | Key Approach |
|---------|-------------|
| 303. Range Sum Query | Precompute prefix sums; query with `preSum[j+1] - preSum[i]` |
| 304. Range Sum Query 2D | 2D prefix sum; inclusion-exclusion for rectangle queries |
| 1094. Car Pooling | Difference array on stops; capacity must not be exceeded at each position |
| 1109. Corporate Flight Bookings | Difference array on flights; increment from `first` to `end-1` |

---

### Stack

| Problem | Key Approach |
|---------|-------------|
| 20. Valid Parentheses | Push matching closing brackets; pop and verify on each closing bracket |
| 71. Simplify Path | Push dir names; pop on `..`; ignore `.`; join remaining stack |
| 150. Evaluate Reverse Polish Notation | Push numbers; on operator pop two, compute, push result |
| 155. Min Stack | Dual stacks; min stack records current minimum at every push |
| 225. Implement Stack using Queues | Track top; to pop, dequeue all but last element |
| 232. Implement Queue using Stacks | Two stacks (top, bottom); pour top into bottom on pop |
| 388. Longest Absolute File Path | Use `\t` depth to manage stack; compute length on file nodes |
| 895. Maximum Frequency Stack | freq-to-stack map + val-to-freq map; pop from highest-frequency stack |
| 933. Number of Recent Calls | Queue; poll all entries older than 3000ms window |
| 1249. Minimum Remove to Make Valid Parentheses | Stack of indices for `(`; unmatched `)` to delete list; remove all marked |

---

### Monotonic Stack

| Problem | Key Approach |
|---------|-------------|
| 402. Remove K Digits | Monotonically increasing stack; remove k elements from top; handle leading zeros |
| 496. Next Greater Element I | Build next-greater map from nums2; look up nums1 values |
| 503. Next Greater Element II | Double array for circular traversal; build next-greater map |
| 581. Shortest Unsorted Continuous Subarray | Sort copy; find leftmost/rightmost where original differs from sorted |
| 739. Daily Temperatures | Monotonic stack storing indices; pop when warmer temperature found |
| 853. Car Fleet | Sort by position; compute arrival times; count increasing sequences from rear |
| 901. Online Stock Span | Stack storing (value, span); accumulate span of popped elements |
| 1019. Next Greater Node in Linked List | Convert list to array; apply monotonic stack |
| 1475. Final Prices with Special Discount | Find next smaller price; subtract |
| 1944. Number of Visible People in Queue | Count elements popped from monotonic stack |

---

### Binary Tree

| Problem | Key Approach |
|---------|-------------|
| 98. Validate Binary Search Tree | Pass min/max bounds down; return false if node violates bounds |
| 102. Level Order Traversal | Standard BFS level by level |
| 103. Zigzag Level Order | BFS; alternate addFirst/addLast based on level parity |
| 104. Maximum Depth | Depth = max(left, right) + 1 |
| 105. Construct from Preorder+Inorder | Preorder root first; find root in inorder to split left/right |
| 106. Construct from Inorder+Postorder | Postorder root last; find root in inorder to split left/right |
| 107. Level Order Traversal II | BFS with addFirst for reversed output |
| 114. Flatten to Linked List | Flatten left/right; attach left subtree tail to right; set left = null |
| 116. Populating Next Right Pointers | Traverse (node1, node2) pairs covering three sibling relationships |
| 117. Populating Next Right Pointers II | BFS with next pointer assignment |
| 129. Sum Root to Leaf Numbers | DFS with accumulated numeric value; add at leaves |
| 144. Preorder Traversal | Standard preorder |
| 199. Right Side View | BFS record last element per level; or preorder DFS going right first |
| 222. Count Complete Tree Nodes | Compare left/right depths; if equal, subtree is full (2^level - 1) |
| 226. Invert Binary Tree | Recursively swap left and right children at every node |
| 236. Lowest Common Ancestor | Return node if equals p or q; LCA where both left and right non-null |
| 257. Binary Tree Paths | DFS with path prefix; record when both children null |
| 297. Serialize and Deserialize | Preorder with null nodes; or BFS level-order |
| 331. Verify Preorder Serialization | Non-null: in -1, out +2; null: in -1; start edge=1, end at 0 |
| 337. House Robber III | Tree DP: each node returns (rob, skip); rob = val + grandchildren sums |
| 515. Find Largest Value per Row | BFS; track max per level |
| 543. Diameter | Max diameter at node = left depth + right depth; global max variable |
| 637. Average of Levels | BFS; average each level |
| 652. Find Duplicate Subtrees | Serialize each subtree (postorder); frequency map detects duplicates |
| 654. Maximum Binary Tree | Find max-value index as root; recursively build left/right |
| 662. Maximum Width | BFS with node IDs (left=2*id, right=2*id+1); width = last - first + 1 |
| 889. Construct from Preorder+Postorder | Preorder start=root; find preorder[start+1] in postorder for left subtree size |
| 894. All Possible Full Binary Trees | Memoized recursion; split n-1 nodes into left(i) and right(n-1-i) |
| 958. Check Completeness | BFS; once null seen, all subsequent must be null |
| 988. Smallest String from Leaf | DFS with string prefix; compare and keep minimum at leaves |
| 998. Maximum Binary Tree II | If new val > root.val, new root with old root as right child; else recurse right |
| 1022. Sum of Root to Leaf Binary Numbers | DFS accumulating binary value; add at leaves |
| 1110. Delete Nodes Return Forest | DFS tracking hasParent; children of deleted become new roots |
| 1161. Maximum Level Sum | BFS; sum each level, find maximum |
| 1302. Deepest Leaves Sum | BFS; sum last level |
| 1457. Pseudo-Palindromic Paths | DFS with count array [10]; at leaf check at most one digit odd count |
| 1609. Even Odd Tree | BFS; validate even/odd level constraints |
| 1644. LCA II (p/q may not exist) | Track whether both p and q found; return LCA only when both confirmed |
| 1650. LCA III (parent pointers) | Parent pointers form linked lists; find intersection of two lists |
| 1676. LCA IV (set of targets) | If node in target set, return node; merge left/right results |

---

### BST

| Problem | Key Approach |
|---------|-------------|
| 95. Unique BSTs II | Enumerate roots 1–n; combine left/right subtree lists; memoize |
| 96. Unique BSTs | Catalan number DP: dp[n] = sum of dp[i-1] * dp[n-i] |
| 230. Kth Smallest Element | Inorder traversal with global counter |
| 235. LCA of BST | Use BST ordering: if node is between val1 and val2, it's the LCA |
| 450. Delete Node in BST | Recurse to find node; if two children, replace with left subtree's max |
| 530. Minimum Absolute Difference | Inorder traversal; track previous node and compute min difference |
| 538. Convert BST to Greater Tree | Reverse inorder (right→root→left); accumulate running sum |
| 700. Search in BST | Inorder-style recursion using BST ordering |
| 701. Insert into BST | Recurse left or right; create node when null reached |
| 1038. BST to Greater Sum Tree | Same as #538 |

---

### Graph

| Problem | Key Approach |
|---------|-------------|
| 127. Word Ladder | BFS from beginWord; try all 1-char mutations; filter by dictionary |
| 130. Surrounded Regions | Connect border 'O's to dummy node; flip all 'O's not connected to dummy |
| 133. Clone Graph | BFS with old→new node map; replicate adjacency lists |
| 200. Number of Islands | DFS flood-fill; count and flatten each island |
| 207. Course Schedule | DFS with onPath array to detect cycles; or BFS Kahn's on in-degrees |
| 210. Course Schedule II | BFS: append in-degree-0 in order; DFS: postorder append then reverse |
| 310. Minimum Height Trees | Iteratively remove leaf nodes (degree 1) until ≤ 2 remain |
| 329. Longest Increasing Path in Matrix | DFS with memoization; each cell = 1 + max of valid neighbors |
| 399. Evaluate Division | Build weighted graph; BFS multiplying edge weights along path |
| 547. Number of Provinces | Union-Find; count connected components |
| 684. Redundant Connection | Union-Find; if two endpoints already connected, that edge is redundant |
| 694. Number of Distinct Islands | DFS recording direction sequence as string; set counts distinct shapes |
| 695. Max Area of Island | DFS flood-fill; track area during recursion |
| 743. Network Delay Time | Dijkstra from source; return maximum shortest path |
| 785. Is Graph Bipartite? | BFS/DFS coloring; return false if adjacent nodes share same color |
| 863. All Nodes Distance K | Build parent map via DFS; BFS from target tracking depth |
| 886. Possible Bipartition | Same as #785 |
| 924. Minimize Malware Spread | BFS from each initial node; candidate = largest component with no other initial node |
| 947. Most Stones Removed | Union stones sharing row or column; answer = stones - component count |
| 990. Satisfiability of Equality Equations | Union equal variables; check no unequal pair in same component |
| 1020. Number of Enclaves | Fill border-connected land; count remaining 1s |
| 1254. Number of Closed Islands | Fill border-connected 0-islands; count remaining 0-island floods |
| 1361. Validate Binary Tree Nodes | One node with in-degree 0 (root); others in-degree 1; traverse from root |
| 1514. Path with Maximum Probability | Dijkstra variant with max-heap; multiply probabilities |
| 1584. Min Cost to Connect All Points | Kruskal's: sort all edges, union if not connected |
| 1631. Path With Minimum Effort | Dijkstra variant; edge weight = max absolute difference |
| 1905. Count Sub Islands | DFS: if grid2's island has cell where grid1=0, not sub-island; count |
| 2101. Detonate Maximum Bombs | Build directed graph by blast radius; BFS count reachable from each |

---

### BFS

| Problem | Key Approach |
|---------|-------------|
| 433. Minimum Genetic Mutation | BFS; each mutation one char change toward bank; return step count |
| 542. 01 Matrix | Multi-source BFS from all 0s; propagate distances outward |
| 752. Open the Lock | BFS from "0000"; each step turns one wheel ±1; filter deadends and visited |
| 773. Sliding Puzzle | BFS on state strings; generate all next states by swapping 0 with neighbors |
| 841. Keys and Rooms | BFS from room 0 collecting keys; check if all rooms visited |
| 909. Snakes and Ladders | BFS on 1D index with boustrophedon conversion; count steps |
| 994. Rotting Oranges | Multi-source BFS from all rotten simultaneously; check any fresh remain |
| 1091. Shortest Path in Binary Matrix | BFS in 8 directions; count steps to (n-1, n-1) |
| 1306. Jump Game III | BFS; from index jump to `index ± arr[index]`; check target reached |
| 1926. Nearest Exit from Entrance | BFS from entrance; first empty border cell (not entrance) is answer |

---

### Backtracking

| Problem | Key Approach |
|---------|-------------|
| 17. Letter Combinations of Phone Number | Backtracking; iterate all letters mapped to each digit |
| 37. Sudoku Solver | 1D array (i=index/9, j=index%9); try digits, validate row/col/box, recurse |
| 39. Combination Sum | Backtracking allowing reuse (recurse with same start) |
| 40. Combination Sum II | Sort + skip `nums[i] == nums[i-1]`; each element used once |
| 46. Permutations | Backtracking with `used` boolean array |
| 47. Permutations II | Sort + skip `nums[i] == nums[i-1] && !used[i-1]` |
| 51. N-Queens | Track column, main diagonal, anti-diagonal sets; place queen per row |
| 52. N-Queens II | Same as #51 but count solutions only |
| 77. Combinations | Backtracking with start index ensuring no repeats |
| 78. Subsets | Backtracking with start index; record every prefix |
| 79. Word Search | Backtracking on grid; track visited; check boundaries |
| 89. Gray Code | Backtracking from 0; change one bit at a time; check if visited |
| 90. Subsets II | Sort + skip duplicate elements at same recursion depth |
| 93. Restore IP Addresses | Pick 1–3 chars, validate, collect exactly 4 valid segments |
| 131. Palindrome Partitioning | Try all substrings from start; add to list if palindrome |
| 216. Combination Sum III | Backtracking with start; exactly k numbers summing to n |
| 301. Remove Invalid Parentheses | Try keeping or removing each bracket; prune when leftCount < 0 |
| 473. Matchsticks to Square | Backtracking into 4 equal-sum buckets; bitmask memoization |
| 491. Non-Decreasing Subsequences | Prune if value < last or already used at this depth |
| 526. Beautiful Arrangement | Backtracking 1–n; check `start % i == 0 \|\| i % start == 0` |
| 638. Shopping Offers | Backtracking through special offers; compare with non-offer buying |
| 784. Letter Case Permutation | Branch on uppercase and lowercase for each character |
| 967. Numbers With Same Consecutive Differences | Backtracking digit by digit; branch by ±k from last digit |
| 980. Unique Paths III | DFS with `used` grid; count paths visiting all non-obstacle cells |
| 996. Number of Squareful Arrays | Sort + permutation backtracking; prune if adjacent sum not perfect square |
| 1079. Letter Tile Possibilities | Sort tiles; backtracking with `used`; prune duplicate tiles |
| 1219. Path with Maximum Gold | DFS with visited set; try all starting cells |
| 1593. Split String Into Max Unique Substrings | Backtracking; skip if substring already used; maximize unique count |
| 1723. Find Minimum Time to Finish All Jobs | Backtracking k workers; prune if exceeding best or worker load matches previous |
| 1849. Splitting Into Descending Consecutive Values | Backtracking; prune if not strictly decreasing by 1 |
| 2305. Fair Distribution of Cookies | Distribute to k children minimizing maximum |
| 2850. Minimum Moves to Spread Stones | Backtracking from cells with >1 stone to empty cells; track total steps |

---

### Dynamic Programming

| Problem | Key Approach |
|---------|-------------|
| 5. Longest Palindromic Substring | Expand around each center (i,j); track longest |
| 45. Jump Game II | Track current and next farthest; increment steps when current reached |
| 53. Maximum Subarray | `dp[i] = max(dp[i-1] + nums[i], nums[i])`; track overall max |
| 55. Jump Game | Track max reachable index; ensure i ≤ max |
| 63. Unique Paths II | `dp[i][j] = dp[i-1][j] + dp[i][j-1]`; set to 0 at obstacles |
| 64. Minimum Path Sum | `dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]` |
| 72. Edit Distance | If chars equal, inherit diagonal; else min(insert, delete, replace) + 1 |
| 97. Interleaving String | `dp[i][j]` true if s1[0..i] and s2[0..j] interleave to form s3[0..i+j] |
| 120. Triangle | `dp[i][j] = min(dp[i-1][j-1], dp[i-1][j]) + triangle[i][j]` |
| 121. Best Time to Buy and Sell Stock | State machine DP with k transactions; track hold/not-hold states |
| 128. Longest Consecutive Sequence | Sort or hash set; if next number exists, dp + 1; else reset to 1 |
| 143. Integer Break | `dp[i] = max(j * max(dp[i-j], i-j))` |
| 152. Maximum Product Subarray | Track both dpMax and dpMin; new max/min = max of three candidates |
| 174. Dungeon Game | Reverse DP from bottom-right; `dp[i][j] = max(1, min(down, right) - grid[i][j])` |
| 198. House Robber | `dp[i] = max(dp[i-2] + nums[i], dp[i-1])` |
| 213. House Robber II | Max of rob(0..n-2) and rob(1..n-1) |
| 221. Maximal Square | `dp[i][j] = min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1` when cell is 1 |
| 300. Longest Increasing Subsequence | For each i, compare all j < i where nums[j] < nums[i]; max length |
| 322. Coin Change | `dp[amount] = min(dp[amount - coin] + 1)` over all coins |
| 354. Russian Doll Envelopes | Sort by width desc, height asc; LIS on heights |
| 368. Largest Divisible Subset | Sort; `dp[i]` = largest subset ending at nums[i] where each element divides next |
| 416. Partition Equal Subset Sum | 0/1 knapsack; target = sum/2; boolean DP array |
| 494. Target Sum | Reduce to subset sum: goal = (target + sum) / 2 |
| 509. Fibonacci Number | Iterative DP from dp[0]=0, dp[1]=1 |
| 518. Coin Change II | Unbounded knapsack; `dp[j] += dp[j - coin]` |
| 583. Delete Operation for Two Strings | `len1 + len2 - 2 * LCS` |
| 712. Minimum ASCII Delete Sum | 2D DP similar to edit distance; initialize with ASCII sums |
| 718. Maximum Length of Repeated Subarray | `dp[i][j] = dp[i-1][j-1] + 1` when match; track max |
| 740. Delete and Earn | Aggregate same-value sums; then house-robber DP |
| 918. Maximum Sum Circular Subarray | max(Kadane result, totalSum - min subarray) |
| 931. Minimum Falling Path Sum | DP row by row; dp[i][j] = min of three above neighbors + grid |
| 983. Minimum Cost for Tickets | Memoized DFS; at each travel day try 1/7/30-day passes |
| 1024. Video Stitching | Sort by start; greedily extend coverage choosing furthest end |
| 1049. Last Stone Weight II | Find subset closest to sum/2 (0/1 knapsack); answer = total - 2*subset |
| 1143. Longest Common Subsequence | If chars equal add 1 from diagonal; else max of left/up |
| 1235. Maximum Profit in Job Scheduling | Sort by start; DP with binary search for next available job |
| 1262. Greatest Sum Divisible by Three | Track dp0/dp1/dp2; update on each number |
| 2140. Solving Questions with Brainpower | Reverse DP: `dp[i] = max(dp[i + brainpower[i] + 1] + points[i], dp[i+1])` |
| 2320. Count Ways to Place Houses | `dp[i] = dp[i-1] + dp[i-2]`; square the 1-side result |

---

### Greedy / Interval

| Problem | Key Approach |
|---------|-------------|
| 45. Jump Game II | Track current and next farthest; increment steps at boundary |
| 55. Jump Game | Track max reachable index |
| 134. Gas Station | Prefix sums; position with min prefix sum + 1 is start |
| 135. Candy | Two-pass greedy: left-to-right then right-to-left; sum |
| 253. Meeting Rooms II | Dual pointer on sorted starts/ends; count peak concurrent |
| 274. H-Index | Sort descending; h-index = largest i where citations[i] ≥ papers so far |
| 435. Non-overlapping Intervals | Sort by end; greedily keep non-overlapping; count removals |
| 452. Minimum Arrows to Burst Balloons | Count non-overlapping regions; equal endpoints overlap |
| 502. IPO | Sort by capital; max-heap for profits; greedily pick highest-profit available |
| 57. Insert Interval | Merge overlapping with new interval; pass non-overlapping through |
| 791. Custom Sort String | Count chars; output in order's sequence first, then remaining |
| 2611. Mice and Cheese | Sort by `reward1[i] - reward2[i]` desc; give top k to cheese1 |

---

### Heap

| Problem | Key Approach |
|---------|-------------|
| 264. Ugly Number II | Track indices for multiples of 2,3,5; pick min next ugly; increment index |
| 295. Find Median from Data Stream | Max-heap (lower half) + min-heap (upper half); balance sizes |
| 313. Super Ugly Number | PriorityQueue of (value, index, prime) tuples; merge and deduplicate |
| 373. Find K Pairs with Smallest Sums | PriorityQueue for K-sorted-array merging |
| 378. Kth Smallest in Sorted Matrix | PriorityQueue merging sorted rows/diagonals |
| 973. K Closest Points to Origin | Sort by Euclidean distance squared; take first k |

---

### Design

| Problem | Key Approach |
|---------|-------------|
| 146. LRU Cache | HashMap + doubly-linked list; move accessed entries to head |
| 380. Insert Delete GetRandom O(1) | Map (value→index) + list; on remove swap with last element |
| 919. Complete Binary Tree Inserter | BFS-based insertion queue; maintain nodes with empty children |

---

### Math / String

| Problem | Key Approach |
|---------|-------------|
| 6. Zigzag Conversion | Assign chars to rows with direction flag; reverse at row 0 and numRows-1 |
| 9. Palindrome Number | Convert to string; left/right pointer check |
| 12. Integer to Roman | Map each thousands/hundreds/tens/ones digit to Roman |
| 13. Roman to Integer | Iterate right-to-left; subtract if current < previous |
| 14. Longest Common Prefix | Compare char by char at index i across all strings |
| 28. Find First Occurrence | Slide through haystack; compare substring when first chars match |
| 50. Pow(x, n) | Fast exponentiation: `pow(x, n/2)^2`; handle negative n and odd n |
| 58. Length of Last Word | Trim trailing spaces; count from end until space found |
| 67. Add Binary | Simulate binary addition from right with carry |
| 68. Text Justification | Group words; distribute spaces (last line and single-word: left-justified) |
| 149. Max Points on a Line | For each point i, map slope (dx/gcd, dy/gcd) to count |
| 151. Reverse Words in String | Reverse entire string; reverse each word; trim spaces |
| 202. Happy Number | Simulate digit-square sum; detect cycle with visited set |
| 204. Count Primes | Sieve of Eratosthenes; mark multiples starting at i² |
| 263. Ugly Number | Divide by 2,3,5 repeatedly; ugly if result equals 1 |
| 372. Super Pow | Modular exponentiation with base 1337; recursively compute |
| 383. Ransom Note | Compare character frequency arrays (size 26) |
| 877. Stone Game | Always true; first player can always choose optimal parity |
| 1201. Ugly Number III | Binary search on answer; count multiples with inclusion-exclusion and LCM |

---

### Bit Manipulation / Matrix / Randomized

| Problem | Key Approach |
|---------|-------------|
| 48. Rotate Image | Transpose along diagonal, then reverse each row |
| 54. Spiral Matrix | Maintain left/right/top/bottom boundaries; shrink after each pass |
| 59. Spiral Matrix II | Same boundary approach as #54, filling values |
| 73. Set Matrix Zeroes | Record if first row/col has zeros; use them as markers |
| 137. Single Number II | Count array indexed by value/10000; filter entries with count 1 |
| 201. Bitwise AND of Numbers Range | Repeatedly AND right with right-1 until right ≤ left |
| 238. Product of Array Except Self | Left-pass prefix products × right-pass postfix products |
| 289. Game of Life | Three-row sliding window tracks neighbor counts |
| 382. Linked List Random Node | Reservoir sampling: replace with probability 1/index |
| 384. Shuffle an Array | Fisher-Yates: swap position i with random position ≥ i |
| 398. Random Pick Index | Reservoir sampling over indices matching target |
| 427. Construct Quad Tree | Recursively split into 4 quadrants; merge if all children same-value leaves |
| 867. Transpose Matrix | New m×n array swapping rows and columns |
| 1260. Shift 2D Grid | Flatten to 1D, reverse, reverse sub-segments |
| 1329. Sort Matrix Diagonally | Use `i-j` as diagonal key; sort each diagonal and reconstruct |
| 2073. Time Needed to Buy Tickets | People before k buy up to `tickets[k]`; after buy up to `tickets[k]-1` |
