# Samanvaya (समन्वय) — AI-Native Recursive Code Evolution

> **Agents coordinate. Conflicts auto-resolve. Code evolves through observable generations. No human in the loop.**

---

## See It Work

### `safe` — "Can I touch this file?"

Three agents are already on `main.py`. Should you proceed?

```console
$ python samanvaya.py safe --file backend/main.py

✅ SAFE — 3 agent(s) also on backend/main.py
   Different kinds of work: buddhi, manas, mahat
   Their changes are in different sections. Git merges cleanly.
   • agent-search [manas] vishnu — 1747-1800
   • agent-graph [mahat] vishnu — 1936-1949
   • agent-synthesis [buddhi] vishnu — 1956-1994
```

Three agents. One file. **Zero coordination needed.** Different layers (kinds of work), different line ranges. Proceed.

Now check a file where someone is doing the SAME kind of work:

```console
$ python samanvaya.py safe --file backend/buddhi.py

⚡ CHECK — 1 agent(s) doing the SAME kind of work on backend/buddhi.py
   Layer: buddhi (Synthesis — reasoning, prompts, response generation)
   • agent-synthesis — vishnu — lines: entire file

   If your lines DON'T overlap theirs → safe, proceed.
   If they DO → the auto-resolver will merge them via LLM.
```

### `status` — Who is working on what?

```console
$ python samanvaya.py status

LAYER      AGENT                     STAGE        TOUCHING
---------------------------------------------------------------------------
Retrieval  agent-search              vishnu       indexer/search.py, backend/main.py:1747-1800
Knowledge  agent-graph               vishnu       backend/graph_memory.py, backend/main.py:1936-1949
Synthesis  agent-synthesis           vishnu       backend/buddhi.py, backend/main.py:1956-1994
```

### `resolve` — AI resolves conflicts automatically

```console
$ python samanvaya.py resolve

Found 1 conflict(s)

⚡ backend/main.py [buddhi] — agent-synthesis, agent-new
   Overlap: 15 lines → SEMANTIC
   → LLM resolving...
   → RESOLVED: 2fdd4883c149

Done. 1/1 resolved. Zero human touchpoints.
```

### `auto` — Fully autonomous recursive evolution

```console
$ python samanvaya.py auto --layer buddhi --max 3 \
    --problems "Search latency p95 is 2.3s target under 1s.,Vasudev entity returns 0 graph results.,Buddhi synthesis uses generic fallback for 60% of queries."

🔄 Samanvaya Autonomous Evolution Loop
   Problems: 3 | Max generations: 3

🔍 [gen-0003] OBSERVING: Search latency p95 is 2.3s
   Formulating fix via LLM...
   Layer: purusa | indexer/search.py
   📡 Deploying...
   ✅ Outcome: stable — latency p95: -70% (2.3s → 0.7s)

🔍 [gen-0004] OBSERVING: Vasudev entity returns 0 graph results
   Formulating fix via LLM...
   Layer: manas | backend/query_processor.py
   📡 Deploying...
   ✅ Outcome: stable — recall (Sanskrit entities): +7%

🔍 [gen-0005] OBSERVING: Buddhi synthesis uses generic fallback for 60% of queries
   Formulating fix via LLM...
   Layer: buddhi | backend/buddhi.py
   📡 Deploying...
   ✅ Outcome: stable — generic fallback rate: -30%, response specificity: +12%

🏁 Loop complete. 3/3 generations stable.
```

### `lineage` — The evolutionary tree

```console
$ python samanvaya.py lineage

GEN        PARENT     LAYER      INTENT                                             OUTCOME
------------------------------------------------------------------------------------------------------------------------
gen-0000   genesis    buddhi     Add Buddhi module for granthi-bheda reasoning      stable (errors: 0)
gen-0001   gen-0000   manas      Reduce search latency by capping ILIKE patterns    stable (errors: 0)
gen-0002   gen-0001   mahat      Fix graph recall: English-to-Sanskrit mapping      stable (errors: 0)
gen-0003   gen-0002   purusa     Resolve high search latency from ILIKE scans       stable (errors: 0)
gen-0004   gen-0003   manas      Enhanced entity expansion for Sanskrit recall      stable (errors: 0)
gen-0005   gen-0004   buddhi     Enhanced query intent classification               stable (errors: 0)

🌳 Evolutionary tree (6 generations):
├─ gen-0000 [buddhi] Add Buddhi module for structured reasoning
  ├─ gen-0001 [manas] Reduce search latency
  ├─ gen-0002 [mahat] Fix graph recall entity mapping
  ├─ gen-0003 [purusa] Resolve high search latency
  ├─ gen-0004 [manas] Enhanced entity expansion
  └─ gen-0005 [buddhi] Enhanced query intent classification
```

---

## How It Works

```
Agent declares: "I'm working on main.py:1956-1994, layer=buddhi (synthesis code)"
                │
                ▼
Other agent:    samanvaya safe --file main.py
                → "3 agents here, all different layers → SAFE"
                → Proceeds immediately. No wait. No coordination.
                │
                ▼
If same-layer:  samanvaya resolve
                → LLM reads both diffs → merges → commits resolution
                → No human touchpoints.
                │
                ▼
After deploy:   samanvaya evolve --intent "..." --change "..."
                → Records the generation with parent, intent, observed
                → samanvaya outcome --id gen-X --status stable
                → Next generation learns from this one
                → Forever.
```

## Layers = Kinds of Work

"Layer" just means **what kind of code you're writing.** Different kinds don't collide.

| Layer | Kind of Work | Example Files |
|-------|-------------|---------------|
| **manas** | Retrieval | `search.py`, RAG pipeline |
| **buddhi** | Synthesis | `buddhi.py`, prompt templates |
| **mahat** | Knowledge Graph | `graph_memory.py`, RAM keys |
| **purusa** | Intent | `query_processor.py`, routing |
| **brahman** | Corpus | `data/chunks/`, embeddings |

## Get It

```bash
git clone https://github.com/prashantpandey-creator/samanvaya.git
cd samanvaya

# Core — no dependencies needed
python samanvaya.py safe --file main.py

# LLM features — set one of these
export GROQ_API_KEY="..."    # or DEEPSEEK_API_KEY, GEMINI_API_KEY
python samanvaya.py resolve
python samanvaya.py auto --problems "problem1,problem2,problem3"
```

## Dashboard

```bash
python3 -m http.server 8765
open http://localhost:8765/dashboard.html
```

Shows agents by layer, file conflicts, granthi stages, lineage tree. Auto-refreshes every 5 seconds.

## Why

Multi-agent codebases have two problems nobody has solved together:

1. **False conflicts.** Git sees "same file modified → conflict" but can't tell whether the changes actually overlap. Samanvaya adds one piece of information — the layer — and that single addition eliminates most coordination overhead.

2. **Static code.** Software is treated as a finished artifact. It isn't. Each deployment produces new data, new metrics, new problems. Samanvaya treats each deployment as a **generation** — with observable parents, intent, and outcomes. The codebase becomes a living lineage.

## Research Grounding

This architecture draws from and connects to:

- **Darwin Gödel Machine** (ICLR 2026) — Self-modifying agents with empirical validation
- **HyperAgents** (Meta, 2026) — Metacognitive self-improvement loops
- **Weave** (Ataraxy Labs) — Entity-level merge, 95% reduction in false conflicts
- **Kitchen Loop** (March 2026) — 1,094+ autonomous PRs, zero regressions
- **STORM** (May 2026) — State-oriented multi-agent coordination
- **Anthropic** (May 2026) — >80% of production code authored by Claude, 8x developer throughput

## License

MIT
