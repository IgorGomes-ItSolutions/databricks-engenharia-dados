# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — Auditoria de qualidade com SQL
# MAGIC Execute o projeto 01 primeiro. Selecione o mesmo catálogo.
# MAGIC Este notebook apenas consulta as tabelas de laboratório.

# COMMAND ----------
spark.sql("USE SCHEMA portfolio_igor_vendas")
resumo = spark.sql("""
SELECT
  (SELECT COUNT(*) FROM vendas_bronze) AS linhas_bronze,
  (SELECT COUNT(*) FROM vendas_silver) AS linhas_silver,
  (SELECT COUNT(*) FROM vendas_invalidas) AS linhas_invalidas,
  (SELECT SUM(receita) FROM vendas_silver) AS receita_total
""")
display(resumo)
linha = resumo.first()
assert (linha.linhas_bronze, linha.linhas_silver, linha.linhas_invalidas) == (9, 6, 2)

# COMMAND ----------
# IDs repetidos na origem: o exemplo tem uma cópia idêntica do ID 6.
display(spark.sql("""
SELECT id_venda, COUNT(*) AS ocorrencias
FROM vendas_bronze
GROUP BY id_venda
HAVING COUNT(*) > 1
ORDER BY id_venda
"""))

# COMMAND ----------
# Não deve haver IDs repetidos após a limpeza.
conflitos = spark.sql("""
SELECT id_venda, COUNT(*) AS ocorrencias
FROM vendas_silver
GROUP BY id_venda
HAVING COUNT(*) > 1
""")
assert conflitos.count() == 0
display(spark.sql("SELECT * FROM vendas_invalidas ORDER BY id_venda"))

# COMMAND ----------
# Comparação calculada: resultado esperado 1 duplicata exata removida.
display(spark.sql("""
SELECT
 (SELECT COUNT(*) FROM vendas_bronze)
 - (SELECT COUNT(*) FROM vendas_invalidas)
 - (SELECT COUNT(*) FROM vendas_silver) AS duplicatas_removidas
"""))
