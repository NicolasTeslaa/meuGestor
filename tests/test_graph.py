import tempfile
import unittest
from pathlib import Path

from scripts.graph import neighborhood, search, validate


def fixture():
    graph = {
        "nodes": [
            {"id": "metric.cpl", "type": "metric", "title": "CPL", "summary": "Custo por lead", "applies_to": ["b2b", "b2c"], "sources": ["meta.leads"]},
            {"id": "metric.qualified_lead", "type": "metric", "title": "Lead qualificado", "summary": "Contatos com perfil", "applies_to": ["b2b"], "sources": ["meta.leads"]},
            {"id": "stage.qualified_lead", "type": "stage", "title": "Lead qualificado", "summary": "Etapa comercial", "applies_to": ["b2b"], "sources": ["meta.leads"]},
        ],
        "edges": [
            {"from": "metric.cpl", "relation": "precedes", "to": "stage.qualified_lead", "summary": "CPL antecede qualificação", "sources": ["meta.leads"], "evidence": "inference"},
            {"from": "stage.qualified_lead", "relation": "measured_by", "to": "metric.qualified_lead", "summary": "Etapa medida pela contagem", "sources": ["meta.leads"], "evidence": "operational_definition"},
        ],
    }
    for node in graph["nodes"]:
        node.update(status="active", verified_at="2026-10-25", confidence="medium", context="Serviços B2B no Brasil com coorte definida")
    for edge in graph["edges"]:
        edge.update(verified_at="2026-10-25", confidence="medium", context="Coorte de serviços B2B no Brasil")
    return graph


def sources():
    return {"sources": [{"id": "meta.leads", "title": "Meta Blueprint", "url": "https://www.facebookblueprint.com/example", "kind": "official", "verified_at": "2026-10-25"}]}


class GraphValidationTests(unittest.TestCase):
    def test_rejects_missing_collections(self):
        self.assertIn("graph requires nonempty nodes", validate({}, {}))
        self.assertIn("graph requires edges list", validate({}, {}))
        self.assertIn("catalog requires nonempty sources", validate({}, {}))

    def test_accepts_connected_sourced_graph(self):
        self.assertEqual([], validate(fixture(), sources()))

    def test_rejects_duplicate_node_id(self):
        graph = fixture()
        graph["nodes"].append(dict(graph["nodes"][0]))
        self.assertIn("duplicate node id metric.cpl", validate(graph, sources()))

    def test_rejects_missing_and_malformed_ids(self):
        graph = fixture()
        catalog = sources()
        del graph["nodes"][0]["id"]
        catalog["sources"][0]["id"] = "bad id"
        errors = validate(graph, catalog)
        self.assertIn("node requires valid id", errors)
        self.assertIn("source requires valid id", errors)

    def test_rejects_node_without_claim_metadata(self):
        graph = fixture()
        del graph["nodes"][0]["verified_at"]
        del graph["nodes"][0]["confidence"]
        del graph["nodes"][0]["context"]
        del graph["nodes"][0]["status"]
        errors = validate(graph, sources())
        self.assertIn("node metric.cpl has invalid verified_at", errors)
        self.assertIn("node metric.cpl requires confidence", errors)
        self.assertIn("node metric.cpl requires context", errors)
        self.assertIn("node metric.cpl requires status", errors)

    def test_rejects_orphan_edge(self):
        graph = fixture()
        graph["edges"][0]["to"] = "missing"
        self.assertIn("edge target missing", validate(graph, sources()))

    def test_rejects_missing_source(self):
        graph = fixture()
        graph["nodes"][0]["sources"] = ["absent"]
        self.assertIn("node metric.cpl references absent source absent", validate(graph, sources()))

    def test_rejects_unsourced_claim(self):
        graph = fixture()
        graph["nodes"][0]["sources"] = []
        self.assertIn("node metric.cpl requires at least one source", validate(graph, sources()))

    def test_rejects_untraceable_relation(self):
        graph = fixture()
        del graph["edges"][0]["sources"]
        self.assertIn("edge metric.cpl->stage.qualified_lead requires sources", validate(graph, sources()))

    def test_rejects_relation_without_claim_metadata(self):
        graph = fixture()
        edge = graph["edges"][0]
        del edge["verified_at"]
        del edge["confidence"]
        del edge["context"]
        errors = validate(graph, sources())
        self.assertIn("edge metric.cpl->stage.qualified_lead has invalid verified_at", errors)
        self.assertIn("edge metric.cpl->stage.qualified_lead requires confidence", errors)
        self.assertIn("edge metric.cpl->stage.qualified_lead requires context", errors)

    def test_rejects_invalid_source_date_and_url(self):
        catalog = sources()
        catalog["sources"][0].update(url="http://example.com", verified_at="2026-15-99")
        errors = validate(fixture(), catalog)
        self.assertIn("source meta.leads requires HTTPS URL", errors)
        self.assertIn("source meta.leads has invalid verified_at", errors)


class GraphQueryTests(unittest.TestCase):
    def test_search_matches_title_and_filters_type(self):
        self.assertEqual(["metric.qualified_lead"], [item["id"] for item in search(fixture(), "LEAD QUALIFICADO", node_type="metric")])

    def test_neighborhood_includes_both_directions(self):
        result = neighborhood(fixture(), "stage.qualified_lead")
        self.assertEqual("stage.qualified_lead", result["node"]["id"])
        self.assertEqual("metric.cpl", result["incoming"][0]["from"])
        self.assertEqual("metric.qualified_lead", result["outgoing"][0]["to"])

    def test_unknown_node_raises_clear_error(self):
        with self.assertRaisesRegex(KeyError, "unknown node missing"):
            neighborhood(fixture(), "missing")


if __name__ == "__main__":
    unittest.main()
