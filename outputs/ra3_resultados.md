# RA3 — Resultados do projeto: padarias

Equipe: Helena Picinin, Marco Capote, Raissa Queiroz e Rafael Sene.

## Origem e representatividade
Base sintética do Kaggle, 19.321 itens de pedidos; 6.576 pedidos distintos; 3 lojas; 7 categorias; 35 produtos; período de 01/01/2023 a 31/12/2024. Censo dos registros disponíveis, não amostragem. Não generalizável diretamente a padarias reais; grupos desiguais (72 dias com festival, 58 dias de neblina).

## Estatística descritiva
| Variável por item | Média | Mediana | Desvio-padrão | Mín. | Q1 | Q3 | Máx. | Amplitude |
|---|---|---|---|---|---|---|---|---|
| Quantidade (unidades) | 2,23 | 2,00 | 1,78 | 1,00 | 1,00 | 3,00 | 20,00 | 19,00 |
| Faturamento | 139,27 | 82,80 | 157,77 | 13,12 | 52,12 | 146,54 | 1.885,96 | 1.872,84 |
| Lucro | 59,20 | 36,76 | 65,24 | -0,55 | 20,69 | 65,92 | 767,60 | 768,15 |
| Waste_Pct (%) | 34,12 | 33,30 | 12,73 | 4,20 | 25,00 | 50,00 | 50,00 | 45,80 |

- Distribuição: 43,6% dos itens têm 1 unidade e 74,6% até 2; faturamento com assimetria 3,43; 33,3% dos registros têm Waste_Pct = 50%.

## Visualizações e interpretações
1. `01_distribuicao_variaveis.png`: quantidade e faturamento com cauda longa à direita; sobra concentrada em poucos valores (lotes pequenos).
2. `02_unidades_por_hora.png`: pico às 9h (5.610 unidades) e às 17h; 8h–10h = 32,8% e 16h–18h = 25,6% das unidades.
3. `03_media_por_dia_semana.png`: maior média em Sáb (74,8 unidades/dia); fim de semana +39% sobre os dias úteis, nas três lojas.
4. `04_media_por_clima.png`: maior média em Foggy (67,41 unidades/dia; 58 dias; 12,1% com festival). Associação, sem inferência causal.
5. `05_festival_boxplot.png`: medianas de 132 (com festival, n = 72) e 48 (sem festival, n = 659) unidades/dia; razão de 2,75.
6. `06_promocoes_margem_unidades.png`: maior margem em Sem desconto (45,41%); só a promoção Festival aumenta unidades por item (2,86 contra 2,15) e mantém o lucro médio por item (64,28 contra 62,83).
7. `07_sobra_perecibilidade.png`: medianas iguais (33,3%); médias de 33,0% (Very High) a 37,1% (Medium).
8. `08_ml_observado_previsto.png`: a previsão acompanha o nível e os festivais, mas suaviza os picos.

## Machine Learning supervisionado — regressão
- Alvo: unidades vendidas registradas por data, loja e categoria.
- Entradas: loja, categoria, calendário, festival e lags/médias de vendas passadas.
- Treino: 12831 observações anteriores a 01/10/2024; teste: 1932 observações posteriores (out–dez/2024).
- Modelo: Random Forest Regressor; referência: média dos 7 dias anteriores.

| Métrica | Random Forest | Referência |
|---|---|---|
| MAE (unidades) | 2,526 | 2,801 |
| RMSE (unidades) | 3,727 | 4,217 |
| R² | 0,203 | -0,020 |

- Redução do MAE: 9,8%. Venda média no teste: 2,87 unidades por grupo/dia (MAE = 88% dessa média).
- Interpretação: o modelo superou a referência simples no recorte de teste, mas ainda erra bastante em termos relativos e suaviza picos.

## Testes de consistência
11 verificações automáticas aprovadas (sem vazamento de dados nos lags, divisão temporal correta, previsões válidas, base íntegra e gráficos gravados).

## Limitações e conclusão
A base é sintética; clima é diário; não há localização das lojas, moeda, ID de lote, rupturas de estoque nem perdas observadas por produto. O projeto mostra quando produzir mais (manhã, fim da tarde, fins de semana e festivais), quais promoções reduzem margem sem ganho de volume e uma previsão de curto prazo melhor que a média simples; não fornece ainda uma política comprovada de produção ótima.

Fonte: sdcloud, Bakery Sales, Customer & Inventory Analytics Dataset, Kaggle. https://www.kaggle.com/datasets/sdcloud/historical-bakery-sales-dataset
