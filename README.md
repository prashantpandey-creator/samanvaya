# Samanvaya (समन्वय) — AI-Native Recursive Code Evolution

> **Git tells you a file was changed. Samanvaya tells you whether that change matters — and if it does, an LLM resolves it. Then the code evolves itself.**

---

## What It Does

One tool. Seven commands.

```bash
samanvaya safe --file main.py     # "Can I touch this file right now?"
samanvaya status                   # "Who is working on what?"
samanvaya resolve                  # AI resolves all conflicts automatically
samanvaya watch                    # Continuous auto-resolution
samanvaya evolve --layer ...       # Record a new generation of code evolution
samanvaya outcome --id ...         # Record deploy metrics
samanvaya lineage                  # Show the full evolutionary tree
samanvaya auto --problems "..."    # Fully autonomous recursive loop
```

---

## The Problem

Multiple AI agents work on the same codebase. They all touch the same files.
Git sees "same file modified → conflict risk" but can't tell whether the
changes actually overlap semantically. Agents hesitate. Humans get pulled in
to resolve "conflicts" that git would have merged cleanly.

## The Solution

**Layers = kinds of work.** An agent declares what kind of code it's writing
(search, synthesis, graph, intent, data) before touching any file. Two agents
at different layers touching the same file is safe — their changes are in
different sections. Git merges mechanically. Same layer + overlapping lines =
LLM resolves automatically.

## The Bigger Picture

Code is never "done." Each deployment is a **generation.** The agent observes
metrics, formulates improvements, deploys, measures outcomes, and feeds
everything back into the next generation. The lineage IS the memory of the
system — not who wrote the code, but **why it was written, what it observed,
and what it produced.**

```
gen-0000 [buddhi] Add structured reasoning layer
  └─ gen-0001 [manas] Reduce search latency by capping ILIKE patterns
      └─ gen-0002 [mahat] Fix graph recall for Sanskrit entities
          └─ gen-0003 [purusa] Improve query intent classification
```

## Install

```bash
git clone https://github.com/prashantpandey-creator/samanvaya.git
cd samanvaya
pip install -r requirements.txt  # none required for core; groq optional for LLM features
```

## Quick Start

```bash
# 1. Initialize in any repo
python samanvaya.py init

# 2. Check if a file is safe to touch
python samanvaya.py safe --file src/main.py

# 3. See all active agents
python samanvaya.py status

# 4. Run the autonomous evolution loop
python samanvaya.py auto --layer buddhi --max 5 \
    --problems "Fix search latency,Add entity resolution,Improve synthesis quality"
```

## Dashboard

```bash
python3 -m http.server 8765
# Open http://localhost:8765/dashboard.html
```

## Requirements

- Python 3.9+
- Git
- Optional: GROQ_API_KEY, DEEPSEEK_API_KEY, or GEMINI_API_KEY for LLM-powered resolution and evolution

## License

MIT
