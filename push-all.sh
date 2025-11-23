#!/bin/bash

# push-all: git add, commit with intelligent message, and push

set -e

# Add all changes
echo "Staging all changes..."
git add .

# Check if there are any changes to commit
if git diff --cached --quiet && git diff --quiet; then
    echo "No changes to commit."
    exit 0
fi

# Generate commit message based on changes
echo "Analyzing changes to generate commit message..."

# Get list of changed files
CHANGED_FILES=$(git diff --cached --name-only)
MODIFIED_FILES=$(git diff --cached --name-only --diff-filter=M)
ADDED_FILES=$(git diff --cached --name-only --diff-filter=A)
DELETED_FILES=$(git diff --cached --name-only --diff-filter=D)

# Count file changes
NEW_FILES=$(echo "$ADDED_FILES" | wc -l)
MODIFIED_COUNT=$(echo "$MODIFIED_FILES" | wc -l)
DELETED_COUNT=$(echo "$DELETED_FILES" | wc -l)

# Build summary
SUMMARY=""
if [ "$NEW_FILES" -gt 0 ]; then
    SUMMARY="${SUMMARY}+${NEW_FILES} "
fi
if [ "$MODIFIED_COUNT" -gt 0 ]; then
    SUMMARY="${SUMMARY}~${MODIFIED_COUNT} "
fi
if [ "$DELETED_COUNT" -gt 0 ]; then
    SUMMARY="${SUMMARY}-${DELETED_COUNT} "
fi

# Build commit message based on changes
# Build a concise single-line summary
SUMMARY_PARTS=""
if echo "$CHANGED_FILES" | grep -q "\.py$"; then
    PYTHON_COUNT=$(echo "$CHANGED_FILES" | grep "\.py$" | wc -l)
    SUMMARY_PARTS="${SUMMARY_PARTS}Python(${PYTHON_COUNT}) "
fi
if echo "$CHANGED_FILES" | grep -q "\.md$"; then
    SUMMARY_PARTS="${SUMMARY_PARTS}docs "
fi
if echo "$CHANGED_FILES" | grep -q "\.json$"; then
    SUMMARY_PARTS="${SUMMARY_PARTS}data "
fi
if echo "$CHANGED_FILES" | grep -q "pyproject.toml\|uv.lock"; then
    SUMMARY_PARTS="${SUMMARY_PARTS}deps "
fi

# Build main message
if [ -n "$SUMMARY_PARTS" ]; then
    MAIN_MSG="Update ${SUMMARY_PARTS}"
else
    MAIN_MSG="Update project files"
fi

# Add file change summary
if [ -n "$SUMMARY" ]; then
    MAIN_MSG="${MAIN_MSG} - ${SUMMARY}files"
fi

# Trim whitespace
MAIN_MSG=$(echo "$MAIN_MSG" | sed 's/[[:space:]]*$//')

echo "Committing changes..."
echo "Commit message: $MAIN_MSG"
echo ""

git commit -m "$MAIN_MSG"

# Push to remote
echo "Pushing to remote..."
CURRENT_BRANCH=$(git branch --show-current)
REMOTE=$(git remote | head -1)

if [ -z "$REMOTE" ]; then
    echo "No remote configured. Skipping push."
    exit 0
fi

# Check if upstream is set
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "")

if [ -z "$UPSTREAM" ]; then
    echo "Setting upstream and pushing..."
    git push --set-upstream "$REMOTE" "$CURRENT_BRANCH"
else
    echo "Pushing to existing upstream..."
    git push
fi

echo "Done! All changes have been committed and pushed."

