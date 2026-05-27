import re

filepath = r"C:\Users\lorra\projects\ai-infra-manager\skills\tech\algorithms\LeetCode Problem Collection.md"

# Additional slug aliases (shorter URLs used in the file)
translations = {
    "remove-duplicates": "快慢指针去重",
    "middle-of-linked-list": "快指针到尾时，慢指针在中点",
    "sort-colors-dutch-national-flag": "三路划分，追踪p0和p2指针",
    "two-sum-ii-sorted-array": "左右指针，根据和与目标大小内移",
    "squares-of-sorted-array": "左右指针，较大的平方从末尾填入",
    "longest-substring-without-repeating": "窗口字符计数，重复时左移",
    "longest-substring-with-at-least-k-repeating": "枚举1-26种不同字符数，对每种找最长合法窗口",
    "find-all-anagrams": "need/window双Map+valid计数，valid==need.size时记下标",
    "find-first-and-last-position": "两次二分：左边界（收右）和右边界（收左）",
    "capacity-to-ship-packages": "对载重量二分，最小化天数函数",
    "kth-missing-positive": "线性扫描比较期望值与实际值，调整剩余k",
    "range-sum-query": "预计算前缀和，查询用preSum[j+1]-preSum[i]",
    "range-sum-query-2d": "二维前缀和，容斥原理处理矩形查询",
    "final-prices-with-special-discount": "找下一个更小价格做差即折后价",
    "number-of-visible-people-in-queue": "统计从单调栈中弹出的元素数",
    "level-order-traversal": "标准BFS逐层遍历",
    "zigzag-level-order": "BFS，按层奇偶交替addFirst/addLast",
    "maximum-depth": "深度=max(左,右)+1",
    "construct-from-preorderinorder": "前序首元素为根，在中序中找根拆分左右",
    "construct-from-inorderpostorder": "后序末元素为根，在中序中找根拆分左右",
    "level-order-traversal-ii": "BFS用addFirst实现逆序输出",
    "flatten-to-linked-list": "展开左右子树，左子树尾接右子树，左置null",
    "populating-next-right-pointers": "遍历(node1,node2)对，覆盖三种兄弟关系",
    "populating-next-right-pointers-ii": "BFS逐层赋next指针",
    "preorder-traversal": "标准前序遍历",
    "right-side-view": "BFS记录每层最后元素；或前序DFS先走右子树",
    "lowest-common-ancestor": "节点等于p或q则返回，左右均非空则为LCA",
    "serialize-and-deserialize": "前序加null节点序列化；或BFS层序",
    "verify-preorder-serialization": "非空节点入-1出+2，空节点入-1，初始边=1，为0时合法",
    "find-largest-value-per-row": "BFS记录每层最大值",
    "diameter": "当前节点直径=左深+右深，维护全局最大",
    "average-of-levels": "BFS对每层求平均",
    "maximum-width": "BFS带节点ID(左=2*id,右=2*id+1)，宽度=最后-最前+1",
    "construct-from-preorderpostorder": "前序首为根，在后序中找前序[start+1]确定左子树大小",
    "check-completeness": "BFS，出现null后后续必须全为null",
    "smallest-string-from-leaf": "DFS带字符串前缀，叶子处比较保留最小",
    "delete-nodes-return-forest": "DFS追踪hasParent，被删节点的子节点成为新根",
    "maximum-level-sum": "BFS对每层求和，找最大",
    "pseudo-palindromic-paths": "DFS+大小10的计数数组，叶子处至多一个数字奇数次",
    "lca-ii-pq-may-not-exist": "追踪p和q是否均找到，仅两者均确认时返回LCA",
    "lca-iii-parent-pointers": "父指针构成链表，找两链表的交叉点",
    "lca-iv-set-of-targets": "节点在目标集合中则返回，合并左右结果",
    "unique-bsts-ii": "枚举根1到n，组合左右子树列表，记忆化",
    "unique-bsts": "卡特兰数DP：dp[n]=sum(dp[i-1]*dp[n-i])",
    "kth-smallest-element": "中序遍历+全局计数器",
    "lca-of-bst": "利用BST性质：节点值在val1和val2之间即为LCA",
    "delete-node-in-bst": "递归定位节点，双子树时用左子树最大值替换",
    "minimum-absolute-difference": "中序遍历，追踪前驱节点，计算最小差值",
    "search-in-bst": "利用BST顺序递归查找",
    "insert-into-bst": "递归左或右，到null时创建节点",
    "bst-to-greater-sum-tree": "同第538题",
    "longest-increasing-path-in-matrix": "DFS+记忆化，每格=1+合法邻居的最大值",
    "all-nodes-distance-k": "DFS建父指针Map，从目标BFS按深度追踪",
    "most-stones-removed": "并查集合并共行或共列的石头，答案=石头数-分量数",
    "detonate-maximum-bombs": "按炸弹爆炸半径建有向图，BFS统计每个起点的可达数",
    "nearest-exit-from-entrance": "从入口BFS，第一个非入口的空边界格为答案",
    "letter-combinations-of-phone-number": "回溯，遍历每个数字映射的所有字母",
    "split-string-into-max-unique-substrings": "回溯，子串已出现则跳过，最大化唯一子串数",
    "splitting-into-descending-consecutive-values": "回溯，不严格递减1时剪枝",
    "minimum-moves-to-spread-stones": "从石头>1的格回溯到空格，追踪总步数",
    "minimum-ascii-delete-sum": "类编辑距离的2D DP，初始化为ASCII码之和",
    "minimum-arrows-to-burst-balloons": "统计不重叠区域数，等端点也视为重叠",
    "kth-smallest-in-sorted-matrix": "PriorityQueue合并有序行/对角线",
    "find-first-occurrence": "滑动遍历haystack，首字符匹配时比较子串",
    "reverse-words-in-string": "反转整个字符串，反转每个单词，去多余空格",
    "sort-matrix-diagonally": "用i-j作对角线键，排序并重建每条对角线",
}

row_pattern = re.compile(
    r'^(\| \[\d+\. [^\]]+\]\(https://leetcode\.com/problems/([^/]+)/\) \| )(.+?)( \|)\s*$'
)

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

updated = 0
new_lines = []
for line in lines:
    m = row_pattern.match(line.rstrip('\n'))
    if m:
        prefix = m.group(1)
        slug = m.group(2)
        approach = m.group(3)
        suffix = m.group(4)
        if slug in translations and '（' not in approach:
            chinese = translations[slug]
            new_line = f"{prefix}{approach} （{chinese}）{suffix}\n"
            new_lines.append(new_line)
            updated += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Patched {updated} additional rows.")
