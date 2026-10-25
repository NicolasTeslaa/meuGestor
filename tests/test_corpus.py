import unittest
from collections import deque
from pathlib import Path

from scripts.graph import load_graph, neighborhood, search, validate


ROOT = Path(__file__).resolve().parents[1]


def reachable(graph, start, target):
    edges = graph["edges"]
    queue = deque([start])
    seen = set()
    while queue:
        current = queue.popleft()
        if current == target:
            return True
        if current not in seen:
            seen.add(current)
            queue.extend(edge["to"] for edge in edges if edge["from"] == current)
    return False


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph, cls.sources = load_graph(ROOT)

    def test_corpus_is_connected_and_sourced(self):
        self.assertEqual([], validate(self.graph, self.sources))
        self.assertGreaterEqual(len(self.graph["nodes"]), 45)
        self.assertGreaterEqual(len(self.graph["edges"]), 65)
        self.assertGreaterEqual(len(self.sources["sources"]), 8)

    def test_cpl_decision_reaches_revenue(self):
        self.assertTrue(reachable(self.graph, "metric.cpl", "outcome.revenue"))
        self.assertTrue(neighborhood(self.graph, "metric.cpl")["outgoing"])

    def test_attribution_reaches_incrementality_test(self):
        self.assertTrue(reachable(self.graph, "metric.platform_attribution", "experiment.conversion_lift"))

    def test_key_decision_topics_are_searchable(self):
        for term in ("receita", "lead qualificado", "incrementalidade", "capacidade de atendimento"):
            with self.subTest(term=term):
                self.assertTrue(search(self.graph, term))

    def test_formulas_define_operands_units_and_period(self):
        formulas = [node for node in self.graph["nodes"] if node["type"] == "formula"]
        self.assertGreaterEqual(len(formulas), 6)
        for node in formulas:
            with self.subTest(node=node["id"]):
                for field in ("numerator", "denominator", "unit", "period"):
                    self.assertTrue(node.get(field))


if __name__ == "__main__":
    unittest.main()
