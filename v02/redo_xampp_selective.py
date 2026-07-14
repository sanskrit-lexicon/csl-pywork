#!/usr/bin/env python3
"""Python 3 driver for the selective XAMPP refresh (csl-pywork#53).

Ports redo_xampp_selective.sh to a parameterized, dry-run-capable, manifest-
producing driver, per docs/REFRESH_SCRIPT_MODERNIZATION_PLAN.md in
csl-observatory. Backward-compatible: redo_xampp_selective.sh still works as
a thin wrapper that calls this driver with the production server defaults.

Usage:
    python3 v02/redo_xampp_selective.py --dry-run
    python3 v02/redo_xampp_selective.py \
        --base /var/www/html/cologne --indic-base /var/www/html/indic-dict \
        --state-file csl-orig/v02/.xampp_last_run --manifest refresh-manifest.json

Prerequisites: sibling dirs csl-orig, csl-websanlexicon, csl-homepage,
hwnorm1, csl-json, cologne-stardict must exist under --base, and
stardict-sanskrit under --indic-base. See readme_selective.md.

Server rehearsal note: preflight/pull/diff/generate/stardict/json/homepage
phase bodies are implemented per the modernization plan's Phase Design table,
but a live dry-run and --no-push rehearsal against the real Cologne server
layout (plan steps 7-8) require Cologne server access (DECISIONS_NEEDED.md
C2), which is not yet granted — do not enable push-capable runs before that
rehearsal and explicit maintainer/server confirmation (plan step 9).
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

PHASES = [
    "preflight",
    "pull",
    "diff",
    "generate",
    "stardict",
    "stardict_sync",
    "json",
    "homepage",
    "state_update",
]

# Repos that must exist under --base (sibling directories of csl-pywork).
REQUIRED_REPOS = [
    "csl-orig",
    "csl-websanlexicon",
    "csl-homepage",
    "hwnorm1",
    "csl-json",
    "cologne-stardict",
]


class DriverError(Exception):
    """A phase failed; stop without advancing state."""


def log(msg):
    # Progress goes to stderr so stdout stays pure JSON (the manifest, when
    # --manifest isn't given) for scripting/tests to parse.
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def run(cmd, cwd=None, dry_run=False, check=True):
    """Run a shell command, honoring --dry-run (print, don't execute)."""
    printable = cmd if isinstance(cmd, str) else " ".join(cmd)
    if dry_run:
        log(f"DRY-RUN would run: {printable} (cwd={cwd or '.'})")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
    try:
        result = subprocess.run(
            cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True
        )
    except OSError as e:
        # e.g. cwd doesn't exist, or the interpreter/script named in cmd is
        # missing — a real precondition failure, not a Python crash.
        raise DriverError(f"could not run: {printable} (cwd={cwd or '.'}): {e}")
    if check and result.returncode != 0:
        raise DriverError(
            f"command failed ({result.returncode}): {printable}\n{result.stderr}"
        )
    return result


def git_output(args, cwd, dry_run_safe=True):
    """Run a read-only git command and return stripped stdout. Always runs,
    even under --dry-run, since read-only git calls are safe to preview with."""
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise DriverError(f"git {' '.join(args)} failed in {cwd}: {result.stderr}")
    return result.stdout.strip()


def is_worktree_clean(repo_dir):
    status = git_output(["status", "--porcelain"], repo_dir)
    return status == ""


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", default=os.environ.get("CSL_BASE", "/var/www/html/cologne"),
                    help="Parent directory for csl-orig, csl-pywork, csl-homepage, "
                         "csl-websanlexicon, hwnorm1, csl-json, cologne-stardict.")
    p.add_argument("--indic-base", default=os.environ.get("CSL_INDIC_BASE", "/var/www/html/indic-dict"),
                    help="Parent directory for stardict-sanskrit.")
    p.add_argument("--state-file", default=None,
                    help="Last-successful csl-orig commit marker "
                         "(default: <base>/csl-orig/v02/.xampp_last_run).")
    p.add_argument("--since", default=None,
                    help="Override the state file for one manual run (a csl-orig commit-ish).")
    p.add_argument("--dict", dest="dicts", action="append", default=None,
                    help="Limit the run to one or more dictionary codes after diff detection "
                         "(repeatable).")
    p.add_argument("--dry-run", action="store_true",
                    help="Print phases, commands, repos, and commits without writing or pushing.")
    p.add_argument("--no-push", action="store_true",
                    help="Commit locally where needed but skip pushes.")
    p.add_argument("--skip-pull", action="store_true",
                    help="Use current local checkout state for offline tests.")
    p.add_argument("--strict-clean", action="store_true",
                    help="Fail if any participating repo has uncommitted changes.")
    p.add_argument("--allow-dirty", action="append", default=[],
                    help="Permit a known-dirty repo during manual testing (repeatable).")
    p.add_argument("--stop-after", choices=PHASES, default=None,
                    help="Stop after the named phase.")
    p.add_argument("--manifest", default=None,
                    help="Write a machine-readable run summary to this path.")
    return p.parse_args(argv)


def repo_path(base, name):
    return os.path.join(base, name)


def phase_preflight(ctx):
    log("PHASE preflight")
    missing = [r for r in REQUIRED_REPOS if not os.path.isdir(repo_path(ctx["base"], r))]
    if missing:
        raise DriverError(f"missing required repo(s) under --base {ctx['base']}: {missing}")
    if not os.path.isdir(os.path.join(ctx["indic_base"], "stardict-sanskrit")):
        raise DriverError(f"missing stardict-sanskrit under --indic-base {ctx['indic_base']}")
    if ctx["since"] is None and not os.path.isfile(ctx["state_file"]):
        raise DriverError(
            f"no --since given and state file does not exist: {ctx['state_file']} "
            "(first run needs an explicit --since)"
        )
    if ctx["strict_clean"]:
        dirty = []
        for r in REQUIRED_REPOS:
            if r in ctx["allow_dirty"]:
                continue
            rp = repo_path(ctx["base"], r)
            if os.path.isdir(rp) and not is_worktree_clean(rp):
                dirty.append(r)
        if dirty:
            raise DriverError(f"--strict-clean: dirty repo(s), not in --allow-dirty: {dirty}")
    ctx["manifest"]["phases_run"].append("preflight")


def phase_pull(ctx):
    log("PHASE pull")
    if ctx["skip_pull"]:
        log("--skip-pull: using current local checkout state")
        ctx["manifest"]["phases_run"].append("pull(skipped)")
        return
    pull_repos = ["csl-pywork", *REQUIRED_REPOS]
    for r in pull_repos:
        rp = repo_path(ctx["base"], r)
        if not os.path.isdir(rp):
            continue
        run(["git", "pull", "origin"], cwd=rp, dry_run=ctx["dry_run"])
    ctx["manifest"]["phases_run"].append("pull")


def phase_diff(ctx):
    log("PHASE diff")
    orig_dir = repo_path(ctx["base"], "csl-orig")
    since = ctx["since"] or open(ctx["state_file"], encoding="utf-8").read().strip()
    head = git_output(["rev-parse", "HEAD"], orig_dir)
    ctx["manifest"]["old_commit"] = since
    ctx["manifest"]["new_commit"] = head

    # Validate --dict codes unconditionally (invalid codes must fail even when
    # the diff itself is empty — an operator typo shouldn't silently no-op).
    valid_dicts = {
        name for name in os.listdir(os.path.join(orig_dir, "v02"))
        if not name.startswith(".") and os.path.isdir(os.path.join(orig_dir, "v02", name))
    }
    if ctx["dicts"]:
        invalid = set(ctx["dicts"]) - valid_dicts
        if invalid:
            raise DriverError(f"--dict named unknown dictionary code(s): {sorted(invalid)}")

    if since == head:
        log("diff: state already at HEAD, nothing changed")
        ctx["changed_dicts"] = []
        ctx["manifest"]["phases_run"].append("diff")
        return

    changed_files = git_output(["diff", "--name-only", f"{since}..{head}"], orig_dir).splitlines()
    candidates = set()
    for f in changed_files:
        base_name = os.path.basename(f)
        if base_name.endswith(".txt"):
            candidates.add(base_name[: -len(".txt")])
    changed = sorted(candidates & valid_dicts)

    if ctx["dicts"]:
        requested = set(ctx["dicts"])
        changed = sorted(requested & set(changed)) if changed else sorted(requested)

    ctx["changed_dicts"] = changed
    ctx["manifest"]["dictionaries"] = changed
    log(f"diff: {len(changed)} dictionary(ies) to handle: {changed}")
    ctx["manifest"]["phases_run"].append("diff")


def phase_generate(ctx):
    log("PHASE generate")
    if not ctx["changed_dicts"]:
        log("generate: empty diff, nothing to generate")
        ctx["manifest"]["phases_run"].append("generate(empty)")
        return
    pywork_v02 = os.path.join(ctx["base"], "csl-pywork", "v02")
    for d in ctx["changed_dicts"]:
        run(["sh", "generate_dict.sh", d, f"../../{d}"], cwd=pywork_v02, dry_run=ctx["dry_run"])
    ctx["manifest"]["phases_run"].append("generate")


def phase_stardict(ctx):
    log("PHASE stardict")
    if not ctx["changed_dicts"]:
        ctx["manifest"]["phases_run"].append("stardict(empty)")
        return
    stardict_dir = repo_path(ctx["base"], "cologne-stardict")
    hwnorm1_src = os.path.join(ctx["base"], "hwnorm1", "sanhw1", "hwnorm1c.txt")
    hwnorm1_dst = os.path.join(stardict_dir, "input", "hwnorm1c.txt")
    if ctx["dry_run"]:
        log(f"DRY-RUN would copy: {hwnorm1_src} -> {hwnorm1_dst}")
    else:
        try:
            shutil.copyfile(hwnorm1_src, hwnorm1_dst)
        except OSError as e:
            raise DriverError(f"could not refresh hwnorm1c.txt before Stardict generation: {e}")
    dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    for d in ctx["changed_dicts"]:
        run(["python3", "make_babylon.py", d, "0"], cwd=stardict_dir, dry_run=ctx["dry_run"])
        run(["python3", "make_babylon.py", d, "1"], cwd=stardict_dir, dry_run=ctx["dry_run"])
        run(["git", "add", "output/", "production/"], cwd=stardict_dir, dry_run=ctx["dry_run"])
        run(["git", "commit", "-m", f"{d} update {dt}"], cwd=stardict_dir, dry_run=ctx["dry_run"], check=False)
        ctx["manifest"].setdefault("changed_repos", []).append("cologne-stardict")
    if not ctx["no_push"] and not ctx["dry_run"]:
        run(["git", "push"], cwd=stardict_dir, dry_run=ctx["dry_run"])
        ctx["manifest"].setdefault("pushed_repos", []).append("cologne-stardict")
    else:
        log("stardict: --no-push or --dry-run, skipping push")
    ctx["manifest"]["phases_run"].append("stardict")


def phase_stardict_sync(ctx):
    log("PHASE stardict_sync")
    if not ctx["changed_dicts"]:
        ctx["manifest"]["phases_run"].append("stardict_sync(empty)")
        return
    indic_dir = os.path.join(ctx["indic_base"], "stardict-sanskrit")
    stardict_dir = repo_path(ctx["base"], "cologne-stardict")
    if not ctx["skip_pull"]:
        run(["git", "pull", "origin"], cwd=indic_dir, dry_run=ctx["dry_run"])
    run(["bash", "move_to_stardict.sh"], cwd=stardict_dir, dry_run=ctx["dry_run"])
    dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    run(["git", "add", "."], cwd=indic_dir, dry_run=ctx["dry_run"])
    run(["git", "commit", "-m", f"update {dt}"], cwd=indic_dir, dry_run=ctx["dry_run"], check=False)
    ctx["manifest"].setdefault("changed_repos", []).append("stardict-sanskrit")
    if not ctx["no_push"] and not ctx["dry_run"]:
        run(["git", "push", "origin"], cwd=indic_dir, dry_run=ctx["dry_run"])
        ctx["manifest"].setdefault("pushed_repos", []).append("stardict-sanskrit")
    ctx["manifest"]["phases_run"].append("stardict_sync")


def phase_json(ctx):
    log("PHASE json")
    if not ctx["changed_dicts"]:
        ctx["manifest"]["phases_run"].append("json(empty)")
        return
    json_dir = repo_path(ctx["base"], "csl-json")
    dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    for d in ctx["changed_dicts"]:
        run(["python3", "json_from_babylon.py", d], cwd=json_dir, dry_run=ctx["dry_run"])
        run(["git", "add", "ashtadhyayi.com/"], cwd=json_dir, dry_run=ctx["dry_run"])
        run(["git", "commit", "-m", f"{d} update {dt}"], cwd=json_dir, dry_run=ctx["dry_run"], check=False)
        ctx["manifest"].setdefault("changed_repos", []).append("csl-json")
    if not ctx["no_push"] and not ctx["dry_run"]:
        run(["git", "push"], cwd=json_dir, dry_run=ctx["dry_run"])
        ctx["manifest"].setdefault("pushed_repos", []).append("csl-json")
    ctx["manifest"]["phases_run"].append("json")


def phase_homepage(ctx):
    log("PHASE homepage")
    homepage_dir = repo_path(ctx["base"], "csl-homepage")
    run(["bash", "redo_xampp.sh"], cwd=homepage_dir, dry_run=ctx["dry_run"])
    ctx["manifest"]["phases_run"].append("homepage")


def phase_state_update(ctx):
    log("PHASE state_update")
    if ctx["dry_run"]:
        log(f"DRY-RUN would advance {ctx['state_file']} to {ctx['manifest']['new_commit']}")
        ctx["manifest"]["phases_run"].append("state_update(dry-run)")
        return
    with open(ctx["state_file"], "w", encoding="utf-8") as f:
        f.write(ctx["manifest"]["new_commit"] + "\n")
    orig_dir = repo_path(ctx["base"], "csl-orig")
    commit_count = git_output(["log", "--oneline"], orig_dir).count("\n") + 1
    version_path = os.path.join(orig_dir, ".version")
    with open(version_path, "w", encoding="utf-8") as f:
        f.write(f"2.0.{commit_count}\n")
    ctx["manifest"]["phases_run"].append("state_update")


PHASE_FUNCS = {
    "preflight": phase_preflight,
    "pull": phase_pull,
    "diff": phase_diff,
    "generate": phase_generate,
    "stardict": phase_stardict,
    "stardict_sync": phase_stardict_sync,
    "json": phase_json,
    "homepage": phase_homepage,
    "state_update": phase_state_update,
}


def main(argv=None):
    args = parse_args(argv)
    base = os.path.abspath(args.base)
    indic_base = os.path.abspath(args.indic_base)
    state_file = args.state_file or os.path.join(base, "csl-orig", "v02", ".xampp_last_run")

    ctx = {
        "base": base,
        "indic_base": indic_base,
        "state_file": state_file,
        "since": args.since,
        "dicts": args.dicts,
        "dry_run": args.dry_run,
        "no_push": args.no_push or args.dry_run,
        "skip_pull": args.skip_pull,
        "strict_clean": args.strict_clean,
        "allow_dirty": set(args.allow_dirty),
        "changed_dicts": [],
        "manifest": {
            "started_at": datetime.datetime.now().isoformat(),
            "dry_run": args.dry_run,
            "no_push": args.no_push or args.dry_run,
            "phases_run": [],
            "dictionaries": [],
            "changed_repos": [],
            "pushed_repos": [],
            "failures": [],
        },
    }

    stop_after = args.stop_after
    failed = False
    for phase in PHASES:
        try:
            PHASE_FUNCS[phase](ctx)
        except DriverError as e:
            log(f"FAILED at phase {phase}: {e}")
            ctx["manifest"]["failures"].append({"phase": phase, "error": str(e)})
            failed = True
            break
        if stop_after == phase:
            log(f"--stop-after {phase}: stopping")
            break

    ctx["manifest"]["ended_at"] = datetime.datetime.now().isoformat()
    ctx["manifest"]["ok"] = not failed

    if args.manifest:
        with open(args.manifest, "w", encoding="utf-8") as f:
            json.dump(ctx["manifest"], f, indent=2)
        log(f"manifest written: {args.manifest}")
    else:
        print(json.dumps(ctx["manifest"], indent=2))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
