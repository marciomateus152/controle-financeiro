# 📊 FinDash Pro (Controle Financeiro)

Bem-vindo ao **FinDash Pro**, um sistema de automação para extração de dados e geração de dashboards financeiros em HTML. 

Este projeto foi desenvolvido para otimizar o controle de finanças, processando dados brutos e transformando-os em visualizações claras e acessíveis diretamente no navegador.

---

## ⚙️ Funcionalidades

- **Motor ETL (Extract, Transform, Load):** Processamento e organização de dados financeiros.
- **Geração Dinâmica de HTML:** Construção automatizada de dashboards para visualização imediata.
- **Arquitetura Modular:** Código estruturado em módulos independentes (`etl_engine`, `html_builder`, `generator`) para facilitar a manutenção e escalabilidade.
- **Automação via Batch:** Script `FinDash_Start.bat` para execução rápida do sistema com um único clique.

---

## 🚀 O Ciclo de Atualização (Git Workflow)

Abaixo está o fluxo de trabalho utilizado para versionar este projeto e enviá-lo para a nuvem:

```mermaid
graph LR
    A[💻 Seu Computador <br/> Diretório de Trabalho] -- "git add ." --> B[📥 Área de Preparação <br/> Staging Area]
    B -- "git commit -m" --> C[📦 Repositório Local <br/> Git Local]
    C -- "git push origin main" --> D[☁️ Nuvem <br/> GitHub]
