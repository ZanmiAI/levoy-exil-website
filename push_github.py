#!/usr/bin/env python3
"""Push levoy-exil-website updates to GitHub main + gh-pages via the Data API.

main:      full local source (README, site.json, build.py, assets/, public/)
gh-pages:  contents of preview_public/ at the branch root (site preview)

Only uploads blobs whose content actually changed (git blob-sha comparison).
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import (  # noqa: E402
    add_surrogate_to_request,
    read_json_response,
    DynamicCredentialError,
)

CREDENTIAL = "custom.github"
ALLOWED_HOSTS = ["api.github.com"]
API = "https://api.github.com"
OWNER, REPO = "ZanmiAI", "levoy-exil-website"
ROOT = "/home/hatch/workspace/levoy-exil-website"


def api(method, path, payload=None, retries=3):
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(API + path, method=method)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "muse-github-skill/1.0")
        add_surrogate_to_request(req, CREDENTIAL,
                                 entry_name="access_token",
                                 allowed_hosts=ALLOWED_HOSTS)
        data = None
        if payload is not None:
            data = json.dumps(payload).encode()
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, data=data,
                                        timeout=60) as resp:
                return read_json_response(resp)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:2000]
            raise RuntimeError(f"{method} {path} -> {e.code}: {body}")
        except Exception as e:  # transient network drop: retry
            last = e
            import time
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{method} {path} failed after {retries} tries: {last}")


def blob_sha(content: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(content) + content).hexdigest()


def local_files(base: str, prefix: str):
    """Return {repo_path: local_abs_path} for everything under base."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, base).replace(os.sep, "/")
            out[f"{prefix}{rel}" if prefix else rel] = full
    return out


def push_branch(branch: str, mapping: dict, message: str):
    # current ref + commit
    ref = api("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{branch}")
    old_commit = ref["object"]["sha"]
    commit = api("GET", f"/repos/{OWNER}/{REPO}/git/commits/{old_commit}")
    base_tree = commit["tree"]["sha"]
    tree = api("GET", f"/repos/{OWNER}/{REPO}/git/trees/{base_tree}?recursive=1")
    remote = {t["path"]: t["sha"] for t in tree.get("tree", [])
              if t["type"] == "blob"}

    changes = []
    for repo_path, full in mapping.items():
        with open(full, "rb") as f:
            content = f.read()
        if remote.get(repo_path) == blob_sha(content):
            continue  # unchanged, reuse blob from base tree
        blob = api("POST", f"/repos/{OWNER}/{REPO}/git/blobs",
                   {"content": base64.b64encode(content).decode(),
                    "encoding": "base64"})
        changes.append({"path": repo_path, "mode": "100644",
                        "type": "blob", "sha": blob["sha"]})
        if len(changes) % 25 == 0:
            print(f"  {branch}: uploaded {len(changes)} blobs...", flush=True)

    # deletions: remote paths not present locally
    for rp in remote:
        if rp not in mapping:
            changes.append({"path": rp, "mode": "100644",
                            "type": "blob", "sha": None})

    if not changes:
        print(f"  {branch}: nothing changed, skipping")
        return old_commit

    new_tree = api("POST", f"/repos/{OWNER}/{REPO}/git/trees",
                   {"base_tree": base_tree, "tree": changes})
    new_commit = api("POST", f"/repos/{OWNER}/{REPO}/git/commits",
                     {"message": message, "tree": new_tree["sha"],
                      "parents": [old_commit]})
    api("PATCH", f"/repos/{OWNER}/{REPO}/git/refs/heads/{branch}",
        {"sha": new_commit["sha"]})
    print(f"  {branch}: {old_commit[:7]} -> {new_commit['sha'][:7]} "
          f"({len(changes)} paths)")
    return new_commit["sha"]


def main():
    print("Pushing main...", flush=True)
    main_map = {}
    for name in ("README.md", "TEMPLATE-README.md", "TODO.md",
                 "site.json", "build.py"):
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            main_map[name] = p
    main_map.update(local_files(os.path.join(ROOT, "assets"), "assets/"))
    main_map.update(local_files(os.path.join(ROOT, "public"), "public/"))
    main_map.update(local_files(os.path.join(ROOT, "brand"), "brand/"))
    push_branch("main", main_map,
                "Lock official brand blue #0e3c79 + brand record (2026-09-20)")

    print("Pushing gh-pages...", flush=True)
    pages_map = local_files(os.path.join(ROOT, "preview_public"), "")
    push_branch("gh-pages", pages_map,
                "Deploy site with locked brand blue #0e3c79 (2026-09-20)")


if __name__ == "__main__":
    try:
        main()
    except (DynamicCredentialError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
