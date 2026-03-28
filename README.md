# 🤖 Claude Code Agent Mode — Find & Fix Bugs FREE on Windows

> **Run Claude Code in Full Agent Mode Using LM Studio — No API Key, No Cloud, Zero Cost**
>
> The agent reads your files, finds bugs, fixes them, and writes documentation. Everything runs on your own machine.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-v2.1.81-orange)](https://docs.anthropic.com/claude-code)
[![LM Studio](https://img.shields.io/badge/LM%20Studio-v0.4.3-blue)](https://lmstudio.ai)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011-lightgrey)](https://lmstudio.ai)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## What This Video Covers

This is **Part 2** of the local Claude Code series.

**Part 1** covered the full setup — connecting Claude Code to LM Studio, fixing the context window error, the --tools none optimization. [Link in description]

**This video** takes the same setup and runs it in full agent mode against a real broken codebase.

**What happened:**
- Agent read 4 files autonomously
- Found 12 bugs — 6 planted, 6 it discovered itself
- Fixed 3 files directly on disk
- Wrote 179 lines of documentation
- Total time — ~45 minutes on CPU-only hardware

---

## System Used

| Component | Value |
|-----------|-------|
| OS | Windows 11 |
| RAM | 32 GB |
| GPU | None (Intel UHD integrated) |
| Model | Qwen 3.5 2B Q4_K_M (1.94 GB) |
| Claude Code | v2.1.81 |
| LM Studio | v0.4.3 |

---

## Config Updates From Part 1

Two changes needed for agent mode to work reliably:

```powershell
# PowerShell profile — Microsoft.PowerShell_profile.ps1

$env:ANTHROPIC_BASE_URL = "http://169.254.145.96:1234"
$env:ANTHROPIC_AUTH_TOKEN = "lmstudio"
$env:CLAUDE_CODE_API_TIMEOUT_MS = "900000"   # increased from 300000
$env:CLAUDE_CODE_MAX_TOKENS = "19000"        # new — prevents context overflow

function claude-local {
    claude --model qwen3.5-2b --tools none
}

function claude-agent {
    claude --model qwen3.5-2b
}
```

### Why These Values

| Setting | Value | Reason |
|---------|-------|--------|
| Timeout | 900,000ms (15 min) | Agent mode prompts take 10+ min to process on CPU |
| Max tokens | 19,000 | Prevents n_past = n_tokens edge case that clears memory |

---

## LM Studio Settings for Agent Mode

| Setting | Value |
|---------|-------|
| Context Length | 32,000 |
| Max Concurrent Predictions | 1 |
| Prompt Template | Qwen-ChatML |

> **Important:** Select the **Qwen-ChatML** preset in the Inference tab. Without this you'll get a Jinja template error on every request.

---

## The Broken Project

Four files with 6 hidden bugs. Clone and test it yourself.

```
broken-app/
├── app.py          — Flask REST API (2 bugs)
├── database.py     — SQLite layer (1 bug)
├── utils.py        — Helper functions (2 bugs)
└── requirements.txt — Dependencies (1 bug)
```

### The 6 Hidden Bugs

| # | File | Bug | Type |
|---|------|-----|------|
| 1 | app.py | No error handling in get_user_route — crashes if user not found | Missing handling |
| 2 | app.py | No null check on request body — crashes if empty POST | Missing validation |
| 3 | database.py | SQL injection — string concatenation instead of parameterised query | Security |
| 4 | utils.py | String not converted to float before multiplication | Type error |
| 5 | utils.py | O(n²) nested loop — should use a set | Performance |
| 6 | requirements.txt | sqlite3 is standard library — should not be in requirements | Bad practice |

### The 6 Bugs the Agent Found Itself

| # | File | Bug |
|---|------|-----|
| 7 | app.py | No rate limiting on endpoints |
| 8 | database.py | Inconsistent naming conventions |
| 9 | app.py | Magic number — hardcoded 0.1 discount rate |
| 10 | database.py | Hardcoded database path |
| 11 | app.py | Flask debug=True enabled in production |
| 12 | Multiple | No docstrings on any function |

---

## The 4 Prompts Used

### Prompt 1 — Read the project
```
Read every file in this project and tell me what it does
```
Time: 9m 25s — Agent read all 4 files and described the project correctly.

### Prompt 2 — Find bugs
```
Find every bug, security issue and bad practice in this 
codebase. List them all clearly before fixing anything.
```
Time: 1m 26s — Faster because context was already in memory from Prompt 1.
Result: 12 bugs found.

### Prompt 3 — Fix everything
```
Now fix every issue you found. Write the corrected 
code directly to the files.
```
Time: 19m 42s — Agent rewrote 3 files on disk.

### Prompt 4 — Write documentation
```
Write complete documentation for this entire project 
including a setup guide, API reference and contributing 
guidelines. Save it as DOCUMENTATION.md
```
Time: 6m 47s — 179 lines written.

---

## What the LM Studio Logs Show

### Token growth across the session

| Prompt | n_tokens | Why |
|--------|----------|-----|
| Prompt 1 | 19,893 | Initial system prompt + tool definitions |
| Prompt 2 | ~22,000 | + Prompt 1 response added to history |
| Prompt 3 | ~25,000 | + Bug list added to history |
| Prompt 4 | ~29,500 | + All file contents + fixes added |

### The warning you'll see on every request
```
Reasoning setting 'on' cannot be converted to any custom KVs
```
Claude Code always requests extended thinking mode. Qwen 3.5 2B doesn't support it. LM Studio ignores it and continues normally. Not an error — ignore it.

### The tool call moment
```
[SamplingSwitch] Entering switch 'qwenToolsSamplingSwitch' 
(triggered by string: "<tool_call>")
```
This is the exact moment the agent decides to call a tool. You never see this in a normal chat window. The logs show you when the agent shifts from thinking to acting.

---

## Honest Results

### What worked well ✅
- Found all 6 planted bugs
- Found 6 additional real issues
- Fixed files correctly on disk
- Wrote accurate API documentation
- Recovered from every error autonomously

### What didn't work perfectly ⚠️
- SQL injection fix used f-strings instead of parameterised queries — still technically vulnerable
- Hallucinated a GitHub URL in documentation
- Listed rate limiting as fixed — only added try/except, not actual rate limiting
- Wrong bash syntax on first attempt (Windows vs Linux path confusion)

### Final scorecard

| Metric | Result |
|--------|--------|
| Bugs planted | 6 |
| Bugs found total | 12 |
| Files fixed on disk | 3 |
| Documentation lines written | 179 |
| Total session time | ~45 min |
| Peak token count | ~29,500 |
| Conversation messages | 68 |
| Errors hit | 6 |
| Errors recovered automatically | 6 |

---

## Files in This Repo

```
broken-app/          — Original broken files (6 hidden bugs)
fixed-app/           — Agent-fixed versions for comparison
DOCUMENTATION.md     — Documentation written by the agent
```

---

## Quick Reference

```powershell
# Setup
. $PROFILE
cd broken-app
git init

# Launch agent mode
claude-agent

# The 4 prompts (run in order, same terminal session)
# 1. Read every file in this project and tell me what it does
# 2. Find every bug, security issue and bad practice. List them before fixing.
# 3. Now fix every issue you found. Write corrected code directly to the files.
# 4. Write complete documentation including setup guide and API reference. Save as DOCUMENTATION.md
```

---

## Resources

| Resource | Link |
|----------|------|
| Part 1 — Full Setup Guide | Link in description |
| LM Studio | [lmstudio.ai](https://lmstudio.ai) |
| Claude Code Docs | [docs.anthropic.com/claude-code](https://docs.anthropic.com/en/docs/claude-code) |
| Qwen Models | [huggingface.co/Qwen](https://huggingface.co/Qwen) |

---

<p align="center">
  <strong>Built with real testing, real logs, real hardware</strong><br>
  <em>Windows 11 · 32GB RAM · No GPU · Intel UHD integrated</em><br>
  <em>March 2026</em>
</p>

