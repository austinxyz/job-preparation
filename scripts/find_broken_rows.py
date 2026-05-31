import re

filepath = r"C:\Users\lorra\projects\ai-infra-manager\skills\tech\algorithms\LeetCode Problem Collection.md"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped.startswith('|') or stripped.startswith('|---') or stripped == '| Problem | Key Approach |':
        continue
    # Count unescaped pipes (not preceded by backslash, not inside backticks)
    # Remove backtick spans first
    no_code = re.sub(r'`[^`]*`', 'CODE', stripped)
    # Count pipes
    pipes = no_code.count('|')
    # A normal row has exactly 3 pipes: | col1 | col2 |
    if pipes != 3:
        print(f"Line {i} ({pipes} pipes): {stripped[:120]}")
