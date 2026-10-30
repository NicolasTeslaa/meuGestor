from pathlib import Path
import unittest


PAGE = Path(__file__).parents[1] / "essencia-aroma-estrategia.html"


class EssenciaAromaStrategyPageTest(unittest.TestCase):
    def test_page_presents_three_scenarios_for_the_martam_gold_campaign(self):
        self.assertTrue(PAGE.exists(), f"missing artifact: {PAGE}")
        html = PAGE.read_text(encoding="utf-8")

        html_lower = html.lower()
        for expected in (
            "Essência & Aroma",
            "Martam Gold",
            "Água de Lençóis",
            "220 ml",
            "R$ 49,99",
            "WhatsApp",
            "São José dos Campos e região",
            "Todo o Brasil",
            "Cenário 1",
            "Cenário 2",
            "Cenário 3",
            "pontos fortes",
            "pontos fracos",
            "conversa qualificada",
            "venda fechada",
            "receita realizada",
            "margem",
            "orçamento a definir",
            "preço informado pela cliente",
            "Não publicado no GitHub",
        ):
            self.assertIn(expected.lower(), html_lower)

        self.assertNotIn("Kit Um Momento".lower(), html_lower)
        self.assertNotIn("R$ 7/dia".lower(), html_lower)
        self.assertIn('meta name="viewport"', html)
        self.assertIn("@media", html)


if __name__ == "__main__":
    unittest.main()
