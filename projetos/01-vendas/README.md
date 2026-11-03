# 01 — Análise de vendas com PySpark

**Em construção; execução no Databricks pendente.**

Pergunta: qual a receita por categoria e mês, depois da limpeza dos dados?

O notebook [01_pipeline.py](01_pipeline.py) gera 9 linhas fictícias em memória e grava tabelas Delta no schema `portfolio_igor_vendas`, dentro do catálogo atual. A data usa o padrão ISO `AAAA-MM-DD`; valores monetários são convertidos para decimal com duas casas.

## Regras
- ID, data, categoria, quantidade e preço precisam estar preenchidos.
- Quantidade maior que zero e preço não negativo.
- Datas precisam ser válidas.
- Duplicatas completamente idênticas são removidas.
- Registros inválidos são guardados em `vendas_invalidas`.

## Resultados esperados (não são evidências de execução)
| Medida | Esperado |
|---|---:|
| Linhas Bronze | 9 |
| Linhas inválidas | 2 |
| Linhas válidas antes da deduplicação | 7 |
| Linhas Silver | 6 |
| Duplicatas removidas | 1 |
| Receita janeiro/2026 | R$ 265,00 |
| Receita fevereiro/2026 | R$ 270,00 |
| Receita total | R$ 535,00 |

As quatro tabelas `vendas_bronze`, `vendas_silver`, `vendas_invalidas` e `vendas_gold` são substituídas a cada execução. Não altere o schema para um ambiente real.

Próxima atividade: explicar por que filtrar dados e remover duplicatas muda a receita; depois adicionar duas vendas e recalcular as expectativas.
