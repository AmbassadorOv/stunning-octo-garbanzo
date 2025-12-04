#!/usr/bin/env python3
"""
Julius Automation Bundle — GitHub Issues Integration

Single-file orchestration script that performs:
- daily ingest (Hot)
- gate parsing & normalization
- multilayer tensor build (sparse)
- compression policy decision
- kernel simulation stubs (photonic/sonographic/liquid)
- fusion & 3D projection
- GitHub Issues creation/update (replaces Trello)
- promotion pipeline (Hot -> Warm -> Cold) with governance gating
- audit logging and artifact manifest export

USAGE:
  - Set environment variable GITHUB_TOKEN with a personal access token that has repo:issues scope.
  - Fill CONFIG['github']['owner'] and CONFIG['github']['repo'].
  - Run: python3 julius_bundle.py --run
  - For dry-run (no GitHub calls): python3 julius_bundle.py --dry
"""

import os
import sys
import json
import time
import hashlib
import argparse
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

# Optional numeric libs
try:
    import numpy as np
    from scipy import sparse
except Exception:
    np = None
    sparse = None

#----------------------------
#
# CONFIGURATION (fill values)
#
#----------------------------
CONFIG = {
    "data_dir": "./data",
    "hotretentionseconds": 24 * 3600,
    "warmretentiondays": 30,
    "colddir": "./data/coldarchive",
    "github": {
        "enabled": True,
        "owner": "<GITHUB_OWNER>",   # <-- fill: username or org
        "repo": "<GITHUB_REPO>"      # <-- fill: repository name
    },
    "compression": {
        "vsa_dim": 1024,
        "tensortrainrank": 16,
        "growththresholdbits": 2.0
    },
    "governance": {
        "humanreviewrisk_tier": 2
    },
    "logging": {
        "level": "INFO"
    }
}

#----------------------------
#
# Logging
#
#----------------------------
logging.basicConfig(
    level=getattr(logging, CONFIG["logging"]["level"]),
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger("julius_bundle")

#----------------------------
#
# Utilities
#
#----------------------------
def ensure_dirs():
    os.makedirs(CONFIG["data_dir"], exist_ok=True)
    os.makedirs(CONFIG["colddir"], exist_ok=True)

def sha256ofbytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256oftext(s: str) -> str:
    return sha256ofbytes(s.encode("utf-8"))

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

#----------------------------
#
# Ingest (Hot)
#
#----------------------------
def ingest_sources(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    manifest = {
        "artifactid": f"artifact://gate/hotbatch::{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        "ingestdate": now_iso(),
        "items": []
    }
    for s in sources:
        content = s.get("content", "")
        snippet = content[:400]
        item = {
            "source_id": s.get("id"),
            "source_type": s.get("type", "text"),
            "source_url": s.get("url"),
            "ingestdate": now_iso(),
            "provenance_snippet": snippet,
            "raw": content,
            "confidence": 0.5
        }
        item_bytes = json.dumps(item, sort_keys=True).encode("utf-8")
        item["sha256"] = sha256ofbytes(item_bytes)
        manifest["items"].append(item)
    manifest_bytes = json.dumps(manifest, indent=2).encode("utf-8")
    manifest["sha256"] = sha256ofbytes(manifest_bytes)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(CONFIG["data_dir"], f"hotmanifest_{ts}.json")
    with open(path, "wb") as f:
        f.write(manifest_bytes)
    logger.info("Ingested %d sources into %s", len(sources), path)
    return manifest

#----------------------------
#
# Gate Parser & Variable Extractor
#
#----------------------------
def parsegatesfrom_manifest(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    gates = []
    for item in manifest.get("items", []):
        text = item.get("raw", "")
        tokens = [t for t in text.replace("\n", " ").split(" ") if t]
        candidates = []
        for t in tokens:
            if len(t) == 3 and t.isalpha():
                candidates.append(t)
        if not candidates:
            for i in range(len(text) - 2):
                sub = text[i:i+3]
                if sub.isalpha():
                    candidates.append(sub)
                    break
        for idx, cand in enumerate(candidates[:10]):
            gate = {
                "gateid": f"{item['source_id']}GATE{idx+1}",
                "symbolic_label": cand,
                "crystallographic_label": None,
                "layer_index": None,
                "type": "unknown",
                "parameters": {},
                "relations": [],
                "confidence": round(0.6 + 0.1 * min(idx, 3), 2),
                "provenance": {"source": item.get("source_id"), "snippet": item.get("provenance_snippet")}
            }
            gates.append(gate)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(CONFIG["data_dir"], f"gatesparsed_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(gates, f, indent=2)
    logger.info("Parsed %d gates into %s", len(gates), path)
    return gates

#----------------------------
#
# Multilayer Tensor Builder
#
#----------------------------
def buildmultilayer_tensor(gates: List[Dict[str, Any]], num_layers: int = 15):
    N = len(gates)
    L = num_layers
    if N == 0:
        logger.warning("No gates to build tensor from")
        return None
    layers = []
    for ell in range(L):
        density = 0.01 + 0.005 * (ell % 3)
        mat = sparse.random(N, N, density=density, format="coo", data_rvs=np.random.rand) if sparse else None
        layers.append(mat)
    if sparse:
        blocks = []
        for ell, mat in enumerate(layers):
            blocks.append(mat.tocsr())
        S = sparse.block_diag(blocks, format="csr")
        coupling_strength = 0.02
        for i in range(L-1):
            rows = np.arange(N) + i*N
            cols = np.arange(N) + (i+1)*N
            data = np.full(N, coupling_strength)
            S[rows, cols] = data
            S[cols, rows] = data
    else:
        S = None
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    s_path = os.path.join(CONFIG["data_dir"], f"supraS_{ts}.npz")
    if sparse and S is not None:
        sparse.save_npz(s_path, S)
        logger.info("Saved supra-adjacency to %s", s_path)
    meta = {"N": N, "L": L, "supra_path": s_path if S is not None else None}
    return meta

#----------------------------
#
# Growth Estimator & Compression Policy
#
#----------------------------
def estimate_growth_rate(previous_count: int, current_count: int, steps: int = 1) -> float:
    if previous_count <= 0:
        return float("inf")
    return (np.log2(current_count) - np.log2(previous_count)) / max(1, steps)

def choose_compression_policy(growth_rate_bits: float) -> Dict[str, Any]:
    cfg = CONFIG["compression"]
    if growth_rate_bits == float("inf") or growth_rate_bits > cfg["growththresholdbits"]:
        return {"method": "VSA", "dim": cfg["vsa_dim"]}
    elif growth_rate_bits > cfg["growththresholdbits"] / 2:
        return {"method": "tensortrain", "rank": cfg["tensortrainrank"]}
    else:
        return {"method": "none"}

#----------------------------
#
# Kernel Simulation Stubs
#
#----------------------------
def photonic_unitary_apply(U_matrix, input_vector):
    if np is None:
        return input_vector
    return U_matrix.dot(input_vector)

def sonographic_modal_decompose(raw_samples, num_modes: int = 8):
    if np is None:
        return [0.0] * num_modes
    coeffs = np.fft.rfft(raw_samples)[:num_modes]
    return np.abs(coeffs)

def liquid_reservoir_states(inputs, reservoir_size: int = 128):
    if np is None:
        return [0.0] * reservoir_size
    W = np.random.randn(reservoir_size, inputs.shape[0]) * 0.1
    states = np.tanh(W.dot(inputs))
    return states

#----------------------------
#
# Fusion & Projection
#
#----------------------------
def fuse_and_project(v_photonic, v_sonographic, v_liquid, w_msc: float = 1.0):
    if np is None:
        coords = [0.0, 0.0, 0.0]
    else:
        vec = np.concatenate([np.asarray(v_photonic).flatten(), np.asarray(v_sonographic).flatten(), np.asarray(v_liquid).flatten()])
        rng = np.random.RandomState(42)
        proj = rng.randn(3, vec.size).dot(vec)
        coords = (proj / (np.linalg.norm(proj) + 1e-9)) * (1.0 + 0.1 * w_msc)
    geometry = {
        "vertices": [{"x": float(coords[0]), "y": float(coords[1]), "z": float(coords[2])}],
        "meta": {"w_msc": w_msc, "timestamp": now_iso()}
    }
    return geometry

#----------------------------
#
# GitHub Integration
#
#----------------------------
import requests

def get_github_token() -> str:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable not set. Create a PAT with repo:issues scope and set GITHUB_TOKEN.")
    return token

def github_create_issue(title: str, body: str, labels: List[str] = None, assignees: List[str] = None, dry_run: bool = False) -> Dict[str, Any]:
    """
    Create a GitHub issue in the configured repository.
    Returns the JSON response from GitHub (issue object) or a mock dict in dry_run.
    """
    if dry_run or not CONFIG["github"]["enabled"]:
        logger.info("Dry-run: would create GitHub issue: %s", title)
        return {"mock": True, "title": title, "body": body, "labels": labels or [], "assignees": assignees or []}

    token = get_github_token()
    owner = CONFIG["github"]["owner"]
    repo = CONFIG["github"]["repo"]
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    payload = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    if assignees:
        payload["assignees"] = assignees
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        logger.error("GitHub issue creation failed: %s %s", resp.status_code, resp.text)
        resp.raise_for_status()
    logger.info("Created GitHub issue: %s", resp.json().get("html_url"))
    return resp.json()

def github_add_comment(issue_number: int, comment_body: str, dry_run: bool = False) -> Dict[str, Any]:
    if dry_run or not CONFIG["github"]["enabled"]:
        logger.info("Dry-run: would add comment to issue #%s", issue_number)
        return {"mock": True, "issue_number": issue_number, "comment": comment_body}
    token = get_github_token()
    owner = CONFIG["github"]["owner"]
    repo = CONFIG["github"]["repo"]
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    payload = {"body": comment_body}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        logger.error("GitHub comment failed: %s %s", resp.status_code, resp.text)
        resp.raise_for_status()
    logger.info("Added comment to issue #%s", issue_number)
    return resp.json()

#----------------------------
#
# Promotion Pipeline & Governance
#
#----------------------------
def promote_artifact(manifest: Dict[str, Any], target_tier: str) -> Dict[str, Any]:
    risk_tier = manifest.get("governance", {}).get("risktier", 0)
    if target_tier == "cold" and risk_tier >= CONFIG["governance"]["humanreviewrisk_tier"]:
        manifest["publish_blocked"] = True
        manifest["publish_block_reason"] = f"Requires human review for risk_tier >= {CONFIG['governance']['humanreviewrisk_tier']}"
        logger.warning("Promotion blocked: %s", manifest["publish_block_reason"])
        return manifest
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{manifest.get('artifactid','artifact')}_v{ts}.json".replace("://", "_").replace("/", "_")
    path = os.path.join(CONFIG["colddir"], filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    manifest["promoted_to"] = target_tier
    manifest["promoted_at"] = now_iso()
    manifest["cold_path"] = path
    logger.info("Promoted artifact to %s: %s", target_tier, path)
    return manifest

#----------------------------
#
# Audit Logging
#
#----------------------------
def write_audit(entry: Dict[str, Any]):
    ts = datetime.utcnow().strftime("%Y%m%d")
    path = os.path.join(CONFIG["data_dir"], f"audit_{ts}.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    logger.info("Audit logged: %s", entry.get("action"))

#----------------------------
#
# High-level Orchestration
#
#----------------------------
def run_pipeline(sources: List[Dict[str, Any]], dry_run: bool = False):
    ensure_dirs()
    manifest = ingest_sources(sources)
    write_audit({"action": "ingest", "artifactid": manifest["artifactid"], "time": now_iso(), "items": len(manifest["items"])})
    gates = parsegatesfrom_manifest(manifest)
    write_audit({"action": "parsegates", "count": len(gates), "time": now_iso()})
    tensor_meta = buildmultilayer_tensor(gates)
    write_audit({"action": "buildtensor", "meta": tensor_meta, "time": now_iso()})
    prev_count = 0
    curr_count = len(gates)
    growth_bits = estimate_growth_rate(prev_count, curr_count)
    policy = choose_compression_policy(growth_bits)
    logger.info("Compression policy chosen: %s", policy)
    write_audit({"action": "compressionpolicy", "policy": policy, "time": now_iso()})
    if np is None:
        photonic_out = [0.0, 0.0, 0.0]
        sonographic_out = [0.0] * 8
        liquid_out = [0.0] * 16
    else:
        U = np.eye(3)
        inp = np.array([1.0, 1.0, 1.0])
        photonic_out = photonic_unitary_apply(U, inp)
        sonographic_raw = np.sin(np.linspace(0, 2*np.pi, 256))
        sonographic_out = sonographic_modal_decompose(sonographic_raw)
        liquid_in = np.array([0.1, 0.2, 0.3])
        liquid_out = liquid_reservoir_states(liquid_in)
    geometry = fuse_and_project(np.array(photonic_out), np.array(sonographic_out), np.array(liquid_out), w_msc=7.712)
    geom_path = os.path.join(CONFIG["data_dir"], f"geometry_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json")
    with open(geom_path, "w", encoding="utf-8") as f:
        json.dump(geometry, f, indent=2)
    logger.info("Fusion geometry written to %s", geom_path)
    write_audit({"action": "fusion", "geometry_path": geom_path, "time": now_iso()})
    # Create GitHub issue summarizing the run
    issue_title = f"Automated ingest run {datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    issue_body = (
        f"Automated ingest run\n\n"
        f"- Ingested sources: {len(sources)}\n"
        f"- Parsed gates: {len(gates)}\n"
        f"- Tensor meta: {json.dumps(tensor_meta)}\n"
        f"- Compression policy: {json.dumps(policy)}\n"
        f"- Geometry artifact: {geom_path}\n\n"
        "### Quick checklist\n"
        "- [ ] Ingested\n"
        "- [ ] Parsed\n"
        "- [ ] Tensor built\n"
        "- [ ] Compression applied\n"
        "- [ ] Fusion geometry attached\n"
        "- [ ] Promote to Warm/Cold\n\n"
        "### Notes\n"
        "This issue was created by the Julius automation bundle. Attach artifacts or add comments with links to stored files."
    )
    gh_resp = github_create_issue(issue_title, issue_body, labels=["automation", "ingest"], assignees=[CONFIG["github"].get("owner")], dry_run=dry_run)
    write_audit({"action": "github_issue_create", "response": {"title": gh_resp.get("title"), "url": gh_resp.get("html_url", gh_resp.get("mock_url", None))}, "time": now_iso()})
    manifest_entry = {
        "artifactid": manifest["artifactid"],
        "gates_count": len(gates),
        "tensormeta": tensor_meta,
        "compression_policy": policy,
        "geometry": geom_path,
        "governance": {"risktier": 1, "explainabilityscore": 0.9},
        "ingestedat": manifest["ingestdate"]
    }
    promoted = promote_artifact(manifest_entry, target_tier="cold")
    write_audit({"action": "promote", "artifactid": manifest_entry["artifactid"], "result": promoted.get("promoted_to", "blocked"), "time": now_iso()})
    logger.info("Pipeline run complete. Manifest: %s", manifest_entry["artifactid"])
    return manifest_entry

#----------------------------
#
# CLI & Demo sources
#
#----------------------------
def sample_sources_for_demo():
    return [
        {"id": "src_001", "type": "text", "content": "C4DPP snippet: three-letter triplet CHE, elements fire water air. W axis mapping."},
        {"id": "src_002", "type": "text", "content": "Photonic kernel notes: MZI mesh, phase encoding, VSA binding examples."}
    ]

def main():
    parser = argparse.ArgumentParser(description="Julius single-bundle automation runner (GitHub Issues integration)")
    parser.addargument("--run", action="store_true", help="Run full pipeline")
    parser.addargument("--dry", action="store_true", help="Dry run (no GitHub API calls)")
    args = parser.parse_args()
    if args.dry:
        CONFIG["github"]["enabled"] = False
    if args.run or args.dry:
        sources = sample_sources_for_demo()
        manifest = run_pipeline(sources, dry_run=args.dry)
        print(json.dumps(manifest, indent=2))
    else:
        print("No action specified. Use --run to execute pipeline or --dry for dry run.")

if __name__ == "__main__":
    main()
