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
| [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Iterate both lists simultaneously carrying sum digit; handle remaining carry （两链表同步迭代进位求和） |
| [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Dummy result pointer; advance through both lists picking smaller value （哑节点+双指针合并有序链表） |
| [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Min-heap comparing node values; repeatedly extract minimum （最小堆比较节点值，反复提取最小） |
| [19. Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end/) | Dummy head; keep gap of N between fast/slow pointers to land on predecessor （哑头节点，快慢指针间距N，落点为待删前驱） |
| [25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Recursive; grab successor head, set `head.next = successor` after reversing k nodes （递归取后继头节点，逆转k节后接后继） |
| [61. Rotate List](https://leetcode.com/problems/rotate-list/) | Reverse whole list, then reverse first-K and last-K segments separately （三次反转法：整体→前K→后K） |
| [82. Remove Duplicates II](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/) | Fast/slow with prev tracker; or split into dup/noDup lists （带prev的快慢指针跳过重复段，或分成dup/noDup两链） |
| [83. Remove Duplicates](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) | Fast/slow pointers （快慢指针去重） |
| [86. Partition List](https://leetcode.com/problems/partition-list/) | Two dummy lists (low, high); join at end, nullify tail （两哑节点分低高两链，尾部相接） |
| [92. Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/) | Recursive; advance to position m, then trigger reverse-k logic （递归推进到m位，触发k节逆转逻辑） |
| [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Two-pass: create all new nodes in map; assign next and random （两遍：建旧→新映射后赋next和random） |
| [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Fast/slow pointers; fast catches slow when cycle exists （快慢指针，相遇则有环） |
| [142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | Fast/slow meet, reset one to head, step both by 1; second meeting = cycle entry （快慢相遇后，一指针回头，再次相遇为环入口） |
| [143. Reorder List](https://leetcode.com/problems/reorder-list/) | Store list in stack; alternate original forward nodes with reversed tail nodes （栈存后半，交替拼接原链表与倒序尾节点） |
| [160. Intersection of Two Lists](https://leetcode.com/problems/intersection-of-two-lists/) | Concatenate A+B and B+A; alignment makes them meet at intersection （A+B与B+A等长对齐，相遇为交点） |
| [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Recursive: `head.next.next = head; head.next = null` （递归：head.next.next=head; head.next=null） |
| [234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | Recursive traversal with global left pointer compared against right (post-order) （递归后序+全局左指针，与右指针比较） |
| [445. Add Two Numbers II](https://leetcode.com/problems/add-two-numbers-ii/) | Reverse both lists, then apply #2 approach （反转两链表后套用第2题做法） |
| [876. Middle of Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | Fast/slow; slow is at middle when fast reaches end （快指针到尾时，慢指针在中点） |

---

### Two Pointers

| Problem | Key Approach |
|---------|-------------|
| [1. Two Sum](https://leetcode.com/problems/two-sum/) | Hash map storing complement indices （哈希表存补数下标） |
| [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Left/right pointers; move shorter side inward; track max area （左右指针向中收缩，移动较短边） |
| [15. 3Sum](https://leetcode.com/problems/3sum/) | Sort, deduplicate, reduce to two-sum with left/right pointers （排序+去重，转化为双指针两数之和） |
| [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Fast/slow; slow advances only on unique values （快慢指针，慢指针仅在不重复时前进） |
| [27. Remove Element](https://leetcode.com/problems/remove-element/) | Fast/slow; overwrite target elements in place （快慢指针原地覆盖目标值） |
| [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Left/right max arrays; water = min(leftMax, rightMax) - height （左右最大高度数组，水量=min(左最大,右最大)-高度） |
| [75. Sort Colors (Dutch National Flag)](https://leetcode.com/problems/sort-colors/) | Track p0 and p2; swap elements, handle p < p0 case （三路划分，追踪p0和p2指针） |
| [80. Remove Duplicates II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/) | Fast/slow with count variable allowing up to 2 duplicates （带prev的快慢指针跳过重复段，或分成dup/noDup两链） |
| [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | Two pointers from the end; fill in reverse （从末尾双指针逆向填充） |
| [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Strip to alphanumeric lowercase; left/right pointer check （去非字母数字字符，左右指针检验） |
| [167. Two Sum II - Sorted Array](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Left and right pointers; move inward based on sum vs target （左右指针，根据和与目标大小内移） |
| [228. Summary Ranges](https://leetcode.com/problems/summary-ranges/) | Two pointers (start, end); extend end while consecutive; format range （双指针(start,end)，连续则延伸，否则格式化区间） |
| [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Fast/slow; compact non-zeros, fill tail with zeros （快慢指针压缩非零元素，末尾补零） |
| [344. Reverse String](https://leetcode.com/problems/reverse-string/) | Left/right pointers swapping toward center （左右指针向中交换） |
| [392. Is Subsequence](https://leetcode.com/problems/is-subsequence/) | Two pointers on s and t; advance t for every match （双指针遍历s和t，每次匹配推进t） |
| [977. Squares of Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/) | Left/right; place larger square from end （左右指针，较大的平方从末尾填入） |
| [986. Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | Advance pointer whose interval ends earlier; collect overlaps （推进结束较早的区间指针，收集重叠） |

---

### Sliding Window

| Problem | Key Approach |
|---------|-------------|
| [3. Longest Substring Without Repeating](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Window map tracks char counts; move left until no count exceeds 1 （窗口字符计数，重复时左移） |
| [30. Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) | Sliding window with word-count maps; multiple starting offsets (0 to word length) （滑动窗口+词频Map，多起点偏移（0到词长）） |
| [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Shrink left when valid == need.size; track min window length and start （满足时收缩左边，记录最小窗口） |
| [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Shrink left while sum ≥ target; track min length （累积和>=目标时收缩左边，记最小长度） |
| [219. Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | Use set; remove element at left when window exceeds k （集合维护窗口，超过k时移除左端） |
| [220. Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/) | Use TreeSet; check ceiling/floor within value range （TreeSet维护窗口，检查上下界是否在值域内） |
| [395. Longest Substring with At Least K Repeating](https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/) | Enumerate 1–26 unique char counts; find longest window for each （枚举1-26种不同字符数，对每种找最长合法窗口） |
| [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Track max-freq char; shrink left when (window - maxFreq) > k （记最高频字符，(窗口-最高频)>k时左移） |
| [438. Find All Anagrams](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | Need/window maps + valid counter; record left index when valid == need.size （need/window双Map+valid计数，valid==need.size时记下标） |
| [567. Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Same as #438; return true when valid == need.size （同438，valid==need.size时返回true） |
| [713. Subarray Product Less than K](https://leetcode.com/problems/subarray-product-less-than-k/) | Each valid window of size (right-left) contributes (right-left) subarrays （合法窗口大小(right-left)即贡献的子数组数） |
| [1004. Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | Move left when zero-count exceeds k; track max window （零的个数超k时左移，记最大窗口） |
| [1658. Minimum Operations to Reduce X to Zero](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/) | Convert to finding longest subarray with sum = total - x （转化为找最长子数组使其和=总和-x） |

---

### Binary Search

| Problem | Key Approach |
|---------|-------------|
| [4. Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Binary search on smaller array; partition to find median （二分较短数组，划分以找中位数） |
| [34. Find First and Last Position](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Two binary searches: left boundary (tighten right) and right boundary (tighten left) （两次二分：左边界（收右）和右边界（收左）） |
| [35. Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Binary search; return left when target not found （二分查找，未找到时返回left） |
| [69. Sqrt(x)](https://leetcode.com/problems/sqrtx/) | Binary search in [1, x/2+1]; find largest mid where mid ≤ x/mid （在[1,x/2+1]二分，找最大mid使mid*mid<=x） |
| [162. Find Peak Element](https://leetcode.com/problems/find-peak-element/) | Compare mid with neighbors to determine which side has a peak （比较mid与邻居，确定有峰值的方向） |
| [528. Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) | Prefix sum array; binary search for rightmost index ≥ random in [1, total] （前缀和数组，二分查找最右>=随机数[1,total]的下标） |
| [704. Binary Search](https://leetcode.com/problems/binary-search/) | Standard closed-interval binary search （标准闭区间二分） |
| [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Binary search on eating speed; minimize hours （对吃香蕉速度二分，最小化耗时） |
| [1011. Capacity to Ship Packages](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Binary search on load; minimize days function （对载重量二分，最小化天数函数） |
| [1235. Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Sort by start; DP with binary search for next available job （按开始时间排序，DP+二分找下一个可用任务） |
| [1539. Kth Missing Positive](https://leetcode.com/problems/kth-missing-positive-number/) | Linear scan comparing expected vs actual; adjust with remaining k （线性扫描比较期望值与实际值，调整剩余k） |
| [410. Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Binary search on max subarray sum; minimize splits （对子数组最大和二分，最小化分割数） |

---

### Prefix Sum / Difference Array

| Problem | Key Approach |
|---------|-------------|
| [303. Range Sum Query](https://leetcode.com/problems/range-sum-query-immutable/) | Precompute prefix sums; query with `preSum[j+1] - preSum[i]` （预计算前缀和，查询用preSum[j+1]-preSum[i]） |
| [304. Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d-immutable/) | 2D prefix sum; inclusion-exclusion for rectangle queries （二维前缀和，容斥原理处理矩形查询） |
| [1094. Car Pooling](https://leetcode.com/problems/car-pooling/) | Difference array on stops; capacity must not be exceeded at each position （差分数组作用于站点，每处容量不超上限） |
| [1109. Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/) | Difference array on flights; increment from `first` to `end-1` （差分数组作用于航班，first到end-1区间加值） |

---

### Stack

| Problem | Key Approach |
|---------|-------------|
| [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Push matching closing brackets; pop and verify on each closing bracket （压入匹配的右括号，遇右括号弹出并验证） |
| [71. Simplify Path](https://leetcode.com/problems/simplify-path/) | Push dir names; pop on `..`; ignore `.`; join remaining stack （压入目录名，遇..弹出，忽略.，最后连接栈内容） |
| [150. Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Push numbers; on operator pop two, compute, push result （压数字，遇运算符弹两个计算后压回） |
| [155. Min Stack](https://leetcode.com/problems/min-stack/) | Dual stacks; min stack records current minimum at every push （双栈，辅助栈记录每次push时的当前最小值） |
| [225. Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/) | Track top; to pop, dequeue all but last element （记录栈顶，pop时将其余元素依次出队再入队） |
| [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | Two stacks (top, bottom); pour top into bottom on pop （两个栈(top/bottom)，pop时将top倒入bottom） |
| [388. Longest Absolute File Path](https://leetcode.com/problems/longest-absolute-file-path/) | Use `\t` depth to manage stack; compute length on file nodes （用换行缩进深度管理栈，文件节点时计算完整路径长度） |
| [895. Maximum Frequency Stack](https://leetcode.com/problems/maximum-frequency-stack/) | freq-to-stack map + val-to-freq map; pop from highest-frequency stack （freq到栈的映射+值到freq的映射，从最高频栈弹出） |
| [933. Number of Recent Calls](https://leetcode.com/problems/number-of-recent-calls/) | Queue; poll all entries older than 3000ms window （队列，移除3000ms窗口外的旧请求） |
| [1249. Minimum Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/) | Stack of indices for `(`; unmatched `)` to delete list; remove all marked （栈记录(的下标，不匹配的)加入删除列表，移除所有标记位置） |

---

### Monotonic Stack

| Problem | Key Approach |
|---------|-------------|
| [402. Remove K Digits](https://leetcode.com/problems/remove-k-digits/) | Monotonically increasing stack; remove k elements from top; handle leading zeros （单调递增栈，从栈顶移除k个元素，处理前导零） |
| [496. Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | Build next-greater map from nums2; look up nums1 values （从nums2构建下一个更大元素Map，再查nums1） |
| [503. Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | Double array for circular traversal; build next-greater map （数组加倍模拟循环，构建下一个更大元素Map） |
| [581. Shortest Unsorted Continuous Subarray](https://leetcode.com/problems/shortest-unsorted-continuous-subarray/) | Sort copy; find leftmost/rightmost where original differs from sorted （排序后找最左/最右位置原数组与排序数组不同处） |
| [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Monotonic stack storing indices; pop when warmer temperature found （单调栈存下标，遇到更高温度时弹出） |
| [853. Car Fleet](https://leetcode.com/problems/car-fleet/) | Sort by position; compute arrival times; count increasing sequences from rear （按位置排序，计算到达时间，从后向前数递增序列） |
| [901. Online Stock Span](https://leetcode.com/problems/online-stock-span/) | Stack storing (value, span); accumulate span of popped elements （栈存(值,跨度)，累计弹出元素的跨度） |
| [1019. Next Greater Node in Linked List](https://leetcode.com/problems/next-greater-node-in-linked-list/) | Convert list to array; apply monotonic stack （链表转数组，应用单调栈） |
| [1475. Final Prices with Special Discount](https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/) | Find next smaller price; subtract （找下一个更小价格做差即折后价） |
| [1944. Number of Visible People in Queue](https://leetcode.com/problems/number-of-visible-people-in-a-queue/) | Count elements popped from monotonic stack （统计从单调栈中弹出的元素数） |

---

### Binary Tree

| Problem | Key Approach |
|---------|-------------|
| [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Pass min/max bounds down; return false if node violates bounds （向下传递min/max边界，节点违反则返回false） |
| [102. Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Standard BFS level by level （标准BFS逐层遍历） |
| [103. Zigzag Level Order](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | BFS; alternate addFirst/addLast based on level parity （BFS，按层奇偶交替addFirst/addLast） |
| [104. Maximum Depth](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Depth = max(left, right) + 1 （深度=max(左,右)+1） |
| [105. Construct from Preorder+Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Preorder root first; find root in inorder to split left/right （前序首元素为根，在中序中找根拆分左右） |
| [106. Construct from Inorder+Postorder](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) | Postorder root last; find root in inorder to split left/right （后序末元素为根，在中序中找根拆分左右） |
| [107. Level Order Traversal II](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/) | BFS with addFirst for reversed output （BFS用addFirst实现逆序输出） |
| [114. Flatten to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) | Flatten left/right; attach left subtree tail to right; set left = null （展开左右子树，左子树尾接右子树，左置null） |
| [116. Populating Next Right Pointers](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/) | Traverse (node1, node2) pairs covering three sibling relationships （遍历(node1,node2)对，覆盖三种兄弟关系） |
| [117. Populating Next Right Pointers II](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/) | BFS with next pointer assignment （BFS逐层赋next指针） |
| [129. Sum Root to Leaf Numbers](https://leetcode.com/problems/sum-root-to-leaf-numbers/) | DFS with accumulated numeric value; add at leaves （DFS累积数值，叶子时累加） |
| [144. Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/) | Standard preorder （标准前序遍历） |
| [199. Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | BFS record last element per level; or preorder DFS going right first （BFS记录每层最后元素；或前序DFS先走右子树） |
| [222. Count Complete Tree Nodes](https://leetcode.com/problems/count-complete-tree-nodes/) | Compare left/right depths; if equal, subtree is full (2^level - 1) （比较左右深度，相等时子树为满树(2^层-1)） |
| [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Recursively swap left and right children at every node （递归交换每个节点的左右子树） |
| [236. Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Return node if equals p or q; LCA where both left and right non-null （节点等于p或q则返回，左右均非空则为LCA） |
| [257. Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths/) | DFS with path prefix; record when both children null （DFS带路径前缀，两子树均为null时记录） |
| [297. Serialize and Deserialize](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Preorder with null nodes; or BFS level-order （前序加null节点序列化；或BFS层序） |
| [331. Verify Preorder Serialization](https://leetcode.com/problems/verify-preorder-serialization-of-a-binary-tree/) | Non-null: in -1, out +2; null: in -1; start edge=1, end at 0 （非空节点入-1出+2，空节点入-1，初始边=1，为0时合法） |
| [337. House Robber III](https://leetcode.com/problems/house-robber-iii/) | Tree DP: each node returns (rob, skip); rob = val + grandchildren sums （树形DP，每节点返回(抢,跳)，抢=值+孙子之和） |
| [515. Find Largest Value per Row](https://leetcode.com/problems/find-largest-value-in-each-tree-row/) | BFS; track max per level （BFS记录每层最大值） |
| [543. Diameter](https://leetcode.com/problems/diameter-of-binary-tree/) | Max diameter at node = left depth + right depth; global max variable （当前节点直径=左深+右深，维护全局最大） |
| [637. Average of Levels](https://leetcode.com/problems/average-of-levels-in-binary-tree/) | BFS; average each level （BFS对每层求平均） |
| [652. Find Duplicate Subtrees](https://leetcode.com/problems/find-duplicate-subtrees/) | Serialize each subtree (postorder); frequency map detects duplicates （后序序列化每棵子树，频率Map检测重复） |
| [654. Maximum Binary Tree](https://leetcode.com/problems/maximum-binary-tree/) | Find max-value index as root; recursively build left/right （找最大值下标为根，递归构建左右子树） |
| [662. Maximum Width](https://leetcode.com/problems/maximum-width-of-binary-tree/) | BFS with node IDs (left=2*id, right=2*id+1); width = last - first + 1 （BFS带节点ID(左=2*id,右=2*id+1)，宽度=最后-最前+1） |
| [889. Construct from Preorder+Postorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-postorder-traversal/) | Preorder start=root; find preorder[start+1] in postorder for left subtree size （前序首为根，在后序中找前序[start+1]确定左子树大小） |
| [894. All Possible Full Binary Trees](https://leetcode.com/problems/all-possible-full-binary-trees/) | Memoized recursion; split n-1 nodes into left(i) and right(n-1-i) （记忆化递归，n-1节点分为左(i)和右(n-1-i)） |
| [958. Check Completeness](https://leetcode.com/problems/check-completeness-of-a-binary-tree/) | BFS; once null seen, all subsequent must be null （BFS，出现null后后续必须全为null） |
| [988. Smallest String from Leaf](https://leetcode.com/problems/smallest-string-starting-from-leaf/) | DFS with string prefix; compare and keep minimum at leaves （DFS带字符串前缀，叶子处比较保留最小） |
| [998. Maximum Binary Tree II](https://leetcode.com/problems/maximum-binary-tree-ii/) | If new val > root.val, new root with old root as right child; else recurse right （新值>根值时，新节点为根，旧根为其右子树；否则递归右边） |
| [1022. Sum of Root to Leaf Binary Numbers](https://leetcode.com/problems/sum-of-root-to-leaf-binary-numbers/) | DFS accumulating binary value; add at leaves （DFS累积二进制值，叶子处累加） |
| [1110. Delete Nodes Return Forest](https://leetcode.com/problems/delete-nodes-and-return-forest/) | DFS tracking hasParent; children of deleted become new roots （DFS追踪hasParent，被删节点的子节点成为新根） |
| [1161. Maximum Level Sum](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/) | BFS; sum each level, find maximum （BFS对每层求和，找最大） |
| [1302. Deepest Leaves Sum](https://leetcode.com/problems/deepest-leaves-sum/) | BFS; sum last level （BFS对最后一层求和） |
| [1457. Pseudo-Palindromic Paths](https://leetcode.com/problems/pseudo-palindromic-paths-in-a-binary-tree/) | DFS with count array [10]; at leaf check at most one digit odd count （DFS+大小10的计数数组，叶子处至多一个数字奇数次） |
| [1609. Even Odd Tree](https://leetcode.com/problems/even-odd-tree/) | BFS; validate even/odd level constraints （BFS验证奇偶层约束） |
| [1644. LCA II (p/q may not exist)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-ii/) | Track whether both p and q found; return LCA only when both confirmed （追踪p和q是否均找到，仅两者均确认时返回LCA） |
| [1650. LCA III (parent pointers)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/) | Parent pointers form linked lists; find intersection of two lists （父指针构成链表，找两链表的交叉点） |
| [1676. LCA IV (set of targets)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iv/) | If node in target set, return node; merge left/right results （节点在目标集合中则返回，合并左右结果） |

---

### BST

| Problem | Key Approach |
|---------|-------------|
| [95. Unique BSTs II](https://leetcode.com/problems/unique-binary-search-trees-ii/) | Enumerate roots 1–n; combine left/right subtree lists; memoize （枚举根1到n，组合左右子树列表，记忆化） |
| [96. Unique BSTs](https://leetcode.com/problems/unique-binary-search-trees/) | Catalan number DP: dp[n] = sum of dp[i-1] * dp[n-i] （卡特兰数DP：dp[n]=sum(dp[i-1]*dp[n-i])） |
| [230. Kth Smallest Element](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Inorder traversal with global counter （中序遍历+全局计数器） |
| [235. LCA of BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Use BST ordering: if node is between val1 and val2, it's the LCA （利用BST性质：节点值在val1和val2之间即为LCA） |
| [450. Delete Node in BST](https://leetcode.com/problems/delete-node-in-a-bst/) | Recurse to find node; if two children, replace with left subtree's max （递归定位节点，双子树时用左子树最大值替换） |
| [530. Minimum Absolute Difference](https://leetcode.com/problems/minimum-absolute-difference-in-bst/) | Inorder traversal; track previous node and compute min difference （中序遍历，追踪前驱节点，计算最小差值） |
| [538. Convert BST to Greater Tree](https://leetcode.com/problems/convert-bst-to-greater-tree/) | Reverse inorder (right→root→left); accumulate running sum （反中序(右到根到左)，累计运行和） |
| [700. Search in BST](https://leetcode.com/problems/search-in-a-binary-search-tree/) | Inorder-style recursion using BST ordering （利用BST顺序递归查找） |
| [701. Insert into BST](https://leetcode.com/problems/insert-into-a-binary-search-tree/) | Recurse left or right; create node when null reached （递归左或右，到null时创建节点） |
| [1038. BST to Greater Sum Tree](https://leetcode.com/problems/binary-search-tree-to-greater-sum-tree/) | Same as #538 （同第538题） |

---

### Graph

| Problem | Key Approach |
|---------|-------------|
| [127. Word Ladder](https://leetcode.com/problems/word-ladder/) | BFS from beginWord; try all 1-char mutations; filter by dictionary （BFS从beginWord出发，每步替换一个字符，过滤词典） |
| [130. Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | Connect border 'O's to dummy node; flip all 'O's not connected to dummy （将边缘O连接到哑节点，翻转所有未连接哑节点的O） |
| [133. Clone Graph](https://leetcode.com/problems/clone-graph/) | BFS with old→new node map; replicate adjacency lists （BFS+旧到新节点Map，复制邻接表） |
| [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | DFS flood-fill; count and flatten each island （DFS洪泛，统计并展平每个岛屿） |
| [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | DFS with onPath array to detect cycles; or BFS Kahn's on in-degrees （DFS+onPath数组检测环；或BFS Kahn入度算法） |
| [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | BFS: append in-degree-0 in order; DFS: postorder append then reverse （BFS：按顺序追加入度0的节点；DFS：后序追加后反转） |
| [310. Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) | Iteratively remove leaf nodes (degree 1) until ≤ 2 remain （迭代移除叶节点(度为1)，直到剩余<=2个） |
| [329. Longest Increasing Path in Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | DFS with memoization; each cell = 1 + max of valid neighbors （DFS+记忆化，每格=1+合法邻居的最大值） |
| [399. Evaluate Division](https://leetcode.com/problems/evaluate-division/) | Build weighted graph; BFS multiplying edge weights along path （建带权图，BFS沿路径乘积边权） |
| [547. Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | Union-Find; count connected components （并查集，计算连通分量数） |
| [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Union-Find; if two endpoints already connected, that edge is redundant （并查集，两端点已连通则该边冗余） |
| [694. Number of Distinct Islands](https://leetcode.com/problems/number-of-distinct-islands/) | DFS recording direction sequence as string; set counts distinct shapes （DFS记录方向序列为字符串，集合统计不同形状） |
| [695. Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | DFS flood-fill; track area during recursion （DFS洪泛，递归时追踪面积） |
| [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Dijkstra from source; return maximum shortest path （从源点Dijkstra，返回最大最短路径） |
| [785. Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) | BFS/DFS coloring; return false if adjacent nodes share same color （BFS/DFS着色，相邻节点同色则返回false） |
| [863. All Nodes Distance K](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/) | Build parent map via DFS; BFS from target tracking depth （DFS建父指针Map，从目标BFS按深度追踪） |
| [886. Possible Bipartition](https://leetcode.com/problems/possible-bipartition/) | Same as #785 （同第785题） |
| [924. Minimize Malware Spread](https://leetcode.com/problems/minimize-malware-spread/) | BFS from each initial node; candidate = largest component with no other initial node （从每个初始节点BFS，候选=不含其他初始节点的最大分量） |
| [947. Most Stones Removed](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/) | Union stones sharing row or column; answer = stones - component count （并查集合并共行或共列的石头，答案=石头数-分量数） |
| [990. Satisfiability of Equality Equations](https://leetcode.com/problems/satisfiability-of-equality-equations/) | Union equal variables; check no unequal pair in same component （合并相等变量，检查不等对是否在同一分量） |
| [1020. Number of Enclaves](https://leetcode.com/problems/number-of-enclaves/) | Fill border-connected land; count remaining 1s （填充边缘连接的陆地，统计剩余1的个数） |
| [1254. Number of Closed Islands](https://leetcode.com/problems/number-of-closed-islands/) | Fill border-connected 0-islands; count remaining 0-island floods （填充边缘连接的0-岛屿，统计剩余0-岛屿洪泛数） |
| [1361. Validate Binary Tree Nodes](https://leetcode.com/problems/validate-binary-tree-nodes/) | One node with in-degree 0 (root); others in-degree 1; traverse from root （入度0的节点为根，其余入度为1，从根遍历验证） |
| [1514. Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/) | Dijkstra variant with max-heap; multiply probabilities （Dijkstra变体+最大堆，乘积路径概率） |
| [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) | Kruskal's: sort all edges, union if not connected （Kruskal算法，排序所有边后并查集） |
| [1631. Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | Dijkstra variant; edge weight = max absolute difference （Dijkstra变体，边权=最大绝对差） |
| [1905. Count Sub Islands](https://leetcode.com/problems/count-sub-islands/) | DFS: if grid2's island has cell where grid1=0, not sub-island; count （DFS：grid2岛屿中有grid1=0的格子则不是子岛，统计数量） |
| [2101. Detonate Maximum Bombs](https://leetcode.com/problems/detonate-the-maximum-bombs/) | Build directed graph by blast radius; BFS count reachable from each （按炸弹爆炸半径建有向图，BFS统计每个起点的可达数） |

---

### BFS

| Problem | Key Approach |
|---------|-------------|
| [433. Minimum Genetic Mutation](https://leetcode.com/problems/minimum-genetic-mutation/) | BFS; each mutation one char change toward bank; return step count （BFS，每步单字符变换，返回步数） |
| [542. 01 Matrix](https://leetcode.com/problems/01-matrix/) | Multi-source BFS from all 0s; propagate distances outward （从所有0出发的多源BFS，向外传播距离） |
| [752. Open the Lock](https://leetcode.com/problems/open-the-lock/) | BFS from "0000"; each step turns one wheel ±1; filter deadends and visited （BFS从0000出发，每步转动一格，过滤死锁和已访问） |
| [773. Sliding Puzzle](https://leetcode.com/problems/sliding-puzzle/) | BFS on state strings; generate all next states by swapping 0 with neighbors （BFS遍历状态字符串，生成所有下一状态） |
| [841. Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/) | BFS from room 0 collecting keys; check if all rooms visited （从房间0 BFS收集钥匙，检查所有房间是否访问） |
| [909. Snakes and Ladders](https://leetcode.com/problems/snakes-and-ladders/) | BFS on 1D index with boustrophedon conversion; count steps （以蛇形转换为1D索引的BFS，统计步数） |
| [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Multi-source BFS from all rotten simultaneously; check any fresh remain （从所有腐烂橙同时多源BFS，检查是否有新鲜橙剩余） |
| [1091. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | BFS in 8 directions; count steps to (n-1, n-1) （8方向BFS，统计到(n-1,n-1)的步数） |
| [1306. Jump Game III](https://leetcode.com/problems/jump-game-iii/) | BFS; from index jump to `index ± arr[index]`; check target reached （BFS从下标跳+/-arr[index]，检查是否到达目标） |
| [1926. Nearest Exit from Entrance](https://leetcode.com/problems/nearest-exit-from-entrance-in-maze/) | BFS from entrance; first empty border cell (not entrance) is answer （从入口BFS，第一个非入口的空边界格为答案） |

---

### Backtracking

| Problem | Key Approach |
|---------|-------------|
| [17. Letter Combinations of Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Backtracking; iterate all letters mapped to each digit （回溯，遍历每个数字映射的所有字母） |
| [37. Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) | 1D array (i=index/9, j=index%9); try digits, validate row/col/box, recurse （一维数组(i=index/9,j=index%9)，尝试数字，验证行/列/宫，递归） |
| [39. Combination Sum](https://leetcode.com/problems/combination-sum/) | Backtracking allowing reuse (recurse with same start) （允许复用的回溯（用相同start递归）） |
| [40. Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | Sort + skip `nums[i] == nums[i-1]`; each element used once （排序+跳过nums[i]==nums[i-1]，每元素仅用一次） |
| [46. Permutations](https://leetcode.com/problems/permutations/) | Backtracking with `used` boolean array （回溯+used布尔数组） |
| [47. Permutations II](https://leetcode.com/problems/permutations-ii/) | Sort + skip `nums[i] == nums[i-1] && !used[i-1]` （排序+跳过nums[i]==nums[i-1]&&!used[i-1]） |
| [51. N-Queens](https://leetcode.com/problems/n-queens/) | Track column, main diagonal, anti-diagonal sets; place queen per row （追踪列、主对角线、反对角线集合，每行放一个皇后） |
| [52. N-Queens II](https://leetcode.com/problems/n-queens-ii/) | Same as #51 but count solutions only （同第51题，仅统计方案数） |
| [77. Combinations](https://leetcode.com/problems/combinations/) | Backtracking with start index ensuring no repeats （回溯+起始下标，避免重复） |
| [78. Subsets](https://leetcode.com/problems/subsets/) | Backtracking with start index; record every prefix （回溯+起始下标，记录所有前缀） |
| [79. Word Search](https://leetcode.com/problems/word-search/) | Backtracking on grid; track visited; check boundaries （网格回溯+visited追踪，检查边界） |
| [89. Gray Code](https://leetcode.com/problems/gray-code/) | Backtracking from 0; change one bit at a time; check if visited （从0回溯，每次变一位，检查是否已访问） |
| [90. Subsets II](https://leetcode.com/problems/subsets-ii/) | Sort + skip duplicate elements at same recursion depth （排序+同层跳过重复元素） |
| [93. Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/) | Pick 1–3 chars, validate, collect exactly 4 valid segments （选1-3个字符，验证后精确收集4段） |
| [131. Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | Try all substrings from start; add to list if palindrome （尝试从start出发的所有子串，是回文则加入） |
| [216. Combination Sum III](https://leetcode.com/problems/combination-sum-iii/) | Backtracking with start; exactly k numbers summing to n （回溯+起始；恰好k个数字之和为n） |
| [301. Remove Invalid Parentheses](https://leetcode.com/problems/remove-invalid-parentheses/) | Try keeping or removing each bracket; prune when leftCount < 0 （尝试保留或删除每个括号，leftCount<0时剪枝） |
| [473. Matchsticks to Square](https://leetcode.com/problems/matchsticks-to-square/) | Backtracking into 4 equal-sum buckets; bitmask memoization （回溯分配到4个等和桶，超出最优或与前桶相同时剪枝） |
| [491. Non-Decreasing Subsequences](https://leetcode.com/problems/non-decreasing-subsequences/) | Prune if value < last or already used at this depth （剪枝：值<上一个或本层已用则跳过） |
| [526. Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/) | Backtracking 1–n; check `start % i == 0 || i % start == 0` （回溯1到n，任一整除条件满足则合法） |
| [638. Shopping Offers](https://leetcode.com/problems/shopping-offers/) | Backtracking through special offers; compare with non-offer buying （回溯遍历特惠组合，与不用特惠对比） |
| [784. Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/) | Branch on uppercase and lowercase for each character （对每个字符分支大小写两种情况） |
| [967. Numbers With Same Consecutive Differences](https://leetcode.com/problems/numbers-with-same-consecutive-differences/) | Backtracking digit by digit; branch by ±k from last digit （逐位回溯，从末位+/-k分支） |
| [980. Unique Paths III](https://leetcode.com/problems/unique-paths-iii/) | DFS with `used` grid; count paths visiting all non-obstacle cells （DFS+used网格，统计访问所有非障碍格的路径数） |
| [996. Number of Squareful Arrays](https://leetcode.com/problems/number-of-squareful-arrays/) | Sort + permutation backtracking; prune if adjacent sum not perfect square （排序+全排列回溯，相邻和非完全平方则剪枝） |
| [1079. Letter Tile Possibilities](https://leetcode.com/problems/letter-tile-possibilities/) | Sort tiles; backtracking with `used`; prune duplicate tiles （排序拼字块，回溯+used，重复拼块时剪枝） |
| [1219. Path with Maximum Gold](https://leetcode.com/problems/path-with-maximum-gold/) | DFS with visited set; try all starting cells （DFS+visited集合，尝试所有起点） |
| [1593. Split String Into Max Unique Substrings](https://leetcode.com/problems/split-a-string-into-the-max-number-of-unique-substrings/) | Backtracking; skip if substring already used; maximize unique count （回溯，子串已出现则跳过，最大化唯一子串数） |
| [1723. Find Minimum Time to Finish All Jobs](https://leetcode.com/problems/find-minimum-time-to-finish-all-jobs/) | Backtracking k workers; prune if exceeding best or worker load matches previous （回溯k个工人，超最优或工人负载与前相同时剪枝） |
| [1849. Splitting Into Descending Consecutive Values](https://leetcode.com/problems/splitting-a-string-into-descending-consecutive-values/) | Backtracking; prune if not strictly decreasing by 1 （回溯，不严格递减1时剪枝） |
| [2305. Fair Distribution of Cookies](https://leetcode.com/problems/fair-distribution-of-cookies/) | Distribute to k children minimizing maximum （分配给k个小朋友，最小化最大值） |
| [2850. Minimum Moves to Spread Stones](https://leetcode.com/problems/minimum-moves-to-spread-stones-over-grid/) | Backtracking from cells with >1 stone to empty cells; track total steps （从石头>1的格回溯到空格，追踪总步数） |

---

### Dynamic Programming

| Problem | Key Approach |
|---------|-------------|
| [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Expand around each center (i,j); track longest （以每个中心向外扩展(i,j)，追踪最长） |
| [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Track current and next farthest; increment steps when current reached （追踪当前和下一可达最远，到达边界时步数+1） |
| [53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | `dp[i] = max(dp[i-1] + nums[i], nums[i])`; track overall max （dp[i]=max(dp[i-1]+nums[i],nums[i])，追踪全局最大） |
| [55. Jump Game](https://leetcode.com/problems/jump-game/) | Track max reachable index; ensure i ≤ max （追踪最大可达下标，确保i<=max） |
| [63. Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | `dp[i][j] = dp[i-1][j] + dp[i][j-1]`; set to 0 at obstacles （dp[i][j]=dp[i-1][j]+dp[i][j-1]，障碍处置0） |
| [64. Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | `dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]` （dp[i][j]=min(dp[i-1][j],dp[i][j-1])+grid[i][j]） |
| [72. Edit Distance](https://leetcode.com/problems/edit-distance/) | If chars equal, inherit diagonal; else min(insert, delete, replace) + 1 （字符相等继承对角线，否则min(插入,删除,替换)+1） |
| [97. Interleaving String](https://leetcode.com/problems/interleaving-string/) | `dp[i][j]` true if s1[0..i] and s2[0..j] interleave to form s3[0..i+j] （dp[i][j]为true表示s1[0..i]和s2[0..j]可交错成s3[0..i+j]） |
| [120. Triangle](https://leetcode.com/problems/triangle/) | `dp[i][j] = min(dp[i-1][j-1], dp[i-1][j]) + triangle[i][j]` （dp[i][j]=min(dp[i-1][j-1],dp[i-1][j])+triangle[i][j]） |
| [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | State machine DP with k transactions; track hold/not-hold states （状态机DP含k次交易，追踪持有/未持有状态） |
| [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Sort or hash set; if next number exists, dp + 1; else reset to 1 （排序或哈希集合，下一个数字存在则dp+1，否则重置为1） |
| [143. Integer Break](https://leetcode.com/problems/integer-break/) | `dp[i] = max(j * max(dp[i-j], i-j))` （dp[i]=max(j*max(dp[i-j],i-j))） |
| [152. Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Track both dpMax and dpMin; new max/min = max of three candidates （同时追踪dpMax和dpMin，新极值取三者之最） |
| [174. Dungeon Game](https://leetcode.com/problems/dungeon-game/) | Reverse DP from bottom-right; `dp[i][j] = max(1, min(down, right) - grid[i][j])` （从右下角反向DP，dp[i][j]=max(1,min(下,右)-grid[i][j])） |
| [198. House Robber](https://leetcode.com/problems/house-robber/) | `dp[i] = max(dp[i-2] + nums[i], dp[i-1])` （dp[i]=max(dp[i-2]+nums[i],dp[i-1])） |
| [213. House Robber II](https://leetcode.com/problems/house-robber-ii/) | Max of rob(0..n-2) and rob(1..n-1) （取rob(0..n-2)和rob(1..n-1)的最大值） |
| [221. Maximal Square](https://leetcode.com/problems/maximal-square/) | `dp[i][j] = min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1` when cell is 1 （cell为1时dp[i][j]=min(dp[i-1][j],dp[i-1][j-1],dp[i][j-1])+1） |
| [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | For each i, compare all j < i where nums[j] < nums[i]; max length （对每个i比较所有j<i且nums[j]<nums[i]，取最大长度） |
| [322. Coin Change](https://leetcode.com/problems/coin-change/) | `dp[amount] = min(dp[amount - coin] + 1)` over all coins （dp[amount]=min(dp[amount-coin]+1)遍历所有硬币） |
| [354. Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | Sort by width desc, height asc; LIS on heights （按宽度降序/高度升序排序，在高度上求LIS） |
| [368. Largest Divisible Subset](https://leetcode.com/problems/largest-divisible-subset/) | Sort; `dp[i]` = largest subset ending at nums[i] where each element divides next （排序，dp[i]=以nums[i]结尾且各元素整除后继的最大子集） |
| [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | 0/1 knapsack; target = sum/2; boolean DP array （0/1背包，目标=总和/2，布尔DP数组） |
| [494. Target Sum](https://leetcode.com/problems/target-sum/) | Reduce to subset sum: goal = (target + sum) / 2 （转化为子集和：目标=(target+sum)/2） |
| [509. Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | Iterative DP from dp[0]=0, dp[1]=1 （从dp[0]=0,dp[1]=1迭代DP） |
| [518. Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Unbounded knapsack; `dp[j] += dp[j - coin]` （无界背包，dp[j]+=dp[j-coin]） |
| [583. Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) | `len1 + len2 - 2 * LCS` （len1+len2-2*LCS） |
| [712. Minimum ASCII Delete Sum](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/) | 2D DP similar to edit distance; initialize with ASCII sums （类编辑距离的2D DP，初始化为ASCII码之和） |
| [718. Maximum Length of Repeated Subarray](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) | `dp[i][j] = dp[i-1][j-1] + 1` when match; track max （字符匹配时dp[i][j]=dp[i-1][j-1]+1，追踪最大） |
| [740. Delete and Earn](https://leetcode.com/problems/delete-and-earn/) | Aggregate same-value sums; then house-robber DP （聚合同值的分数之和，然后做打家劫舍DP） |
| [918. Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) | max(Kadane result, totalSum - min subarray) （max(Kadane结果，总和-最小子数组)） |
| [931. Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/) | DP row by row; dp[i][j] = min of three above neighbors + grid （逐行DP，dp[i][j]=上方三个邻居之最小+grid值） |
| [983. Minimum Cost for Tickets](https://leetcode.com/problems/minimum-cost-for-tickets/) | Memoized DFS; at each travel day try 1/7/30-day passes （记忆化DFS，每个旅行日尝试1/7/30天票） |
| [1024. Video Stitching](https://leetcode.com/problems/video-stitching/) | Sort by start; greedily extend coverage choosing furthest end （按起点排序，贪心选择覆盖最远末点的片段） |
| [1049. Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/) | Find subset closest to sum/2 (0/1 knapsack); answer = total - 2*subset （找最接近sum/2的子集(0/1背包)，答案=总和-2*子集） |
| [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | If chars equal add 1 from diagonal; else max of left/up （字符相等则对角+1，否则取左/上最大） |
| [1235. Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Sort by start; DP with binary search for next available job （按开始时间排序，DP+二分找下一个可用任务） |
| [1262. Greatest Sum Divisible by Three](https://leetcode.com/problems/greatest-sum-divisible-by-three/) | Track dp0/dp1/dp2; update on each number （追踪dp0/dp1/dp2，对每个数字更新） |
| [2140. Solving Questions with Brainpower](https://leetcode.com/problems/solving-questions-with-brainpower/) | Reverse DP: `dp[i] = max(dp[i + brainpower[i] + 1] + points[i], dp[i+1])` （反向DP：dp[i]=max(dp[i+难度+1]+分数, dp[i+1])） |
| [2320. Count Ways to Place Houses](https://leetcode.com/problems/count-ways-to-place-houses/) | `dp[i] = dp[i-1] + dp[i-2]`; square the 1-side result （dp[i]=dp[i-1]+dp[i-2]，一侧结果的平方） |

---

### Greedy / Interval

| Problem | Key Approach |
|---------|-------------|
| [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Track current and next farthest; increment steps at boundary （追踪当前和下一可达最远，到达边界时步数+1） |
| [55. Jump Game](https://leetcode.com/problems/jump-game/) | Track max reachable index （追踪最大可达下标，确保i<=max） |
| [134. Gas Station](https://leetcode.com/problems/gas-station/) | Prefix sums; position with min prefix sum + 1 is start （前缀和，前缀和最小处+1为起点） |
| [135. Candy](https://leetcode.com/problems/candy/) | Two-pass greedy: left-to-right then right-to-left; sum （两遍贪心：左到右，再右到左，求和） |
| [253. Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | Dual pointer on sorted starts/ends; count peak concurrent （起止时间分别排序，双指针统计峰值并发数） |
| [274. H-Index](https://leetcode.com/problems/h-index/) | Sort descending; h-index = largest i where citations[i] ≥ papers so far （降序排序，最大满足citations[i]>=论文数的i即为H指数） |
| [435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Sort by end; greedily keep non-overlapping; count removals （按结束时间排序，贪心保留不重叠区间，统计移除数） |
| [452. Minimum Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | Count non-overlapping regions; equal endpoints overlap （统计不重叠区域数，等端点也视为重叠） |
| [502. IPO](https://leetcode.com/problems/ipo/) | Sort by capital; max-heap for profits; greedily pick highest-profit available （按资本排序，利润最大堆，贪心选最高可用利润） |
| [57. Insert Interval](https://leetcode.com/problems/insert-interval/) | Merge overlapping with new interval; pass non-overlapping through （不重叠区间直接通过，重叠则合并新区间） |
| [791. Custom Sort String](https://leetcode.com/problems/custom-sort-string/) | Count chars; output in order's sequence first, then remaining （统计字符，先按order顺序输出，再输出剩余） |
| [2611. Mice and Cheese](https://leetcode.com/problems/mice-and-cheese/) | Sort by `reward1[i] - reward2[i]` desc; give top k to cheese1 （按reward1-reward2降序排序，前k个给奶酪1） |

---

### Heap

| Problem | Key Approach |
|---------|-------------|
| [264. Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) | Track indices for multiples of 2,3,5; pick min next ugly; increment index （追踪2,3,5的倍数索引，选最小下一丑数，推进索引） |
| [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Max-heap (lower half) + min-heap (upper half); balance sizes （最大堆(下半)+最小堆(上半)，保持大小平衡） |
| [313. Super Ugly Number](https://leetcode.com/problems/super-ugly-number/) | PriorityQueue of (value, index, prime) tuples; merge and deduplicate （PriorityQueue存(值,索引,质因子)元组，合并并去重） |
| [373. Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) | PriorityQueue for K-sorted-array merging （PriorityQueue合并K个有序数组） |
| [378. Kth Smallest in Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | PriorityQueue merging sorted rows/diagonals （PriorityQueue合并有序行/对角线） |
| [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Sort by Euclidean distance squared; take first k （按欧式距离平方排序，取前k个） |

---

### Design

| Problem | Key Approach |
|---------|-------------|
| [146. LRU Cache](https://leetcode.com/problems/lru-cache/) | HashMap + doubly-linked list; move accessed entries to head （HashMap+双向链表，访问的条目移到头部） |
| [380. Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | Map (value→index) + list; on remove swap with last element （Map(值到下标)+列表，删除时与末尾元素交换） |
| [919. Complete Binary Tree Inserter](https://leetcode.com/problems/complete-binary-tree-inserter/) | BFS-based insertion queue; maintain nodes with empty children （BFS插入队列，维护有空子节点的节点） |

---

### Math / String

| Problem | Key Approach |
|---------|-------------|
| [6. Zigzag Conversion](https://leetcode.com/problems/zigzag-conversion/) | Assign chars to rows with direction flag; reverse at row 0 and numRows-1 （用方向标志分配字符到各行，在行0和numRows-1时反向） |
| [9. Palindrome Number](https://leetcode.com/problems/palindrome-number/) | Convert to string; left/right pointer check （转字符串，左右指针检验） |
| [12. Integer to Roman](https://leetcode.com/problems/integer-to-roman/) | Map each thousands/hundreds/tens/ones digit to Roman （将千/百/十/个位分别映射为罗马数字） |
| [13. Roman to Integer](https://leetcode.com/problems/roman-to-integer/) | Iterate right-to-left; subtract if current < previous （从右到左遍历，当前<前一个则减，否则加） |
| [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | Compare char by char at index i across all strings （按下标i逐字符比较所有字符串） |
| [28. Find First Occurrence](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | Slide through haystack; compare substring when first chars match （滑动遍历haystack，首字符匹配时比较子串） |
| [50. Pow(x, n)](https://leetcode.com/problems/powx-n/) | Fast exponentiation: `pow(x, n/2)^2`; handle negative n and odd n （快速幂：pow(x,n/2)的平方，处理负n和奇数n） |
| [58. Length of Last Word](https://leetcode.com/problems/length-of-last-word/) | Trim trailing spaces; count from end until space found （去尾部空格，从末尾数到空格） |
| [67. Add Binary](https://leetcode.com/problems/add-binary/) | Simulate binary addition from right with carry （从右模拟二进制加法进位） |
| [68. Text Justification](https://leetcode.com/problems/text-justification/) | Group words; distribute spaces (last line and single-word: left-justified) （分组单词，分发空格（末行和单词行：左对齐）） |
| [149. Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) | For each point i, map slope (dx/gcd, dy/gcd) to count （对每个点i，将斜率(dx/gcd,dy/gcd)映射到计数） |
| [151. Reverse Words in String](https://leetcode.com/problems/reverse-words-in-a-string/) | Reverse entire string; reverse each word; trim spaces （反转整个字符串，反转每个单词，去多余空格） |
| [202. Happy Number](https://leetcode.com/problems/happy-number/) | Simulate digit-square sum; detect cycle with visited set （模拟各位平方和，用visited集合检测循环） |
| [204. Count Primes](https://leetcode.com/problems/count-primes/) | Sieve of Eratosthenes; mark multiples starting at i² （埃氏筛法，从i的平方开始标记倍数） |
| [263. Ugly Number](https://leetcode.com/problems/ugly-number/) | Divide by 2,3,5 repeatedly; ugly if result equals 1 （反复除以2,3,5，结果为1则为丑数） |
| [372. Super Pow](https://leetcode.com/problems/super-pow/) | Modular exponentiation with base 1337; recursively compute （模1337的快速幂，递归计算） |
| [383. Ransom Note](https://leetcode.com/problems/ransom-note/) | Compare character frequency arrays (size 26) （比较字符频率数组(大小26)） |
| [877. Stone Game](https://leetcode.com/problems/stone-game/) | Always true; first player can always choose optimal parity （先手必胜，先手总能选最优奇偶性） |
| [1201. Ugly Number III](https://leetcode.com/problems/ugly-number-iii/) | Binary search on answer; count multiples with inclusion-exclusion and LCM （对答案二分，用容斥原理和LCM统计倍数） |

---

### Bit Manipulation / Matrix / Randomized

| Problem | Key Approach |
|---------|-------------|
| [48. Rotate Image](https://leetcode.com/problems/rotate-image/) | Transpose along diagonal, then reverse each row （沿对角线转置，再逐行反转） |
| [54. Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Maintain left/right/top/bottom boundaries; shrink after each pass （维护左右上下边界，每遍后收缩） |
| [59. Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) | Same boundary approach as #54, filling values （同第54题，填充数值） |
| [73. Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | Record if first row/col has zeros; use them as markers （记录首行/列是否有零，用首行列作标记） |
| [137. Single Number II](https://leetcode.com/problems/single-number-ii/) | Count array indexed by value/10000; filter entries with count 1 （按value/10000索引的计数数组，过滤count为1的条目） |
| [201. Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) | Repeatedly AND right with right-1 until right ≤ left （循环将right与right-1做AND，直到right<=left） |
| [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Left-pass prefix products × right-pass postfix products （左遍前缀积x右遍后缀积） |
| [289. Game of Life](https://leetcode.com/problems/game-of-life/) | Three-row sliding window tracks neighbor counts （三行滑动窗口追踪邻居数） |
| [382. Linked List Random Node](https://leetcode.com/problems/linked-list-random-node/) | Reservoir sampling: replace with probability 1/index （水库抽样：以1/index概率替换） |
| [384. Shuffle an Array](https://leetcode.com/problems/shuffle-an-array/) | Fisher-Yates: swap position i with random position ≥ i （Fisher-Yates：位置i与随机>=i的位置交换） |
| [398. Random Pick Index](https://leetcode.com/problems/random-pick-index/) | Reservoir sampling over indices matching target （水库抽样遍历所有匹配目标的下标） |
| [427. Construct Quad Tree](https://leetcode.com/problems/construct-quad-tree/) | Recursively split into 4 quadrants; merge if all children same-value leaves （递归拆成4个象限，子节点全同值时合并为叶子） |
| [867. Transpose Matrix](https://leetcode.com/problems/transpose-matrix/) | New m×n array swapping rows and columns （新m*n数组，交换行列） |
| [1260. Shift 2D Grid](https://leetcode.com/problems/shift-2d-grid/) | Flatten to 1D, reverse, reverse sub-segments （展平为1D，反转，再反转子段） |
| [1329. Sort Matrix Diagonally](https://leetcode.com/problems/sort-the-matrix-diagonally/) | Use `i-j` as diagonal key; sort each diagonal and reconstruct （用i-j作对角线键，排序并重建每条对角线） |
| [2073. Time Needed to Buy Tickets](https://leetcode.com/problems/time-needed-to-buy-tickets/) | People before k buy up to `tickets[k]`; after buy up to `tickets[k]-1` （k之前的人买min(tickets,tickets[k])次，之后的买min(tickets,tickets[k]-1)次） |
