# meuGestor — grafo de conhecimento para tráfego pago

Base de conhecimento para chats do Codex orientarem decisões de Meta Ads em serviços B2B e B2C no Brasil. A prioridade é receita de vendas fechadas, com atenção à margem e ao ciclo comercial. Não há conexão com contas de anúncios nesta versão.

## Uso rápido

```bash
python3 -m scripts.graph validate
python3 -m scripts.graph search 'lead qualificado'
python3 -m scripts.graph show metric.cpl
python3 -m unittest discover -s tests -v
```

O agente lê [AGENTS.md](AGENTS.md), consulta os [nós e relações](knowledge/graph.json) e confere o [catálogo de fontes](knowledge/sources.json). Consulte [a ontologia e os exemplos de aceitação](knowledge/README.md) antes de ampliar a base.

O corpus inicial contém conceitos, métricas, fórmulas, sinais, diagnósticos, ações e experimentos. Cada relação tem uma classificação de evidência e referências de apoio. `inference` marca uma interpretação operacional a testar no contexto do anunciante. As datas do catálogo indicam quando os links e resumos foram verificados; características atuais da Meta exigem nova consulta.

## Perguntas que a base ajuda a responder

- O CPL caiu: há margem e vendas para aumentar a verba?
- Formulário instantâneo, site, conversa ou ligação produz clientes melhores?
- Por que o ROAS do Ads Manager diverge do CRM e do caixa?
- Quando um ciclo B2B longo permite julgar o investimento?
- O limite está no anúncio, na qualificação ou na capacidade comercial?

O [desenho aprovado](docs/superpowers/specs/2026-10-25-grafo-gestao-trafego-design.md) e o [plano de implementação](docs/superpowers/plans/2026-10-25-grafo-gestao-trafego.md) registram decisões e limites desta versão.
