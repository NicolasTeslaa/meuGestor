# Grafo de conhecimento para gestão de tráfego — desenho da primeira versão

Data da decisão: 2026-10-25. Estado: aprovado em conversa, aguardando revisão deste documento.

## Objetivo e escopo

Transformar este repositório em uma base de conhecimento consultável por chats do Codex para apoiar decisões de investimento em anúncios. A prioridade é Meta Ads aplicado a serviços B2B e B2C no Brasil. A primeira versão é uma base de conhecimento, sem conexão com contas de anúncios e sem interface própria.

O resultado de negócio prioritário é **venda fechada e receita realizada**. Leads captados, leads qualificados, agendamentos e oportunidades são etapas intermediárias. O agente deve relacionar mídia, atendimento comercial e resultado financeiro antes de recomendar aumento, redução ou redistribuição de verba.

Esta versão cobre decisões sobre planejamento, campanha, público, criativo, posicionamento, orçamento, mensuração, experimentos, qualidade de leads, CRM e diagnóstico do funil. Não publicará anúncios nem alterará campanhas automaticamente.

## Abordagens consideradas

1. **Documentos Markdown ligados por links:** edição fácil, mas relações e integridade difíceis de validar.
2. **Banco de grafos desde o início:** consultas ricas, mas exige infraestrutura e operação antes de haver dados próprios.
3. **Grafo versionado em Git (escolhido):** registros estruturados de nós e relações, acompanhados de explicações legíveis, fontes e validação automática. Pode ser importado para um banco de grafos quando as consultas e o volume justificarem.

## Componentes e responsabilidades

- `AGENTS.md`: define o papel do especialista, o fluxo de resposta e a obrigação de consultar o grafo, verificar atualidade, explicitar hipóteses e indicar evidências.
- `knowledge/nodes/`: nós temáticos em arquivos estruturados pequenos. Cada nó possui `id`, `tipo`, `titulo`, `resumo`, `aplicabilidade`, `status`, `fontes`, `verificado_em` e, quando pertinente, fórmula, unidade, janela temporal e ressalvas.
- `knowledge/edges/`: relações direcionadas com `origem`, `relacao`, `destino`, justificativa e fontes quando a relação afirmar causalidade ou orientação.
- `knowledge/sources/`: catálogo de URLs, autoria, título, data conhecida, data de acesso, tipo de evidência, escopo e limitações. O grafo preserva o vínculo entre cada afirmação e a fonte que a sustenta.
- `knowledge/guides/`: interpretações curtas para leitura humana e exemplos de perguntas. Guias não substituem os nós como fonte de verdade.
- `scripts/` e `tests/`: validação de esquema, IDs únicos, pontas das relações existentes, fontes referenciadas, datas e casos de decisão.

O formato estruturado será textual e revisável por Git. O plano de implementação escolherá entre JSON e YAML conforme as dependências já disponíveis, sem alterar a semântica acima.

## Ontologia inicial

Tipos de nó: `objetivo_de_negocio`, `modelo_de_servico`, `etapa_do_funil`, `canal`, `objetivo_de_campanha`, `configuracao`, `evento`, `metrica`, `formula`, `sinal`, `hipotese`, `diagnostico`, `acao`, `experimento`, `restricao`, `fonte` e `pergunta_de_decisao`.

Relações iniciais: `mede`, `precede`, `depende_de`, `influencia`, `pode_indicar`, `confirma_ou_refuta`, `recomenda_avaliar`, `restringe`, `aplica_se`, `sustentado_por` e `contradiz`. `influencia` ou `pode_indicar` não significam causalidade comprovada; uma alegação causal deve indicar o desenho de evidência que a sustenta.

O caminho central liga investimento → impressões/visitas/contatos → qualificação → oportunidade → venda → receita e margem. B2B e B2C compartilham o vocabulário, mas registram diferenças de ciclo comercial, ticket, volume, capacidade de atendimento e janelas de observação. Fórmulas de CPL, custo por lead qualificado, CAC, taxa de fechamento, receita por lead e retorno sobre investimento terão denominadores, unidades e períodos explícitos. O grafo não fixa benchmarks universais de CPL, ROAS, frequência ou orçamento.

## Política de evidências e atualização

Fontes primárias da Meta explicam recursos, definições e funcionamento anunciado da plataforma. Estudos independentes, preferencialmente pesquisas originais e experimentos, ajudam a avaliar inferências de desempenho e causalidade. Publicidade institucional, estudos de caso e médias globais são identificados como evidência contextual, não como promessa de resultado para serviços no Brasil.

Cada afirmação recebe fonte, data de verificação, contexto de validade e nível de confiança. Informação que depende de versão de produto, política, disponibilidade regional ou regra legal precisa de nova verificação na internet antes de orientar uma decisão atual. Páginas inacessíveis sem login não serão tratadas como verificadas. Quando fontes discordarem, o agente apresentará a divergência e o que seria necessário medir no caso concreto.

Fontes iniciais já verificadas em 2026-10-25:

- [Meta Blueprint — geração de leads por formulários, mensagens e chamadas](https://www.facebookblueprint.com/student/path/253057-lead-gen-course).
- [Meta Blueprint — Conversions API para CRM e otimização por lead qualificado](https://www.facebookblueprint.com/student/path/253141-conversions-api-crm-lead-quality).
- [Meta Blueprint — tipos de testes e estudos de lift](https://www.facebookblueprint.com/student/path/219763-ab-test-conversion-brand-lift-course).
- [Meta Blueprint — Conversion Lift](https://www.facebookblueprint.com/student/path/253065-conversion-lift-marketing-measurement).
- [NBER — Measuring the Effects of Advertising: The Digital Frontier](https://www.nber.org/papers/w19520), pesquisa sobre dificuldades de inferir efeito de publicidade a partir de dados observacionais.
- [Google Research — Measuring Ad Effectiveness Using Geo Experiments](https://research.google/pubs/measuring-ad-effectiveness-using-geo-experiments/), referência metodológica independente da Meta para avaliação incremental.

## Fluxo de resposta do agente

1. Identificar objetivo de negócio, modelo B2B/B2C, janela de análise e etapa do funil relacionada à pergunta.
2. Recuperar nós e relações pertinentes, verificando fontes e validade temporal.
3. Separar fatos observados, hipóteses, cálculos e recomendações. Não preencher lacunas comerciais com números inventados.
4. Em decisões de verba, considerar vendas, receita, margem, tempo de maturação, qualidade dos leads, capacidade comercial e incerteza. Se faltarem dados decisivos, pedir os mínimos necessários e oferecer apenas uma decisão condicional.
5. Priorizar testes que discriminem hipóteses. Distinguir atribuição reportada pela plataforma de efeito incremental comprovado por experimento.
6. Responder em português claro, com conclusão operacional, condições para agir, riscos relevantes e links diretos às fontes utilizadas.

## Casos de aceitação

- **CPL caiu, devo escalar?** O agente não recomenda escala só pelo CPL. Verifica qualificação, fechamento, receita, margem, ciclo de vendas e se a amostra e a janela são suficientes. Explica como um CPL menor pode coexistir com CAC pior.
- **Formulário instantâneo ou site?** Compara fricção, volume, qualidade observada, capacidade de resposta e mensuração. Propõe teste com critério de sucesso ligado a vendas ou qualificação, não apenas ao total de leads.
- **Meta reporta ROAS alto, mas o caixa não cresceu.** Confere definição de receita, janela de atribuição, duplicidade de eventos, vendas orgânicas e atraso comercial. Não afirma causalidade a partir do ROAS da plataforma; sugere método de incrementabilidade quando viável.
- **B2B com ciclo de 90 dias.** Evita encerrar campanha por ausência de vendas em janela curta. Usa indicadores intermediários definidos e acompanha coortes até o desfecho comercial.
- **B2C local com equipe saturada.** Considera capacidade de atendimento e perda de leads antes de recomendar mais investimento.
- **Fonte desatualizada ou recurso incerto.** Explicita a incerteza, verifica documentação atual e não converte hipótese em regra.

## Verificação da primeira versão

Os testes de comportamento virão antes do código (RED → GREEN → REFACTOR) e validarão os casos acima, sobretudo ausência de recomendação de escala baseada apenas em CPL, distinção entre atribuição e incrementabilidade, e tratamento de ciclo comercial e dados ausentes. Testes estruturais verificarão integridade de nós, relações e citações. A revisão manual avaliará se respostas do agente citam fontes adequadas e deixam claras as limitações da evidência.

## Limites e evolução

Não haverá ingestão de dados privados, autenticação Meta, execução de campanha, automação de orçamento ou promessa de desempenho nesta etapa. Uma futura integração de contas poderá mapear fatos reais para a mesma ontologia, sem misturar observações de clientes com conhecimento geral. O aumento da base será guiado por decisões concretas, cobertura de fontes e manutenção, não por contagem de páginas.
