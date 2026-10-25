# Ontologia e uso editorial

## Estrutura

`graph.json` contém `nodes` e `edges`. IDs estáveis seguem `categoria.nome`. Cada nó define tipo, título, resumo, aplicabilidade (`b2b`, `b2c`), contexto, estado, confiança, data de verificação, fontes e, quando necessário, `evidence`. Cada relação aponta para nós existentes, descreve o vínculo e registra fontes, contexto, confiança, data de verificação e classificação de evidência próprias. `status: review` significa que o nó deve ser revalidado antes de orientar uma decisão.

`sources.json` identifica fonte, publicador, URL HTTPS, data de verificação, escopo e limites. `official` significa documentação institucional da Meta ou órgão público; `research` significa pesquisa original. A classificação `operational_definition` registra convenção de cálculo do projeto. `inference` é análise do agente apoiada por fontes, sem atribuir a elas uma conclusão literal. `documented` fica reservado a uma afirmação explicitamente descrita na fonte. Confiança alta marca uma definição operacional estável ou um conceito documentado; média marca hipótese editorial que precisa de dados do anunciante. Confiança não é probabilidade estatística.

O caminho econômico principal é impressão → clique → lead → qualificação → oportunidade → proposta → venda → receita → margem. Existem ramificações para perda, mensuração, atendimento, testes e privacidade. Relações como `may_indicate` e `recommends_evaluating` são hipóteses condicionais, não relações causais comprovadas.

## Cálculos e comparabilidade

- CPL = investimento em mídia / leads únicos captados.
- Custo por lead qualificado = investimento / leads qualificados da mesma coorte.
- CAC de mídia = investimento / vendas fechadas da coorte. Não inclui automaticamente custos de equipe, software ou agência.
- Taxa de fechamento = vendas fechadas / oportunidades maduras da mesma coorte.
- Receita por lead = receita realizada / leads captados da coorte.
- CTR = cliques definidos / impressões. Informar se o clique é no link ou qualquer clique.
- CPM = investimento × 1.000 / impressões.
- ROI econômico incremental = (margem de contribuição incremental − investimento) / investimento. Sem evidência de incremento, não nomear o cálculo como incremental.

Se o denominador for zero, o quociente é indefinido; não informar zero como se fosse resultado. Especificar moeda, janela, coorte, origem e regra de deduplicação ao comparar períodos. Uma coorte ainda aberta não prova ausência de vendas futuras. Não há CPL, CAC, ROAS, frequência ou orçamento universalmente correto.

## Matriz manual de aceitação

| Pergunta | Caminho do grafo | Resposta esperada | Atalho indevido |
| --- | --- | --- | --- |
| O CPL caiu. Escalo? | `metric.cpl` → `metric.cpql` → `metric.cac` → `outcome.revenue`; `signal.low_cpl` → `action.hold_scale` | Conferir qualificação, vendas, receita, margem, maturação e capacidade; decidir condicionalmente. | Aumentar verba pelo CPL isolado. |
| Formulário instantâneo ou site? | `config.instant_form`/`config.website_form` → `action.test_formats` → `experiment.ab` | Comparar qualidade e desfecho comercial em teste. | Escolher pelo volume de leads apenas. |
| ROAS alto, caixa estável? | `metric.platform_attribution` → `signal.attribution_gap`/`experiment.conversion_lift` | Reconciliar CRM, eventos e janela; separar atribuição de incremento. | Tratar ROAS reportado como efeito causal. |
| B2B com ciclo de 90 dias? | `model.b2b` → `signal.long_cycle` → `diagnosis.immature_cohort` | Acompanhar coortes e indicadores comerciais intermediários até maturação. | Encerrar por falta de venda em poucos dias. |
| Equipe B2C saturada? | `model.b2c` → `signal.capacity_limit` → `diagnosis.slow_followup` | Medir fila, resposta e contato; ajustar atendimento antes de escalar. | Comprar mais leads sem capacidade. |
| Recurso Meta pode ter mudado? | `signal.stale_source` → `action.verify_current` | Consultar documentação atual e registrar incerteza. | Repetir informação histórica como regra vigente. |

## Como ampliar a base

Pesquise fontes atuais e registre seu escopo e limitações. Acrescente o menor conjunto de nós e relações que responda a uma decisão concreta. Indique se a relação é definição, afirmação documentada ou inferência. Rode `python3 -m scripts.graph validate` e `python3 -m unittest discover -s tests -v`. Não inclua dados de clientes, tokens ou capturas privadas neste corpus público.
