import re

filepath = r"C:\Users\lorra\projects\ai-infra-manager\skills\tech\algorithms\LeetCode Problem Collection.md"

# problem_number -> correct LeetCode slug
correct_slugs = {
    # Linked List
    "82": "remove-duplicates-from-sorted-list-ii",
    "83": "remove-duplicates-from-sorted-list",
    "876": "middle-of-the-linked-list",
    # Two Pointers
    "75": "sort-colors",
    "80": "remove-duplicates-from-sorted-array-ii",
    "167": "two-sum-ii-input-array-is-sorted",
    "977": "squares-of-a-sorted-array",
    # Sliding Window
    "3": "longest-substring-without-repeating-characters",
    "395": "longest-substring-with-at-least-k-repeating-characters",
    "438": "find-all-anagrams-in-a-string",
    # Binary Search
    "34": "find-first-and-last-position-of-element-in-sorted-array",
    "1011": "capacity-to-ship-packages-within-d-days",
    "1539": "kth-missing-positive-number",
    # Prefix Sum
    "303": "range-sum-query-immutable",
    "304": "range-sum-query-2d-immutable",
    # Monotonic Stack
    "1475": "final-prices-with-a-special-discount-in-a-shop",
    "1944": "number-of-visible-people-in-a-queue",
    # Binary Tree
    "102": "binary-tree-level-order-traversal",
    "103": "binary-tree-zigzag-level-order-traversal",
    "104": "maximum-depth-of-binary-tree",
    "105": "construct-binary-tree-from-preorder-and-inorder-traversal",
    "106": "construct-binary-tree-from-inorder-and-postorder-traversal",
    "107": "binary-tree-level-order-traversal-ii",
    "114": "flatten-binary-tree-to-linked-list",
    "116": "populating-next-right-pointers-in-each-node",
    "117": "populating-next-right-pointers-in-each-node-ii",
    "144": "binary-tree-preorder-traversal",
    "199": "binary-tree-right-side-view",
    "236": "lowest-common-ancestor-of-a-binary-tree",
    "297": "serialize-and-deserialize-binary-tree",
    "331": "verify-preorder-serialization-of-a-binary-tree",
    "515": "find-largest-value-in-each-tree-row",
    "543": "diameter-of-binary-tree",
    "637": "average-of-levels-in-binary-tree",
    "662": "maximum-width-of-binary-tree",
    "889": "construct-binary-tree-from-preorder-and-postorder-traversal",
    "958": "check-completeness-of-a-binary-tree",
    "988": "smallest-string-starting-from-leaf",
    "1110": "delete-nodes-and-return-forest",
    "1161": "maximum-level-sum-of-a-binary-tree",
    "1457": "pseudo-palindromic-paths-in-a-binary-tree",
    "1644": "lowest-common-ancestor-of-a-binary-tree-ii",
    "1650": "lowest-common-ancestor-of-a-binary-tree-iii",
    "1676": "lowest-common-ancestor-of-a-binary-tree-iv",
    # BST
    "95": "unique-binary-search-trees-ii",
    "96": "unique-binary-search-trees",
    "230": "kth-smallest-element-in-a-bst",
    "235": "lowest-common-ancestor-of-a-binary-search-tree",
    "450": "delete-node-in-a-bst",
    "530": "minimum-absolute-difference-in-bst",
    "700": "search-in-a-binary-search-tree",
    "701": "insert-into-a-binary-search-tree",
    "1038": "binary-search-tree-to-greater-sum-tree",
    # Graph
    "329": "longest-increasing-path-in-a-matrix",
    "863": "all-nodes-distance-k-in-binary-tree",
    "947": "most-stones-removed-with-same-row-or-column",
    "2101": "detonate-the-maximum-bombs",
    # BFS
    "1926": "nearest-exit-from-entrance-in-maze",
    # Backtracking
    "17": "letter-combinations-of-a-phone-number",
    "1593": "split-a-string-into-the-max-number-of-unique-substrings",
    "1849": "splitting-a-string-into-descending-consecutive-values",
    "2850": "minimum-moves-to-spread-stones-over-grid",
    # DP
    "712": "minimum-ascii-delete-sum-for-two-strings",
    # Greedy
    "452": "minimum-number-of-arrows-to-burst-balloons",
    # Heap
    "378": "kth-smallest-element-in-a-sorted-matrix",
    # Math/String
    "28": "find-the-index-of-the-first-occurrence-in-a-string",
    "151": "reverse-words-in-a-string",
    # Matrix
    "1329": "sort-the-matrix-diagonally",
}

row_pattern = re.compile(
    r'(\| \[(\d+)\. [^\]]+\]\(https://leetcode\.com/problems/)([^/]+)(/\) \| .+)'
)

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed = 0
new_lines = []
for line in lines:
    m = row_pattern.match(line)
    if m:
        num = m.group(2)
        current_slug = m.group(3)
        if num in correct_slugs and correct_slugs[num] != current_slug:
            new_line = m.group(1) + correct_slugs[num] + m.group(4) + '\n' if not line.endswith('\n') else m.group(1) + correct_slugs[num] + m.group(4)
            new_lines.append(new_line)
            fixed += 1
            print(f"  #{num}: {current_slug} -> {correct_slugs[num]}")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\nFixed {fixed} URLs.")
