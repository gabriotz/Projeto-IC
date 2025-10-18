import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CARREGAR OS DADOS PROPORCIONAIS ---
print("Carregando o arquivo com as taxas proporcionais...")
try:
    # Este arquivo deve ter sido gerado pelo script analise_proporcional.py
    df_proporcional = pd.read_csv('dados/processados/taxas_proporcionais.csv')
except FileNotFoundError:
    print("ERRO: O arquivo 'dados_zika_proporcional_pe.csv' não foi encontrado.")
    print("Por favor, execute o script 'analise_proporcional.py' primeiro para gerar o arquivo necessário.")
    exit()

# --- 2. PREPARAR OS DADOS PARA O GRÁFICO ---
# Ordena o dataframe pela taxa e seleciona os 20 maiores valores
top_20_municipios = df_proporcional.sort_values(by='taxa_por_10k_hab', ascending=False).head(20)

# --- 3. CRIAR O GRÁFICO DE BARRAS HORIZONTAL ---
print("Gerando o gráfico de barras...")
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(12, 10)) # Tamanho ajustado para caber 20 barras confortavelmente

# Usamos barh para criar um gráfico de barras horizontal.
# Invertemos a ordem dos dados com [::-1] para que o município com a maior taxa fique no topo.
sns.barplot(
    x='taxa_por_10k_hab',
    y='municipio_nome',
    data=top_20_municipios.iloc[::-1], # Inverte a ordem aqui
    palette='inferno',
    hue='municipio_nome',
    legend=False
)

# --- 4. CUSTOMIZAR E SALVAR O GRÁFICO ---
plt.title('Top 20 Municípios por Taxa de Incidência de SCZ em Pernambuco (2015-2024)', fontsize=16, pad=20)
plt.xlabel('Taxa de Casos por 10.000 Habitantes', fontsize=12)
plt.ylabel('Município', fontsize=12)

# Adiciona o valor exato da taxa no final de cada barra para facilitar a leitura
for index, row in top_20_municipios.iloc[::-1].reset_index().iterrows():
    plt.text(row['taxa_por_10k_hab'], index, f" {row['taxa_por_10k_hab']:.2f}", va='center')


plt.tight_layout()

# Salva o gráfico em um arquivo de imagem de alta resolução
nome_arquivo_grafico = 'resultados/graficos/top20_taxa_incidencia.png'
plt.savefig(nome_arquivo_grafico, dpi=300)

print(f"\nGráfico salvo com sucesso como '{nome_arquivo_grafico}'!")