# Vendas, promoções e sobra de produção em uma rede de padarias

Projeto da disciplina de Data Analytics (PjBL) da PUCPR.

**Equipe:** Helena Picinin, Marco Capote, Raissa Queiroz e Rafael Sene

## Sobre o projeto

Padarias vendem produtos que estragam rápido e precisam decidir todos os dias quanto produzir. O que sobra vira prejuízo e o que falta vira venda perdida. Neste projeto usamos dois anos de vendas (2023 e 2024) de uma rede com três lojas para entender como horário, calendário, clima e promoções se relacionam com faturamento, margem e sobra de produtos.

Perguntas que o projeto vai responder ao longo dos RAs:

| ID | Pergunta |
|---|---|
| P1 | Como o faturamento e a quantidade de itens vendidos variam ao longo do dia, entre os dias da semana e entre as estações, em cada loja? |
| P2 | Dias de festival e as condições do tempo estão associados a mudanças no volume vendido e no faturamento de cada categoria? |
| P3 | Os itens vendidos com promoção, e cada tipo de promoção, vendem quantidade suficiente para compensar a margem menor? |
| P4 | Quais produtos, categorias e níveis de perecibilidade concentram os maiores percentuais de sobra? |

## Dados

- **Fonte:** [Bakery Sales, Customer & Inventory Analytics Dataset](https://www.kaggle.com/datasets/sdcloud/historical-bakery-sales-dataset), publicado no Kaggle por `sdcloud` (acesso em 20/10/2026).
- **Licença:** CC0 (domínio público). Por isso o CSV original está versionado em `data/raw/`.
- **Formato:** CSV, UTF-8 com BOM, 19.321 linhas e 40 colunas.
- **Cobertura:** 01/01/2023 a 31/12/2024, 3 lojas, 35 produtos e 500 clientes.
- **Granularidade:** cada linha é um produto dentro de um pedido. Um pedido com três produtos ocupa três linhas.
- **Observação:** os dados são sintéticos, criados pelo autor para fins educacionais.

Se o arquivo de `data/raw/` não existir, o notebook baixa o CSV direto do Kaggle (o endereço de download é público e não pede login).

## Estrutura

```text
padaria-data-analytics/
├── projeto_data_analytics.ipynb    notebook com RA1 e RA2 (feito a partir do template da disciplina)
├── data/
│   ├── raw/
│   │   └── bakery_sales_dataset.csv       dados originais do Kaggle, sem alteração
│   └── processed/
│       └── bakery_sales_preparado.csv     saída do RA1 (gerada pelo notebook)
├── docs/
│   ├── Documentacao_RA1_Data_Analytics.docx   documentação do RA1 (template da disciplina)
│   └── projeto_data_analytics.pdf             notebook exportado em PDF (entrega do RA2)
├── requirements.txt
└── README.md
```

## Como executar

Precisa de Python 3.10 ou mais novo e, para o RA2, de Java 17 (exigido pelo Spark 4).

```bash
git clone <url-do-repositorio>
cd padaria-data-analytics
python -m pip install -r requirements.txt
jupyter notebook projeto_data_analytics.ipynb
```

Depois é só rodar todas as células em ordem (Kernel > Restart & Run All). A execução completa leva cerca de 1 minuto.

**No Windows**, o Spark precisa do `winutils.exe` e do `hadoop.dll` para monitorar a pasta do streaming e gravar o checkpoint. Sem eles, o RA2 falha com `UnsatisfiedLinkError`. Baixe os dois arquivos da versão 3.4 do Hadoop (por exemplo, do repositório [kontext-tech/winutils](https://github.com/kontext-tech/winutils/tree/master/hadoop-3.4.0-win10-x64/bin)) e coloque em `C:\hadoop\bin`. O notebook já configura o `HADOOP_HOME` apontando para essa pasta.

**No Google Colab**, envie o notebook e rode normalmente. O CSV é baixado do Kaggle na primeira célula de ingestão, e o PySpark é instalado se ainda não estiver disponível.

### Como saber se deu certo

- A seção 6 mostra as 12 regras de validação com `OK` e salva `data/processed/bakery_sales_preparado.csv` com 19.321 linhas e 42 colunas.
- Na seção 11, a célula de conferência imprime `Streaming e batch iguais? True`.

## RA1: ingestão e preparação

Principais pontos da preparação (detalhes nas seções 3 a 6 do notebook):

- Não há duplicatas. O `Order_ID` se repete porque cada produto do pedido é uma linha; a chave do registro é `Order_ID` + `Product`.
- `Festival` e `Promotion_Type` vazios significam "sem festival" e "sem promoção" e foram preenchidos com `No Festival` e `No Promotion`.
- 2.089 itens têm desconto, mas estão marcados como sem promoção. Os valores foram mantidos, porque preço, total e lucro já foram calculados com o desconto, e criamos a coluna `Discount_Without_Promotion` para identificar esses casos.
- `Date` virou data, `Time` foi padronizado em `HH:MM` e as colunas Yes/No viraram booleanas.
- Criamos a coluna `Timestamp` (data e hora da venda), usada no RA2.
- Outliers, lucros negativos e as colunas de lote foram mantidos, com justificativa.

A base preparada tem 19.321 linhas e 42 colunas, sem valores ausentes.

## RA2: streaming com janelas de tempo

Cenário A (simulação). Criamos vendas artificiais de um dia novo (06/01/2025), com produtos e preços tirados da base do RA1, e publicamos em quatro lotes de arquivos JSON numa pasta monitorada pelo Spark Structured Streaming. O faturamento e os itens vendidos são calculados em uma sliding window de 1 hora com deslocamento de 30 minutos. A simulação inclui uma venda com quantidade zero (descartada pelo filtro) e uma venda que chega atrasada e atualiza janelas antigas.

## Ferramentas

Python 3.12, pandas 2.2, PySpark 4.0.3 e Jupyter.
