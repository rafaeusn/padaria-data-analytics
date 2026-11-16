# Vendas, promoções e sobra de produção em uma rede de padarias

Projeto da disciplina de Data Analytics (PjBL) da PUCPR — Sistemas de Informação, 6º período. Professora: Marina de Lara.

**Equipe:** Helena Picinin, Marco Capote, Raissa Queiroz e Rafael Sene

## Sobre o projeto

Padarias vendem produtos que estragam rápido e precisam decidir todos os dias quanto produzir. O que sobra vira prejuízo e o que falta vira venda perdida. Neste projeto usamos dois anos de vendas (2023 e 2024) de uma rede com três lojas para entender como horário, calendário, clima e promoções se relacionam com faturamento, margem e sobra de produtos.

Perguntas que o projeto responde ao longo dos RAs:

| ID | Pergunta |
|---|---|
| P1 | Como o faturamento e a quantidade de itens vendidos variam ao longo do dia, entre os dias da semana e entre as estações, em cada loja? |
| P2 | Dias de festival e as condições do tempo estão associados a mudanças no volume vendido e no faturamento de cada categoria? |
| P3 | Os itens vendidos com promoção, e cada tipo de promoção, vendem quantidade suficiente para compensar a margem menor? |
| P4 | Quais produtos, categorias e níveis de perecibilidade concentram os maiores percentuais de sobra? |

## Dados

- **Fonte:** [Bakery Sales, Customer & Inventory Analytics Dataset](https://www.kaggle.com/datasets/sdcloud/historical-bakery-sales-dataset), publicado no Kaggle por `sdcloud` (versão 2, acesso em 20/10/2026).
- **Licença:** CC0 (domínio público). Por isso o CSV original está versionado em `data/raw/`.
- **Formato:** CSV, UTF-8 com BOM, 19.321 linhas e 40 colunas.
- **Cobertura:** 01/01/2023 a 31/12/2024, 3 lojas, 35 produtos e 500 clientes.
- **Granularidade:** cada linha é um produto dentro de um pedido. Um pedido com três produtos ocupa três linhas.
- **Observação:** os dados são sintéticos, criados pelo autor para fins educacionais.

Se o arquivo de `data/raw/` não existir, o notebook baixa o CSV direto do Kaggle (o endereço de download é público e não pede login).

## Estrutura

```text
padaria-data-analytics/
├── projeto_data_analytics.ipynb           notebook com RA1 e RA2 (feito a partir do template da disciplina)
├── RA3_Analise_e_Machine_Learning.ipynb   notebook do RA3: estatística, gráficos, ML e testes
├── data/
│   ├── raw/
│   │   └── bakery_sales_dataset.csv       dados originais do Kaggle, sem alteração
│   └── processed/
│       └── bakery_sales_preparado.csv     saída do RA1 (gerada pelo notebook)
├── outputs/                               saídas do RA3 (geradas pelo notebook)
│   ├── graficos/                          8 gráficos em PNG
│   └── ra3_resultados.md                  resumo dos resultados com os números da execução
├── tests/
│   └── test_ra3.py                        testes automatizados do RA3 (pytest)
├── docs/
│   ├── Documentacao_RA1_Data_Analytics.docx         documentação do RA1 (template da disciplina)
│   ├── projeto_data_analytics.pdf                   notebook exportado em PDF (entrega do RA2)
│   ├── Projeto_Data_Analytics_RA1_RA2_RA3.docx      documentação final integrada (RA1 + RA2 + RA3)
│   └── Projeto_Data_Analytics_RA1_RA2_RA3.pdf       mesma documentação em PDF (entrega do RA3)
├── requirements.txt
└── README.md
```

## Como executar

Precisa de Python 3.10 ou mais novo e, só para o RA2, de Java 17 (exigido pelo Spark 4).

```bash
git clone https://github.com/rafaeusn/padaria-data-analytics.git
cd padaria-data-analytics
python -m pip install -r requirements.txt
python -m notebook
```

Abra o notebook desejado e rode todas as células em ordem (*Kernel > Restart & Run All*):

| Notebook | Conteúdo | Tempo aproximado |
|---|---|---|
| `projeto_data_analytics.ipynb` | RA1 (ingestão, limpeza, validação) e RA2 (streaming com Spark) | 1 minuto |
| `RA3_Analise_e_Machine_Learning.ipynb` | RA3 (estatística, visualizações, Machine Learning e testes) | 30 segundos |

O notebook do RA3 não depende do Spark nem do Java: ele lê `data/processed/bakery_sales_preparado.csv` e, se esse arquivo não existir, reconstrói o preparo do RA1 a partir de `data/raw/`.

Use `python -m notebook` (e não só `jupyter notebook`): assim o Jupyter roda no mesmo Python em que o `requirements.txt` foi instalado. **Se mesmo assim aparecer `ModuleNotFoundError`** (por exemplo, `No module named 'sklearn'`), o notebook está usando outro Python. Registre o ambiente como kernel e selecione-o em *Kernel > Change kernel*:

```bash
python -m ipykernel install --user --name padaria --display-name "Python (padaria)"
```

**No Windows**, o Spark precisa do `winutils.exe` e do `hadoop.dll` para monitorar a pasta do streaming e gravar o checkpoint. Sem eles, o RA2 falha com `UnsatisfiedLinkError`. Baixe os dois arquivos da versão 3.4 do Hadoop (por exemplo, do repositório [kontext-tech/winutils](https://github.com/kontext-tech/winutils/tree/master/hadoop-3.4.0-win10-x64/bin)) e coloque em `C:\hadoop\bin`. O notebook já configura o `HADOOP_HOME` apontando para essa pasta.

**No Google Colab**, envie o notebook e rode normalmente. No RA1/RA2, o CSV é baixado do Kaggle na primeira célula de ingestão, e o PySpark é instalado se ainda não estiver disponível. No RA3, envie também o CSV para `data/processed/` (ou deixe o notebook baixar a base bruta).

### Como saber se deu certo

- **RA1:** a seção 6 mostra as 12 regras de validação com `OK` e salva `data/processed/bakery_sales_preparado.csv` com 19.321 linhas e 42 colunas.
- **RA2:** na seção 11, a célula de conferência imprime `Streaming e batch iguais? True`.
- **RA3:** a seção 5 mostra os 11 testes de consistência com `OK` e imprime `Todos os 11 testes passaram.`; a pasta `outputs/graficos/` fica com 8 gráficos e `outputs/ra3_resultados.md` é recriado.

### Testes automatizados

```bash
python -m pytest -v
```

Os testes executam o notebook do RA3 do zero em uma pasta temporária e conferem: a base preparada (19.321 linhas, 42 colunas, chave única, sem ausentes), a execução sem erros, os 11 testes internos, os 8 gráficos, o relatório em Markdown e o desempenho do modelo frente à referência.

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

## RA3: análise, visualização e Machine Learning

Notebook: `RA3_Analise_e_Machine_Learning.ipynb`. Documentação: `docs/Projeto_Data_Analytics_RA1_RA2_RA3.pdf` (seção RA3).

| Requisito | Técnica usada | Onde está |
|---|---|---|
| Estatística descritiva | Média, mediana, desvio-padrão, amplitude, quartis, assimetria, frequências e histogramas de `Quantity`, `Total_Bill`, `Profit` e `Waste_Pct` | Seção 1 e Gráfico 1 |
| Visualizações | 8 gráficos (barras, histogramas, boxplots e série temporal), cada um com interpretação | Seção 2 e `outputs/graficos/` |
| Amostragem e representatividade | Censo da base sintética; origem, abrangência, adequação e vieses | Seção 3 |
| Machine Learning | Regressão com Random Forest, divisão temporal treino/teste, MAE, RMSE e R² contra uma referência simples | Seção 4 |
| Testes | 11 verificações automáticas (sem vazamento de dados, divisão correta, saídas gravadas) + `pytest` | Seção 5 e `tests/` |
| Conclusões | Síntese, limitações e relação com P1–P4 | Seção 6 e `outputs/ra3_resultados.md` |

Principais resultados:

- **P1:** picos às 9h (5.610 unidades) e às 17h; os fins de semana vendem cerca de 39% mais por dia que os dias úteis, nas três lojas.
- **P2:** a mediana de vendas em dias de festival é 2,75 vezes a dos outros dias (132 contra 48 unidades). Neblina tem a maior média por clima, mas é o clima com menos dias — associação, não causa.
- **P3:** itens sem desconto têm a maior margem (45,4%). Só a promoção Festival aumenta as unidades por item (2,86 contra 2,15) e mantém o lucro médio por item; Clearance e Flash Sale reduzem margem sem ganho de volume.
- **P4:** a sobra mediana é 33,3% em todos os níveis de perecibilidade; bolos e itens de mercearia lideram a sobra (mediana de 50%).
- **Machine Learning:** prevendo as vendas do dia seguinte por loja e categoria, o Random Forest teve MAE de 2,526 unidades contra 2,801 da média dos 7 dias anteriores (−9,8%), RMSE de 3,727 contra 4,217 e R² de 0,203 contra −0,020. O ganho é real, mas o erro ainda é alto frente à venda média (2,87 unidades) e os picos são suavizados.

Limitações: base sintética, clima diário, sem localização das lojas, moeda, ID de lote ou registro de rupturas de estoque; promoções e festivais não são experimentos controlados.

## Ferramentas

Python 3.12, pandas 2.2, PySpark 4.0.3, matplotlib, scikit-learn, pytest e Jupyter.
