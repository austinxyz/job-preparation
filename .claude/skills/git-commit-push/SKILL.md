---
name: Git Commit and Push
description: Stage all changes (including new files), commit with a descriptive message, and push to GitHub. Use this skill when the user asks to commit, push, or save changes to git.
---

# Git Commit and Push Skill

Automatically stage all changes (including new files), create a commit, and push to the remote repository.

## Usage

This skill will:
1. Run `git status` to show what will be committed
2. Run `git add .` to stage all changes (including new files)
3. Create a commit with a descriptive message
4. Push to the remote repository (origin/main)

## Commit Message Format

Follow conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `test:` - Test updates
- `chore:` - Build/tool updates

Example:
```
feat: add Kubernetes GPU scheduling skill note and book-reader skill

- Distill Jimmy Song's GPU infra book into structured reading notes
- Create book-reader skill for reusable online book processing
- Add raw material notes per section under raw_material/books/gpu-infra/
```

## GitHub Repository

- **Username**: austinxyz
- **Repository**: https://github.com/austinxyz/ai-infra-manager.git
- **Branch**: main

## What Gets Committed

- Modified files
- New files (untracked files)
- Deleted files

**Note**: Files listed in `.gitignore` are automatically excluded.
