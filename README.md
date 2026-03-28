# Local Claude Code Agent — Practical Guide
### "I gave my free local AI a real job — here's every decision it made and where it failed"

---

## PREREQUISITES

Everything from the previous video already in place:
- LM Studio installed and running
- Claude Code installed (v2.1.78+)
- PowerShell profile configured
- `claude-local` and `claude-agent` shortcuts working

---

## STEP 1 — LM STUDIO SETTINGS

Before starting, confirm these settings in LM Studio:

| Setting | Value |
|---|---|
| Model | qwen3.5-2b (GGUF Q4_K_M) |
| Context Length | 32,000 |
| Max Concurrent Predictions | 1 |
| Server | Running |

To change context length:
1. Click loaded model in LM Studio
2. Find Context Length
3. Set to 32,000
4. Eject and reload model
5. Verify server is running

---

## STEP 2 — CREATE THE TEST PROJECT

Open PowerShell and run:

```powershell
mkdir broken-app
cd broken-app
```

Create the following 4 files exactly as shown. These contain **6 hidden bugs** for the agent to find.

---

### FILE 1 — app.py

```python
from flask import Flask, request, jsonify
from database import get_user, create_user
from utils import format_response, calculate_discount

app = Flask(__name__)

@app.route('/user/<id>', methods=['GET'])
def get_user_route(id):
    user = get_user(id)
    return jsonify(user)

@app.route('/user', methods=['POST'])
def create_user_route():
    data = request.json
    username = data['username']
    email = data['email']
    result = create_user(username, email)
    return jsonify(result)

@app.route('/discount', methods=['GET'])
def discount_route():
    price = request.args.get('price')
    discount = calculate_discount(price, 0.1)
    response = format_response(discount)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```

**Hidden bugs in this file:**
- Bug 1: `get_user_route` returns raw database object with no error handling — crashes if user not found
- Bug 2: `create_user_route` has no null check on `data` — crashes if request body is empty

---

### FILE 2 — database.py

```python
import sqlite3

def get_connection():
    conn = sqlite3.connect('users.db')
    return conn

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

def create_user(username, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email)
    )
    conn.commit()
    conn.close()
    return {"status": "created"}

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    return results
```

**Hidden bug in this file:**
- Bug 3: SQL injection vulnerability in `get_user` — string concatenation instead of parameterised query

---

### FILE 3 — utils.py

```python
def format_response(data):
    if data == None:
        return {}
    response = {
        "data": data,
        "status": "success"
    }
    return response

def calculate_discount(price, discount_rate):
    discounted = price * (1 - discount_rate)
    return discounted

def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                if items[i] not in duplicates:
                    duplicates.append(items[i])
    return duplicates

def parse_config(config_string):
    pairs = config_string.split(',')
    config = {}
    for pair in pairs:
        key, value = pair.split('=')
        config[key] = value
    return config
```

**Hidden bugs in this file:**
- Bug 4: `calculate_discount` — `price` comes in as string from request args, multiplication will fail
- Bug 5: `find_duplicates` — O(n²) nested loop, inefficient for large lists, should use a set
- Bug 6: `parse_config` — no error handling, crashes if any pair doesn't contain `=`

---

### FILE 4 — requirements.txt

```
flask==1.1.2
requests==2.20.0
sqlite3
```

**Note:** Flask 1.1.2 and requests 2.20.0 are outdated versions with known security issues. `sqlite3` is a standard library module and should not be in requirements.txt.

---

## STEP 3 — VERIFY YOUR SETUP

Before launching the agent, confirm your profile is loaded:

```powershell
. $PROFILE
```

Confirm you're in the right folder:

```powershell
ls
```

You should see: `app.py`, `database.py`, `utils.py`, `requirements.txt`

---

## STEP 4 — LAUNCH AGENT MODE

```powershell
claude-agent
```

Walk through the setup prompt — trust the folder when asked.

Confirm model is loaded:
```
/model
```

Should show: `qwen3.5-2b`

---

## STEP 5 — TEST PROMPTS IN ORDER

Run these prompts in sequence without restarting the terminal between them.

---

### PROMPT 1 — Read Test

```
Read every file in this project and tell me what it does
```

**Switch to LM Studio logs immediately after hitting enter.**

**What to watch for:**
- `n_keep` — total tokens Claude Code sent
- Token count climbing as it reads each file
- RAM climbing in Task Manager
- How long each file read takes

**Expected token counts (approximate):**
| Component | Tokens |
|---|---|
| Claude Code system prompt | ~3,256 |
| app.py | ~280 |
| database.py | ~220 |
| utils.py | ~260 |
| requirements.txt | ~20 |
| Your question | ~12 |
| **Total** | **~4,048** |

**Log line to screenshot:**
```
slot update_slots: id 1 | task X | new prompt, n_ctx_slot = 32000, n_keep = XXXX
```

---

### PROMPT 2 — Bug Hunt (Do not restart terminal)

```
Find every bug, security issue and bad practice in this 
codebase. List them all clearly before fixing anything.
```

**What to watch for in logs:**
- `n_past` — should be higher than Prompt 1 (checkpoint effect from last video)
- Agent reading files again — watch token reuse
- How many of the 6 bugs it finds

**Scoring:**
| Bug | Description | Likely Found? |
|---|---|---|
| Bug 1 | No error handling in get_user_route | ✅ Usually |
| Bug 2 | No null check on request body | ✅ Usually |
| Bug 3 | SQL injection in database.py | ✅ Usually |
| Bug 4 | String type not converted to float | ⚠️ Sometimes |
| Bug 5 | O(n²) inefficient loop | ⚠️ Sometimes |
| Bug 6 | No error handling in parse_config | ❌ Often missed |

**Note for video:** Whatever score you get — 4/6, 5/6 — is the honest content. Do not re-run to get a better score.

---

### PROMPT 3 — Fix Everything (Do not restart terminal)

```
Now fix every issue you found. Write the corrected 
code directly to the files.
```

**This is the agent magic moment.**

**What to watch for:**
- Agent calling `read_file` tool — visible in Claude Code terminal
- Agent calling `write_file` tool — files on disk actually changing
- Agent calling `bash` tool to verify — sometimes runs python checks
- Any retry loops if it's not satisfied with output

**Open File Explorer alongside the terminal** — watch the files update in real time. This is visually powerful for the video.

**LM Studio logs to watch:**
- Each tool call adds tokens to `n_past`
- RAM holding steady or climbing slightly
- Processing time per tool call

---

### PROMPT 4 — Push It Further (Do not restart terminal)

```
Write complete documentation for this entire project 
including a setup guide, API reference and contributing 
guidelines. Save it as DOCUMENTATION.md
```

**This is where Qwen 3.5 2B hits its limit.**

**What to watch for in logs:**
```
n_past approaching 28,000-30,000 of 32,000
```

**What the model might do wrong:**
- Hallucinate a function that does not exist
- Write incomplete API reference and stop mid-sentence
- Reference the wrong parameter names
- Copy-paste same section twice

**Do not hide this — this IS the content.** Show the log line showing context pressure and explain exactly why it happened.

---

## STEP 6 — FIX 1: .claudeignore

Create a `.claudeignore` file in your project folder:

```
__pycache__/
*.pyc
*.log
*.db
.env
node_modules/
dist/
.git/
```

Relaunch the agent and run Prompt 1 again. Compare `n_keep` before and after.

**Expected result:** Token count drops even on this small project. On a real project with node_modules the difference is dramatic.

---

## STEP 7 — FIX 2: Swap to Larger Model

In LM Studio:
1. Eject qwen3.5-2b
2. Search for `qwen 7b` in Model Search
3. Download GGUF Q4_K_M version (~4.4GB)
4. Load it
5. Confirm server still running

Update PowerShell profile:

```powershell
notepad $PROFILE
```

Change the model name in both functions:

```powershell
function claude-agent {
    claude --model qwen7b-instruct
}
```

Reload profile:
```powershell
. $PROFILE
```

Relaunch and run the same prompts. Compare results.

---

## STEP 8 — FINAL SCORECARD

Fill this in during recording based on actual results:

| Task | Qwen 2B | Qwen 7B |
|---|---|---|
| Files read | | |
| Bugs found (out of 6) | | |
| Fixes written correctly | | |
| Docs quality | | |
| Total time | | |
| Peak RAM | | |
| Peak tokens | | |

---

## LOG LINES TO SCREENSHOT DURING RECORDING

These are your key video moments — have LM Studio open and visible:

1. First `n_keep` value after Prompt 1
2. `n_past` value after Prompt 2 (checkpoint effect)
3. Each tool call appearing in Claude Code terminal
4. Context pressure warning when hitting 28,000+ tokens
5. RAM peak in Task Manager during Prompt 4

---

## TROUBLESHOOTING

**Agent not writing files:**
- Check you launched with `claude-agent` not `claude-local`
- Type `/tools` in Claude Code to confirm tools are enabled

**Response timing out:**
- Confirm `CLAUDE_CODE_API_TIMEOUT_MS=300000` is in profile
- Run `. $PROFILE` to reload

**Model ejecting:**
- Context length dropped back to 4,096 in LM Studio
- Set back to 32,000, eject and reload model

**Agent finds 0 bugs:**
- Model too small or confused by prompt
- Try: "List every potential issue you can find in database.py" — single file first

---

## GITHUB README CONTENT FOR THIS VIDEO

```markdown
## Files Included
- broken-app/ — test project with 6 intentional bugs
- .claudeignore — template for token reduction

## The 6 Hidden Bugs
1. No error handling in get_user_route (app.py line 9)
2. No null check on request body (app.py line 15)
3. SQL injection in get_user (database.py line 9)
4. String not converted to float before multiplication (utils.py line 11)
5. O(n²) nested loop — should use a set (utils.py line 19)
6. No error handling in parse_config (utils.py line 29)

## Commands
claude-local   → fast mode, no tools, ~2 min
claude-agent   → full agent mode, all tools, ~12 min

## LM Studio Settings
Context Length: 32,000
Model: qwen3.5-2b or qwen7b-instruct
```

---

## QUICK REFERENCE CARD

```powershell
# Setup
. $PROFILE
cd broken-app
claude-agent

# Test sequence (same terminal, no restart between)
# Prompt 1: Read test
# Prompt 2: Bug hunt  
# Prompt 3: Fix everything
# Prompt 4: Write documentation

# After testing — swap model in LM Studio
# Repeat same 4 prompts with larger model
# Compare results
```
