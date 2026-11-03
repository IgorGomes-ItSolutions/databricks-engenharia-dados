# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Pipeline didático de vendas
# MAGIC Código inicial de estudo; executar uma célula por vez.
# MAGIC Usa o catálogo atual. Cria o schema portfolio_igor_vendas e substitui
# MAGIC somente as quatro tabelas de laboratório nomeadas abaixo.
# MAGIC Se esse schema já contiver dados seus, escolha outro nome antes de executar.

# COMMAND ----------
from decimal import Decimal
from pyspark.sql import functions as F

SCHEMA = "portfolio_igor_vendas"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
spark.sql(f"USE SCHEMA {SCHEMA}")
print("Catálogo e schema:", spark.sql("SELECT current_catalog(), current_schema()").collect())

# COMMAND ----------
# Valores de preço são strings para conversão explícita para decimal.
dados = [
    (1, "2026-01-05", "Livros", 2, "50.00"),
    (2, "2026-01-10", "Papelaria", 3, "15.00"),
    (3, "2026-01-20", "Tecnologia", 1, "120.00"),
    (4, "2026-02-02", "Livros", 1, "50.00"),
    (5, "2026-02-10", "Papelaria", 4, "25.00"),
    (6, "2026-02-12", "Tecnologia", 1, "120.00"),
    (6, "2026-02-12", "Tecnologia", 1, "120.00"),  # duplicata exata
    (7, "2026-02-15", "Livros", -1, "50.00"),  # quantidade inválida
    (8, "data-invalida", "Livros", 1, "50.00"),
]
bronze = spark.createDataFrame(
    dados, "id_venda INT, data_texto STRING, categoria STRING, quantidade INT, preco_texto STRING"
)
bronze.write.format("delta").mode("overwrite").saveAsTable("vendas_bronze")
assert bronze.count() == 9
display(bronze)

# COMMAND ----------
tipados = (spark.table("vendas_bronze")
    .withColumn("data_venda", F.expr("try_cast(data_texto AS DATE)"))
    .withColumn("preco_unitario", F.expr("try_cast(preco_texto AS DECIMAL(12,2))")))
regra = (
    F.col("id_venda").isNotNull()
    & F.col("data_venda").isNotNull()
    & F.col("categoria").isNotNull()
    & (F.length(F.trim(F.col("categoria"))) > 0)
    & F.col("quantidade").isNotNull() & (F.col("quantidade") > 0)
    & F.col("preco_unitario").isNotNull() & (F.col("preco_unitario") >= 0)
)
classificados = tipados.withColumn("valido", F.coalesce(regra, F.lit(False)))
invalidos = classificados.filter(~F.col("valido"))
validos = classificados.filter(F.col("valido"))
silver = (validos.select("id_venda", "data_venda", "categoria", "quantidade", "preco_unitario")
    .dropDuplicates()
    .withColumn("receita", (F.col("quantidade") * F.col("preco_unitario")).cast("decimal(18,2)")))
# Duplicatas conflitantes devem ser tratadas antes de evoluir este exemplo.
assert silver.select("id_venda").distinct().count() == silver.count(), "IDs conflitantes: revisar política"
invalidos.write.format("delta").mode("overwrite").saveAsTable("vendas_invalidas")
silver.write.format("delta").mode("overwrite").saveAsTable("vendas_silver")
assert invalidos.count() == 2
assert validos.count() == 7
assert silver.count() == 6
assert validos.count() - silver.count() == 1
display(invalidos)

# COMMAND ----------
gold = (spark.table("vendas_silver")
    .withColumn("mes", F.date_format("data_venda", "yyyy-MM"))
    .groupBy("mes", "categoria")
    .agg(F.sum("receita").alias("receita_total"), F.sum("quantidade").alias("itens")))
gold.write.format("delta").mode("overwrite").saveAsTable("vendas_gold")
totais = {r["mes"]: r["total"] for r in gold.groupBy("mes").agg(F.sum("receita_total").alias("total")).collect()}
assert totais == {"2026-01": Decimal("265.00"), "2026-02": Decimal("270.00")}
assert sum(totais.values()) == Decimal("535.00")
display(gold.orderBy("mes", "categoria"))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Agora é sua vez
# MAGIC Explique cada transformação. Adicione duas vendas fictícias, calcule o novo total
# MAGIC manualmente e só depois ajuste as verificações. Registre resultados reais no README.
