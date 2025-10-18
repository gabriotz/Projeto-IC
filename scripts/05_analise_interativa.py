import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Carregamento e Limpeza (sem alterações) ---
caminho_do_arquivo = 'dados/brutos/sinannet_cnv_zikape144309150_161_2_202.csv'
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

dados_do_municipio = df[df['municipio_nome'] == municipioEscolhido]

if not dados_do_municipio.empty:
    print(f"\nExibindo dados para: {municipioEscolhido}")

    # --- FILTRO PARA 2015-2024 ---
    # Criar lista apenas com colunas de anos entre 2015 e 2024
    colunas_2015_2024 = []
    for col in colunas_para_converter:
        try:
            ano = int(col)
            if 2015 <= ano <= 2024:
                colunas_2015_2024.append(col)
        except ValueError:
            continue  # Ignora colunas que não podem ser convertidas para inteiro
    
    # Calcular totais apenas para o período 2015-2024
    casos_Totais_2015_2024 = dados_do_municipio[colunas_2015_2024].sum(axis=1).sum()
    print(f"Total de casos registrados (2015-2024): {casos_Totais_2015_2024}")

    # Dados filtrados para estatísticas
    dados_filtrados = dados_do_municipio[colunas_2015_2024]
    valores_casos_por_ano = dados_filtrados.values[0]
    
    # Calcular estatísticas
    media_anual = np.mean(valores_casos_por_ano)
    mediana_anual = np.median(valores_casos_por_ano)
    desvio_padrao = np.std(valores_casos_por_ano)
    max_casos_ano = np.max(valores_casos_por_ano)
    min_casos_ano = np.min(valores_casos_por_ano)
    
    print("\n--- Estatísticas Anuais (2015-2024) ---")
    print(f"Média de casos por ano: {media_anual:.2f}")
    print(f"Mediana de casos por ano: {mediana_anual:.2f}")
    print(f"Maior nº de casos em um único ano: {max_casos_ano}")
    print(f"Menor nº de casos em um único ano: {min_casos_ano}")
    print(f"Desvio Padrão: {desvio_padrao:.2f}")
    print("---------------------------------------------")

    # --- Parte do Gráfico (APENAS 2015-2024) ---
    # Filtrar apenas os dados do período desejado para o gráfico
    dados_grafico = dados_do_municipio[colunas_2015_2024].melt(var_name='Ano', value_name='Casos')
    dados_grafico = dados_grafico[dados_grafico['Casos'] > 0]

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 9))
    
    fig.suptitle(f'Análise de Casos de SCZ em {municipioEscolhido} (2015-2024)', fontsize=16, weight='bold')

    # Criar o gráfico de barras
    bars = ax.bar(dados_grafico['Ano'], dados_grafico['Casos'], color='darkcyan', alpha=0.7)
    
    # Adicionar valores em cima das barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Ano do Primeiro Sintoma', fontsize=12)
    ax.set_ylabel('Número de Casos', fontsize=12)
    plt.xticks(rotation=45)

    # Criar string com todas as estatísticas (PERÍODO 2015-2024)
    estatisticas_texto = (
        f'Total de Casos (2015-2024): {casos_Totais_2015_2024}\n'
        f'Média anual: {media_anual:.1f} casos\n'
        f'Mediana anual: {mediana_anual:.1f} casos\n'
        f'Maior valor anual: {max_casos_ano} casos\n'
        f'Menor valor anual: {min_casos_ano} casos\n'
        f'Desvio Padrão: {desvio_padrao:.1f}'
    )

    # Adicionar box de estatísticas no canto superior direito
    ax.text(0.98, 0.95, estatisticas_texto,
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8,
                     edgecolor='navy', linewidth=1))

    # Adicionar linha da média
    if len(dados_grafico) > 0:
        ax.axhline(y=media_anual, color='red', linestyle='--', alpha=0.7, 
                  label=f'Média: {media_anual:.1f}')
        ax.legend(loc='upper left')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

else:
    print(f"\nO município '{municipioEscolhido}' não foi encontrado. Tente digitar o nome completo e sem acentos.")