Com certeza. Com base em toda a estrutura de pastas e nos resultados que você gerou, preparei um README.md completo. Este arquivo é formatado em Markdown; basta copiá-lo e colá-lo no arquivo README.md na raiz do seu projeto no GitHub.Ele está estruturado para contar a "história" da sua análise, desde a visão geral até a correlação estatística, que é o ponto principal da sua investigação.(Copie e cole o conteúdo abaixo)Projeto-IC: Análise da Epidemia de Zika/SCZ em Pernambuco e sua Correlação com Fatores SocioeconômicosEste repositório contém os scripts e resultados de um projeto de Iniciação Científica que investiga a epidemia da Síndrome Congênita do Zika (SCZ) no estado de Pernambuco. O objetivo principal é analisar a evolução temporal e a distribuição espacial dos casos, e investigar a correlação entre a taxa de incidência da doença e indicadores socioeconômicos, como o IDHM e o PIB per capita.📈 Principais ResultadosA análise segue uma narrativa lógica, partindo do panorama geral (quando e onde) para uma investigação aprofundada das causas (por quê).1. Panorama Temporal: Quando ocorreu o pico?A primeira análise mostra a evolução dos casos confirmados de SCZ em Pernambuco ao longo dos anos. O pico da epidemia é claramente visível em 2015 e 2016, justificando o foco da análise neste período.2. Panorama Espacial: Onde se concentraram os casos?A análise espacial inicial mostra a distribuição dos casos absolutos no estado. Observa-se uma concentração significativa na Região Metropolitana do Recife (RMR) e em polos regionais.3. Análise de Incidência: Quais municípios foram proporcionalmente mais afetados?Analisar números absolutos pode ser enganoso, pois cidades mais populosas naturalmente têm mais casos. Ao calcular a taxa de incidência (casos por 100.000 habitantes), o cenário muda. O gráfico abaixo revela os 20 municípios proporcionalmente mais impactados, destacando cidades que não apareciam no mapa de casos absolutos.4. Correlação Socioeconômica: Por que esses municípios?Esta é a hipótese central do estudo: a vulnerabilidade socioeconômica foi um fator determinante na gravidade da epidemia? Para investigar isso, cruzamos a taxa de incidência com indicadores como IDHM (Índice de Desenvolvimento Humano Municipal) e PIB per capita.Os gráficos de dispersão abaixo sugerem uma tendência negativa: municípios com menor IDH e menor PIB tenderam a apresentar taxas de incidência de Zika/SCZ mais elevadas.Taxa de Incidência vs. IDHMTaxa de Incidência vs. PIB per capita5. A Prova Estatística: O Heatmap de CorrelaçãoPara confirmar a tendência visual, foi calculada a correlação estatística (Coeficiente de Pearson) entre as variáveis. O mapa de calor demonstra uma correlação negativa de moderada a forte entre a taxa de incidência e os indicadores de desenvolvimento (IDHM, Renda, PIB).Isso sugere que piores condições socioeconômicas estão associadas a um maior impacto da epidemia de Zika/SCZ.🏛️ Estrutura do ProjetoO projeto é organizado em pastas que separam os dados brutos, os dados processados, os scripts de análise e os resultados finais.Projeto-IC/
│
├── dados/
│   ├── brutos/       # Arquivos originais (SINAN .csv, Shapefiles .shp, IBGE .csv)
│   └── processados/  # Arquivos intermediários (dados limpos, taxas calculadas)
│
├── resultados/
│   ├── graficos/     # Gráficos de barra, dispersão e heatmaps (.png)
│   └── mapas/        # Mapas coropléticos (.png)
│
├── scripts/
│   ├── 01_coleta_dados.py       # Carrega, limpa dados do SINAN e gera análise temporal/espacial.
│   ├── 02_calcular_taxas.py     # Calcula a taxa de incidência proporcional e gera o top 20.
│   ├── 03_analise_correlacao.py # Junta dados socioeconômicos e gera gráficos de correlação.
│   └── 05_analise_interativa.py # (Script para mapas interativos com Plotly/Folium)
│
└── README.md                    # Este arquivo.
🚀 Como Executar o ProjetoPara replicar esta análise, siga os passos abaixo:1. Pré-requisitosCertifique-se de ter o Python 3.10+ e as seguintes bibliotecas instaladas:Bashpip install pandas geopandas matplotlib seaborn
2. Execução dos ScriptsOs scripts devem ser executados em ordem, pois um depende do arquivo gerado pelo anterior.Bash# 1. Limpa os dados e gera os gráficos/mapas iniciais
python scripts/01_coleta_dados.py

# 2. Calcula as taxas de incidência
python scripts/02_calcular_taxas.py

# 3. Realiza a análise de correlação socioeconômica
python scripts/03_analise_correlacao.py
📄 Relatório CompletoPara uma análise detalhada da metodologia, discussão aprofundada dos resultados e conclusões, aceda ao relatório final do projeto:[Link para o Relatório Final em PDF](Substitua este link pelo caminho do seu PDF quando o tiver)
