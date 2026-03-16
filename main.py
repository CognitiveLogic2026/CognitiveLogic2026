from fastapi import FastAPI, Header, HTTPException
import json
import os

# ============================================================

# Cognitive Logic — QEN API

# Versione: 2.0 (JSON-based, no Neo4j)

# ============================================================

app = FastAPI(
title=“Cognitive Logic QEN API”,
description=“Quantum Ethics Network — AI Governance Framework”,
version=“2.0”
)

GRAPH_PATH = “/root/qen_graph.json”
API_KEY = os.getenv(“API_KEY”, “CL2026”)

def load_graph():
“”“Carica il grafo QEN dal file JSON”””
try:
with open(GRAPH_PATH, “r”) as f:
return json.load(f)
except FileNotFoundError:
return None
except json.JSONDecodeError as e:
return None

# ============================================================

# ROOT

# ============================================================

@app.get(”/”)
async def root():
graph = load_graph()
if graph:
return {
“message”: “CognitiveLogic Validator Active”,
“framework”: graph[“meta”][“name”],
“version”: graph[“meta”][“version”],
“status”: “operational”
}
return {
“message”: “CognitiveLogic Validator Active”,
“status”: “graph not loaded”
}

# ============================================================

# HEALTH CHECK

# ============================================================

@app.get(”/health”)
async def health_check():
graph = load_graph()
if graph is None:
return {“status”: “unhealthy”, “error”: “qen_graph.json not found”}

```
nodes_count = sum(
    len(v) if isinstance(v, list) else 1
    for v in graph["nodes"].values()
)
edges_count = len(graph.get("edges", []))

return {
    "status": "healthy",
    "graph": graph["meta"]["name"],
    "nodes": nodes_count,
    "edges": edges_count,
    "source": GRAPH_PATH
}
```

# ============================================================

# VALIDATE — Trust Anchor check

# ============================================================

@app.post(”/validate”)
async def validate_node(payload: dict, x_api_key: str = Header(None)):
if x_api_key != API_KEY:
raise HTTPException(status_code=403, detail=“Invalid API Key”)

```
graph = load_graph()
if graph is None:
    raise HTTPException(status_code=500, detail="Graph not available")

identity_node = payload.get("identity_node")
if not identity_node:
    raise HTTPException(status_code=400, detail="Manca identity_node nel payload")

# Cerca il nodo nel grafo
found_node = None
found_section = None
for section, items in graph["nodes"].items():
    if isinstance(items, list):
        for item in items:
            if item.get("id") == identity_node or item.get("name") == identity_node:
                found_node = item
                found_section = section
                break
    elif isinstance(items, dict):
        if items.get("id") == identity_node or items.get("name") == identity_node:
            found_node = items
            found_section = section

if not found_node:
    return {
        "status": "not_found",
        "identity_node": identity_node,
        "message": "Nodo non trovato nel grafo QEN"
    }

# Verifica trust anchor
is_trust_anchor = found_node.get("trustAnchor", False)

# Trova relazioni del nodo
edges = graph.get("edges", [])
node_edges = [
    e for e in edges
    if e.get("from") == found_node.get("id") or e.get("to") == found_node.get("id")
]

return {
    "status": "success",
    "identity_node": identity_node,
    "node": found_node,
    "section": found_section,
    "trust_anchor": is_trust_anchor,
    "relations": node_edges,
    "relations_count": len(node_edges)
}
```

# ============================================================

# GRAPH — Lettura grafo completo o per sezione

# ============================================================

@app.get(”/graph”)
async def get_graph(section: str = None, x_api_key: str = Header(None)):
if x_api_key != API_KEY:
raise HTTPException(status_code=403, detail=“Invalid API Key”)

```
graph = load_graph()
if graph is None:
    raise HTTPException(status_code=500, detail="Graph not available")

if section:
    if section not in graph["nodes"]:
        raise HTTPException(status_code=404, detail=f"Sezione '{section}' non trovata")
    return {
        "section": section,
        "data": graph["nodes"][section]
    }

return {
    "meta": graph["meta"],
    "sections": list(graph["nodes"].keys()),
    "nodes_count": sum(
        len(v) if isinstance(v, list) else 1
        for v in graph["nodes"].values()
    ),
    "edges_count": len(graph.get("edges", []))
}
```

# ============================================================

# TRUST ANCHORS — I 4 principi fondanti

# ============================================================

@app.get(”/trust-anchors”)
async def get_trust_anchors():
graph = load_graph()
if graph is None:
raise HTTPException(status_code=500, detail=“Graph not available”)

```
anchors = graph["nodes"].get("trust_anchors", [])
return {
    "trust_anchors": anchors,
    "count": len(anchors)
}
```

# ============================================================

# ALGORITHMS — Lista algoritmi con ethics score

# ============================================================

@app.get(”/algorithms”)
async def get_algorithms():
graph = load_graph()
if graph is None:
raise HTTPException(status_code=500, detail=“Graph not available”)

```
algorithms = graph["nodes"].get("algorithms", [])
return {
    "algorithms": algorithms,
    "count": len(algorithms)
}
```
