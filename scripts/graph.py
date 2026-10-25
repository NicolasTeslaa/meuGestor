"""Read, validate and query the versioned traffic-management graph."""

import argparse
import json
from datetime import date
from pathlib import Path


def load_graph(root):
    root = Path(root)
    with (root / "knowledge" / "graph.json").open(encoding="utf-8") as handle:
        graph = json.load(handle)
    with (root / "knowledge" / "sources.json").open(encoding="utf-8") as handle:
        sources = json.load(handle)
    return graph, sources


def validate(graph, sources):
    errors = []
    node_ids = set()
    source_ids = set()

    for source in sources.get("sources", []):
        source_id = source.get("id", "<missing>")
        if source_id in source_ids:
            errors.append("duplicate source id " + source_id)
        source_ids.add(source_id)
        if not source.get("title"):
            errors.append("source " + source_id + " requires title")
        if not source.get("url", "").startswith("https://"):
            errors.append("source " + source_id + " requires HTTPS URL")
        try:
            date.fromisoformat(source.get("verified_at", ""))
        except ValueError:
            errors.append("source " + source_id + " has invalid verified_at")
        if source.get("kind") not in {"official", "research"}:
            errors.append("source " + source_id + " requires official or research kind")

    for node in graph.get("nodes", []):
        node_id = node.get("id", "<missing>")
        if node_id in node_ids:
            errors.append("duplicate node id " + node_id)
        node_ids.add(node_id)
        for field in ("type", "title", "summary", "applies_to"):
            if not node.get(field):
                errors.append("node " + node_id + " requires " + field)
        if "sources" not in node or not isinstance(node["sources"], list):
            errors.append("node " + node_id + " requires sources list")
        elif not node["sources"]:
            errors.append("node " + node_id + " requires at least one source")
        for source_id in node.get("sources", []):
            if source_id not in source_ids:
                errors.append("node " + node_id + " references absent source " + source_id)
        if node.get("type") == "formula":
            for field in ("numerator", "denominator", "unit", "period"):
                if not node.get(field):
                    errors.append("formula " + node_id + " requires " + field)

    for edge in graph.get("edges", []):
        edge_label = str(edge.get("from")) + "->" + str(edge.get("to"))
        if edge.get("from") not in node_ids:
            errors.append("edge source " + str(edge.get("from")))
        if edge.get("to") not in node_ids:
            errors.append("edge target " + str(edge.get("to")))
        if not edge.get("relation") or not edge.get("summary"):
            errors.append("edge requires relation and summary")
        if not edge.get("sources"):
            errors.append("edge " + edge_label + " requires sources")
        else:
            for source_id in edge["sources"]:
                if source_id not in source_ids:
                    errors.append("edge " + edge_label + " references absent source " + source_id)
        if edge.get("evidence") not in {"documented", "operational_definition", "inference"}:
            errors.append("edge " + edge_label + " requires evidence classification")
    return errors


def search(graph, term, *, node_type=None):
    query = term.casefold().strip()
    return [
        node for node in graph.get("nodes", [])
        if (not node_type or node.get("type") == node_type)
        and query in (node.get("title", "") + " " + node.get("summary", "") + " " + node.get("id", "")).casefold()
    ]


def neighborhood(graph, node_id):
    node = next((item for item in graph.get("nodes", []) if item.get("id") == node_id), None)
    if node is None:
        raise KeyError("unknown node " + node_id)
    return {
        "node": node,
        "outgoing": [edge for edge in graph.get("edges", []) if edge.get("from") == node_id],
        "incoming": [edge for edge in graph.get("edges", []) if edge.get("to") == node_id],
    }


def main():
    parser = argparse.ArgumentParser(description="Validate or query the traffic knowledge graph")
    parser.add_argument("command", choices=("validate", "search", "show"))
    parser.add_argument("value", nargs="?")
    parser.add_argument("--type", dest="node_type")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    graph, sources = load_graph(args.root)
    if args.command == "validate":
        errors = validate(graph, sources)
        if errors:
            print("\n".join(errors))
            return 1
        print("Graph valid: {} nodes, {} edges, {} sources".format(len(graph["nodes"]), len(graph["edges"]), len(sources["sources"])))
        return 0
    if not args.value:
        parser.error("search and show require a value")
    result = search(graph, args.value, node_type=args.node_type) if args.command == "search" else neighborhood(graph, args.value)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
