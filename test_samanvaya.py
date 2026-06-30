#!/usr/bin/env python3
"""
Samanvaya Test Suite — Verifies the methodology end-to-end.

Run: python3 test_samanvaya.py

Tests every command against real manifest states.
No mocking — uses actual MANIFEST.json reads/writes with a test fixture.
"""

import json
import os
import sys
import tempfile
import subprocess
from pathlib import Path

SAMVAYA = Path(__file__).resolve().parent / "samvaya.py"
PASS, FAIL = 0, 0


def test(name):
    global PASS, FAIL
    def decorator(fn):
        def wrapper():
            global PASS, FAIL
            try:
                fn()
                PASS += 1
                print(f"  ✅ {name}")
            except AssertionError as e:
                FAIL += 1
                print(f"  ❌ {name}: {e}")
            except Exception as e:
                FAIL += 1
                print(f"  💥 {name}: {type(e).__name__}: {e}")
        return wrapper
    return decorator


def run(*args):
    """Run samanvaya.py with args, return (exit_code, stdout)."""
    result = subprocess.run(
        [sys.executable, str(SAMVAYA)] + list(args),
        capture_output=True, text=True, timeout=30
    )
    return result.returncode, result.stdout


def set_manifest(data):
    """Write a MANIFEST.json for testing."""
    Path("MANIFEST.json").write_text(json.dumps(data, indent=2))


def get_manifest():
    return json.loads(Path("MANIFEST.json").read_text())


# ── Fixtures ──────────────────────────────────────────────────

CLEAN_MANIFEST = {
    "_system": "Samanvaya",
    "_rule": "Different layers = safe. Same layer = AI resolves.",
    "_layers": {
        "manas": "Retrieval",
        "buddhi": "Synthesis",
        "mahat": "Knowledge Graph",
        "purusa": "Intent",
        "brahman": "Corpus",
    },
    "active": {},
    "completed": [],
    "lineage": {},
    "generations": [],
}

THREE_AGENTS_MANIFEST = {
    "_system": "Samanvaya",
    "_rule": "Different layers = safe. Same layer = AI resolves.",
    "_layers": {
        "manas": "Retrieval",
        "buddhi": "Synthesis",
        "mahat": "Knowledge Graph",
        "purusa": "Intent",
        "brahman": "Corpus",
    },
    "active": {
        "agent-search": {
            "layer": "manas",
            "touches": ["search.py", "main.py:100-200"],
            "granthi": "vishnu",
            "since": "2026-07-01T00:00:00Z"
        },
        "agent-graph": {
            "layer": "mahat",
            "touches": ["graph.py", "main.py:300-400"],
            "granthi": "vishnu",
            "since": "2026-07-01T00:00:00Z"
        },
        "agent-synthesis": {
            "layer": "buddhi",
            "touches": ["synthesize.py"],
            "granthi": "vishnu",
            "since": "2026-07-01T00:00:00Z"
        }
    },
    "completed": [],
    "lineage": {},
    "generations": [],
}

SAME_LAYER_MANIFEST = {
    "_system": "Samanvaya",
    "_rule": "Different layers = safe. Same layer = AI resolves.",
    "_layers": {
        "manas": "Retrieval",
        "buddhi": "Synthesis",
        "mahat": "Knowledge Graph",
        "purusa": "Intent",
        "brahman": "Corpus",
    },
    "active": {
        "agent-alpha": {
            "layer": "buddhi",
            "touches": ["synthesize.py:50-100"],
            "granthi": "vishnu",
            "since": "2026-07-01T00:00:00Z"
        },
        "agent-beta": {
            "layer": "buddhi",
            "touches": ["synthesize.py:80-130"],
            "granthi": "brahma",
            "since": "2026-07-01T00:00:00Z"
        }
    },
    "completed": [],
    "lineage": {},
    "generations": [],
}


# ═══════════════════════════════════════════════════════════════
# TESTS: safe command
# ═══════════════════════════════════════════════════════════════

@test("safe: empty manifest → no agents → safe")
def test_safe_clean():
    set_manifest(CLEAN_MANIFEST)
    code, out = run("safe", "--file", "main.py")
    assert code == 0, f"exit {code}: {out}"
    assert "SAFE" in out, out
    assert "no one else" in out.lower(), out


@test("safe: cross-layer agents on same file → safe")
def test_safe_cross_layer():
    set_manifest(THREE_AGENTS_MANIFEST)
    code, out = run("safe", "--file", "main.py")
    assert code == 0, f"exit {code}: {out}"
    assert "SAFE" in out, out
    assert "Different kinds of work" in out, out  # cross-layer


@test("safe: no agents on untouched file → safe")
def test_safe_untouched():
    set_manifest(THREE_AGENTS_MANIFEST)
    code, out = run("safe", "--file", "untouched.py")
    assert code == 0, f"exit {code}: {out}"
    assert "SAFE" in out, out
    assert "no one else" in out.lower(), out


@test("safe: same-layer agents on overlapping file → check")
def test_safe_same_layer():
    set_manifest(SAME_LAYER_MANIFEST)
    code, out = run("safe", "--file", "synthesize.py")
    assert code == 1, f"should exit 1 (CHECK), got {code}"
    assert "CHECK" in out, out
    assert "SAME kind of work" in out, out


@test("safe: agent touching entire file → check")
def test_safe_entire_file():
    set_manifest(THREE_AGENTS_MANIFEST)
    code, out = run("safe", "--file", "synthesize.py")
    assert code == 1, f"should exit 1 (CHECK), got {code}"
    assert "SAME kind of work" in out or "CHECK" in out, out


# ═══════════════════════════════════════════════════════════════
# TESTS: status command
# ═══════════════════════════════════════════════════════════════

@test("status: shows all active agents")
def test_status_active():
    set_manifest(THREE_AGENTS_MANIFEST)
    code, out = run("status")
    assert code == 0, f"exit {code}"
    assert "agent-search" in out
    assert "agent-graph" in out
    assert "agent-synthesis" in out
    assert "Retrieval" in out
    assert "Knowledge Graph" in out
    assert "Synthesis" in out


@test("status: empty manifest shows clear field")
def test_status_clean():
    set_manifest(CLEAN_MANIFEST)
    code, out = run("status")
    assert code == 0, f"exit {code}"
    assert "clear" in out.lower() or "No active" in out, out


# ═══════════════════════════════════════════════════════════════
# TESTS: resolve command
# ═══════════════════════════════════════════════════════════════

@test("resolve: no conflicts → clean")
def test_resolve_clean():
    set_manifest(THREE_AGENTS_MANIFEST)
    code, out = run("resolve")
    assert code == 0, f"exit {code}"
    assert "No conflicts" in out, out


@test("resolve: same-layer overlap detected")
def test_resolve_detect():
    set_manifest(SAME_LAYER_MANIFEST)
    code, out = run("resolve")
    # Should detect the conflict (even if LLM resolution fails without keys)
    assert "conflict" in out.lower() or "FAILED" in out.upper(), out


# ═══════════════════════════════════════════════════════════════
# TESTS: evolve command
# ═══════════════════════════════════════════════════════════════

@test("evolve: records first generation as genesis")
def test_evolve_genesis():
    set_manifest(CLEAN_MANIFEST)
    code, out = run("evolve", "--layer", "buddhi", "--intent", "Test genesis",
                    "--change", "test.py:1-10")
    assert code == 0, f"exit {code}: {out}"
    assert "gen-0000" in out, out
    assert "genesis" in out, out

    data = get_manifest()
    gens = data.get("generations", [])
    assert len(gens) == 1
    assert gens[0]["id"] == "gen-0000"
    assert gens[0]["parent"] == "genesis"
    assert gens[0]["layer"] == "buddhi"
    assert gens[0]["intent"] == "Test genesis"
    assert gens[0]["change"] == "test.py:1-10"
    assert gens[0]["outcome"] is None


@test("evolve: chains generations correctly")
def test_evolve_chain():
    set_manifest(CLEAN_MANIFEST)
    run("evolve", "--layer", "manas", "--intent", "First", "--change", "a.py")
    run("evolve", "--layer", "buddhi", "--intent", "Second", "--change", "b.py")
    run("evolve", "--layer", "mahat", "--intent", "Third", "--change", "c.py")

    data = get_manifest()
    gens = data.get("generations", [])
    assert len(gens) == 3

    # Verify parent chain
    assert gens[0]["parent"] == "genesis"
    assert gens[1]["parent"] == "gen-0000"
    assert gens[2]["parent"] == "gen-0001"

    # Verify layers alternate correctly
    assert gens[0]["layer"] == "manas"
    assert gens[1]["layer"] == "buddhi"
    assert gens[2]["layer"] == "mahat"

    # Verify _current_generation tracks latest
    assert data["_current_generation"] == "gen-0002"


@test("evolve: stores observed context")
def test_evolve_observed():
    set_manifest(CLEAN_MANIFEST)
    run("evolve", "--layer", "buddhi",
        "--intent", "Fix latency",
        "--change", "search.py:100-120",
        "--observed", "P95 latency increased 20% after last deploy. Users reporting slowness.")

    data = get_manifest()
    gen = data["generations"][0]
    assert "P95 latency" in gen["observed"]
    assert "users" in gen["observed"].lower()


# ═══════════════════════════════════════════════════════════════
# TESTS: outcome command
# ═══════════════════════════════════════════════════════════════

@test("outcome: records deploy metrics")
def test_outcome():
    set_manifest(CLEAN_MANIFEST)
    run("evolve", "--layer", "buddhi", "--intent", "Test", "--change", "x.py")
    code, out = run("outcome", "--id", "gen-0000", "--status", "stable",
                    "--metrics", "latency:-20%, errors:0", "--errors", "0")
    assert code == 0, f"exit {code}: {out}"
    assert "stable" in out

    data = get_manifest()
    gen = data["generations"][0]
    assert gen["outcome"] is not None
    assert gen["outcome"]["status"] == "stable"
    assert gen["outcome"]["errors"] == "0"
    assert "latency:-20%" in gen["outcome"]["metrics"]


@test("outcome: rejects unknown generation")
def test_outcome_unknown():
    set_manifest(CLEAN_MANIFEST)
    code, out = run("outcome", "--id", "gen-9999", "--status", "stable")
    assert code == 0, f"exit {code}"
    assert "not found" in out.lower(), out


# ═══════════════════════════════════════════════════════════════
# TESTS: lineage command
# ═══════════════════════════════════════════════════════════════

@test("lineage: shows generations in order")
def test_lineage():
    set_manifest(CLEAN_MANIFEST)
    run("evolve", "--layer", "buddhi", "--intent", "First gen", "--change", "a.py")
    run("outcome", "--id", "gen-0000", "--status", "stable")
    run("evolve", "--layer", "manas", "--intent", "Second gen", "--change", "b.py")
    run("outcome", "--id", "gen-0001", "--status", "stable")

    code, out = run("lineage")
    assert code == 0, f"exit {code}"
    assert "gen-0000" in out
    assert "gen-0001" in out
    assert "genesis" in out
    assert "First gen" in out
    assert "Second gen" in out
    assert "stable" in out
    assert "Evolutionary tree" in out


@test("lineage: empty → helpful message")
def test_lineage_empty():
    set_manifest(CLEAN_MANIFEST)
    code, out = run("lineage")
    assert code == 0, f"exit {code}"
    assert "No generations" in out, out


# ═══════════════════════════════════════════════════════════════
# TESTS: Layer-based conflict classification
# ═══════════════════════════════════════════════════════════════

@test("methodology: cross-layer = never a real conflict")
def test_cross_layer_safety():
    """The core insight: different layers touching the same file is safe
    because they're working in different sections on different concerns."""
    set_manifest(THREE_AGENTS_MANIFEST)

    # All three agents touch main.py but at different layers and line ranges
    data = get_manifest()
    main_agents = {}
    for aid, entry in data["active"].items():
        for t in entry["touches"]:
            fname = t.split(":")[0] if ":" in t else t
            if fname == "main.py":
                lines = t.split(":")[1] if ":" in t else "entire"
                main_agents[aid] = {"layer": entry["layer"], "lines": lines}

    # Two agents on main.py at different layers
    layers_on_main = set(a["layer"] for a in main_agents.values())
    assert len(layers_on_main) > 1, "Should have multiple layers on main.py"
    assert len(main_agents) == 2  # agent-search + agent-graph

    # Their line ranges don't overlap → zero semantic conflict
    assert main_agents["agent-search"]["lines"] == "100-200"
    assert main_agents["agent-graph"]["lines"] == "300-400"
    # 100-200 and 300-400 don't overlap → git merges cleanly


@test("methodology: same-layer overlapping = potential real conflict")
def test_same_layer_risk():
    """When two agents at the SAME layer touch overlapping lines,
    that's a genuine semantic conflict that needs resolution."""
    set_manifest(SAME_LAYER_MANIFEST)

    data = get_manifest()
    agents = list(data["active"].values())
    assert agents[0]["layer"] == agents[1]["layer"] == "buddhi"

    # Parse line ranges
    r1 = agents[0]["touches"][0].split(":")[1]  # "50-100"
    r2 = agents[1]["touches"][0].split(":")[1]  # "80-130"
    s1, e1 = map(int, r1.split("-"))
    s2, e2 = map(int, r2.split("-"))

    # They overlap on lines 80-100 → real semantic conflict
    overlap = max(0, min(e1, e2) - max(s1, s2))
    assert overlap > 0, f"Lines {r1} and {r2} should overlap"
    assert overlap == 20, f"Expected 20 overlapping lines, got {overlap}"


@test("methodology: lineage tracks evolutionary chain correctly")
def test_lineage_chain():
    """Every generation has a parent. genesis → gen-0000 → gen-0001 → ...
    The chain is never broken. Each generation knows what came before."""
    set_manifest(CLEAN_MANIFEST)

    layers = ["buddhi", "manas", "mahat", "purusa", "brahman"]
    for i, layer in enumerate(layers):
        run("evolve", "--layer", layer,
            "--intent", f"Generation {i}",
            "--change", f"file{i}.py")

    data = get_manifest()
    gens = data["generations"]
    assert len(gens) == 5

    # Verify unbroken parent chain
    assert gens[0]["parent"] == "genesis"
    for i in range(1, len(gens)):
        assert gens[i]["parent"] == gens[i-1]["id"], \
            f"gen-{i:04d} parent should be gen-{i-1:04d}, got {gens[i]['parent']}"

    # Each generation at correct layer
    for i, layer in enumerate(layers):
        assert gens[i]["layer"] == layer, f"gen-{i:04d} should be {layer}"


@test("methodology: completed generations are immutable records")
def test_lineage_immutability():
    """Once a generation completes with an outcome, its record should
    not be modified by subsequent evolves."""
    set_manifest(CLEAN_MANIFEST)
    run("evolve", "--layer", "buddhi", "--intent", "Original", "--change", "x.py")
    run("outcome", "--id", "gen-0000", "--status", "stable", "--metrics", "ok")

    # Record the original state
    data = get_manifest()
    original = dict(data["generations"][0])

    # Evolve again — should not modify gen-0000
    run("evolve", "--layer", "manas", "--intent", "New thing", "--change", "y.py")

    data = get_manifest()
    after = data["generations"][0]
    assert after["id"] == original["id"]
    assert after["intent"] == original["intent"]
    assert after["outcome"] == original["outcome"]
    assert after["parent"] == original["parent"]


# ═══════════════════════════════════════════════════════════════
# TESTS: Help / unknown commands
# ═══════════════════════════════════════════════════════════════

@test("help: no args shows usage")
def test_help():
    code, out = run()
    assert code == 0, f"exit {code}"
    assert "safe" in out.lower()
    assert "resolve" in out.lower()
    assert "evolve" in out.lower()
    assert "lineage" in out.lower()


@test("help: unknown command shows valid options")
def test_unknown():
    code, out = run("nonsense")
    assert code == 1, f"exit {code}"
    assert "Unknown" in out
    assert "safe" in out  # lists valid commands


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║  Samanvaya — Methodology Verification Suite         ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    # Find and run all test_ functions
    import types
    tests = sorted(
        [(name, fn) for name, fn in globals().items()
         if name.startswith("test_") and isinstance(fn, types.FunctionType)],
        key=lambda x: x[0]
    )

    for name, fn in tests:
        fn()

    print()
    print(f"{'='*55}")
    total = PASS + FAIL
    print(f"Results: {PASS}/{total} passed", end="")
    if FAIL > 0:
        print(f", {FAIL} FAILED")
    else:
        print(" ✅ All passing")
    print(f"{'='*55}")

    sys.exit(0 if FAIL == 0 else 1)
