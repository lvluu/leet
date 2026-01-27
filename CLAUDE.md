# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Custom Commands

- **`/add-pattern`** - Add new DSA pattern documentation with animations. Handles creating docs, generating animations, and updating SUMMARY.md.

## Project Overview

This is a GitBook documentation project containing free, open-source guides for coding interview patterns. The content follows the structure from "Grokking the Coding Interview" by DesignGurus.io.

## Commands

### Local Development
```bash
# Install GitBook CLI (first time only)
npm install -g gitbook-cli

# Install dependencies
gitbook install

# Serve locally (available at http://localhost:4000)
gitbook serve

# Build static site (outputs to _book/)
gitbook build
```

## Architecture

- **docs/** - All documentation content (GitBook root specified in `.gitbook.yaml` and `book.json`)
  - `README.md` - Introduction page
  - `SUMMARY.md` - Table of contents (defines sidebar navigation)
  - Each pattern has its own directory with markdown files
- **book.json** - GitBook configuration (plugins, theme settings)
- **.github/workflows/gitbook.yml** - Auto-deploys to gh-pages branch on push to main

## Content Structure

Each coding pattern directory typically contains:
- `introduction.md` - Pattern overview, when to use it, complexity analysis
- `advanced-techniques.md` - Extended techniques (where applicable)

The `SUMMARY.md` file controls the GitBook sidebar navigation. When adding new content, update this file to include the new pages.

## Animation Generator

The `animator/` directory contains a Python tool for generating algorithm visualization GIFs.

### Setup
```bash
cd animator
uv sync  # Install dependencies
```

### Usage
```bash
# List all available animation scenarios
uv run animator list

# Generate a specific animation
uv run animator generate sliding_window_fixed

# Generate with custom data
uv run animator generate two_pointers_opposite --data "[1,2,3,7,11]" --speed 400

# Generate all animations to docs
uv run animator generate-all --output-dir ../docs/.gitbook/assets/animations
```

### Adding New Animations
1. **Renderers** (`animator/src/animator/renderers/`) - Define HOW to draw data structures
2. **Patterns** (`animator/src/animator/patterns/`) - Define WHAT steps to animate
3. **Scenarios** (`animator/src/animator/scenarios/registry.py`) - Pre-configured examples

### Embedding in Markdown
```markdown
![Animation](../.gitbook/assets/animations/sliding-window/sliding_window_fixed.gif)
```

## Deployment

Pushes to `main` automatically trigger GitHub Actions to build and deploy to the `gh-pages` branch.
