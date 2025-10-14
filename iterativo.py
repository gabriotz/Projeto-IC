import pandas as pd
import matplotlib.pyplot as plt
import numpy as np # Import numpy no início do script

# --- Carregamento e Limpeza (sem alterações) ---
caminho_do_arquivo = 'dados/sinannet_cnv_zikape144309150_161_2_202.csv'
df = pd.read_csv(
    caminho_do_arquivo, delimiter=';', encoding='latin1',
    skiprows=3, skipfooter=11, engine='python'
)
df = df.iloc[:-1].copy()

temp_split = df['Município de residência'].str.split(' ', n=1, expand=True)
df['municipio_nome'] = temp_split[1]
df.drop(columns=['Município de residência', 'Total'], inplace=True)

colunas_para_converter = df.columns.drop('municipio_nome')

for coluna in colunas_para_converter:
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

df.fillna(0, inplace=True)

for coluna in colunas_para_converter:
    df[coluna] = df[coluna].astype(int)
# --- Fim da Limpeza ---

print("Iniciando o menu de analise")
print("Qual municipio você deseja ver os dados?")
municipioEscolhido = input().strip().upper()

dados_do_municipio = df[df['municio_nome'] == municipioEscolhido]

if not dados_do_municipio.empty:
    print(f"\nExibindo dados para: {municipioEscolhido}")

    casos_Totais = dados_do_municipio[colunas_para_converter].sum(axis=1).sum()
    print(f"Total de casos registrados (todos os anos): {casos_Totais}")

    # --- CORREÇÃO APLICADA AQUI ---
    # Adicionamos 'col.isdigit()' para garantir que só vamos tentar converter colunas
    # que são compostas apenas por números. Isso irá ignorar a coluna '<1975'.
    colunas_anos_filtrados = [col for col in colunas_para_converter if col.isdigit() and int(col) >= 2015]
    
    # O resto do código continua como antes...
    dados_filtrados = dados_do_municipio[colunas_anos_filtrados]
    valores_casos_por_ano = dados_filtrados.values[0]
    
    media_anual = np.mean(valores_casos_por_ano)
    mediana_anual = np.median(valores_casos_por_ano)
    desvio_padrao = np.std(valores_casos_por_ano)
    max_casos_ano = np.max(valores_casos_por_ano)
    min_casos_ano = np.min(valores_casos_por_ano)
    
    print("\n--- Estatísticas Anuais (a partir de 2015) ---")
    print(f"Média de casos por ano: {media_anual:.2f}")
    print(f"Mediana de casos por ano: {mediana_anual:.2f}")
    print(f"Maior nº de casos em um único ano: {max_casos_ano}")
    print(f"Menor nº de casos em um único ano: {min_casos_ano}")
    print(f"Desvio Padrão: {desvio_padrao:.2f}")
    print("---------------------------------------------")

    # --- Parte do Gráfico ---
    dados_grafico = dados_do_municipio[colunas_para_converter].melt(var_name='Ano', value_name='Casos')
    dados_grafico = dados_grafico[dados_grafico['Casos'] > 0]

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    fig.suptitle(f'Análise de Casos de SCZ em {municipioEscolhido}', fontsize=16, weight='bold')

    ax.bar(dados_grafico['Ano'], dados_grafico['Casos'], color='darkcyan')
    
    ax.set_xlabel('Ano do Primeiro Sintoma', fontsize=12)
    ax.set_ylabel('Número de Casos', fontsize=12)
    plt.xticks(rotation=45)

    ax.text(0.05, 0.95, f'Total de Casos (todos os anos): {casos_Totais}',
            transform=ax.transAxes, fontsize=14, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

else:
    print(f"\nO município '{municipioEscolhido}' não foi encontrado. Tente digitar o nome completo e sem acentos.")