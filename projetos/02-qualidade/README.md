# 02 — Auditoria de qualidade com SQL

**Em construção.** Depende da execução do projeto 01 no mesmo catálogo.

O notebook [01_auditoria.py](01_auditoria.py) consulta as tabelas do primeiro projeto. Não grava nem remove dados. Compara contagens, IDs duplicados e receita; as verificações são para o conjunto fixo de exemplo.

Próximos passos para construirmos juntos:
- [ ] Executar e explicar as consultas SQL.
- [ ] Incluir porcentagem de rejeição, documentando o denominador (linhas Bronze).
- [ ] Adicionar classificação do motivo de rejeição.
- [ ] Tratar colisões de ID com conteúdo divergente.
- [ ] Criar histórico de auditoria com identificação de cada execução.
- [ ] Criar dashboard com contagens, taxa de rejeição e evolução.

Não há dashboard, histórico persistente ou monitoramento contínuo implementado nesta versão.
