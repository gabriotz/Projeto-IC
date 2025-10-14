import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os

print("Iniciando o script de análise...")

# ===================================================================
# PARTE 1: CARREGAR E LIMPAR OS DADOS (Já funcional)
# ===================================================================

try:
    caminho_do_arquivo = 'dados/sinannet_cnv_zikape144309150_161_2_202.csv'
    df = pd.read_csv(
        caminho_do_arquivo, delimiter=';', encoding='latin1', 
        skiprows=3, skipfooter=11, engine='python'
    )
    df = df.iloc[:-1].copy()
    temp_split = df['Município de residência'].str.split(' ', n=1, expand=True)
    df['codigo_ibge'] = temp_split[0]
    df['municipio_nome'] = temp_split[1]
    df.drop(columns=['Município de residência', 'Total'], inplace=True)
    colunas_anos = df.columns.drop(['codigo_ibge', 'municipio_nome'])
    for coluna in colunas_anos:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
    df.fillna(0, inplace=True)
    for coluna in colunas_anos:
        df[coluna] = df[coluna].astype(int)
    print("Dados carregados e limpos com sucesso.")

except FileNotFoundError:
    print(f"ERRO CRÍTICO: O arquivo de dados '{caminho_do_arquivo}' não foi encontrado.")
    exit()
except Exception as e:
    print(f"Ocorreu um erro inesperado ao carregar os dados: {e}")
    exit()


# ===================================================================
# PARTE 2: ANÁLISE TEMPORAL (Já funcional)
# ===================================================================
print("\nIniciando a análise temporal...")
colunas_de_anos = [col for col in df.columns if col.isdigit()]

# 2. Converte essas colunas para tipo numérico
colunas_de_anos_numericas = pd.to_numeric(colunas_de_anos)

# 3. Seleciona apenas as colunas cujo ano é 2015 ou maior
anos_para_plotar = [str(ano) for ano in colunas_de_anos_numericas if ano >= 2015]

# 4. Calcula a soma dos casos usando APENAS a lista de anos correta
casos_por_ano = df[anos_para_plotar].sum()

plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(12, 7))
sns.barplot(x=casos_por_ano.index, y=casos_por_ano.values, hue=casos_por_ano.index, palette="mako", legend=False)
plt.title('Casos Confirmados de SCZ em Pernambuco por Ano (2015-2025)', fontsize=16, pad=20)
plt.xlabel('Ano do Primeiro Sintoma', fontsize=12)
plt.ylabel('Número de Casos Confirmados', fontsize=12)
plt.xticks(rotation=45, ha="right")
for index, value in enumerate(casos_por_ano):
    plt.text(index, value + 50, str(value), ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('grafico_casos_por_ano.png', dpi=300)
print("Análise Temporal Concluída. Gráfico salvo como 'grafico_casos_por_ano.png'")


# ===================================================================
# PARTE 3: ANÁLISE ESPACIAL (COM MAPA GRANDE E NOMES DAS CIDADES)
# ===================================================================
print("\nIniciando a análise espacial...")

df_mapa = df.groupby(['codigo_ibge', 'municipio_nome'])[colunas_anos].sum().sum(axis=1).reset_index(name='total_casos')
caminho_shapefile = 'dados/PE_Municipios_2024.shp'

try:
    mapa_pe = gpd.read_file(caminho_shapefile)
    df_mapa['codigo_ibge'] = df_mapa['codigo_ibge'].astype(str).str.strip()
    mapa_pe['CD_MUN'] = mapa_pe['CD_MUN'].astype(str).str.strip().str[:6]
    mapa_final = mapa_pe.merge(df_mapa, left_on='CD_MUN', right_on='codigo_ibge')
    
    if not mapa_final.empty:
        print("SUCESSO! A junção foi bem-sucedida. Gerando o mapa aprimorado...")
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 7)) # Aumentei ainda mais o tamanho
        
        mapa_final.plot(
            column='total_casos', cmap='Reds', linewidth=0.5, 
            ax=ax, edgecolor='0.8', legend=True,
            legend_kwds={
                'label': "Total de Casos Confirmados de SCZ (2015-2025)",
                'orientation': "horizontal",
                'shrink': 0.6, 'pad': 0.01
            }
        )
        ax.set_title('Distribuição Espacial de Casos de SCZ em Pernambuco', fontdict={'fontsize': '22', 'fontweight': '3'})
        ax.set_axis_off()

        # --- INÍCIO DA NOVA PARTE: ADICIONAR NOMES DAS CIDADES ---
        
        # 1. Defina o ponto de corte: mostrar nome de cidades com mais de X casos
        ponto_de_corte = 500 # Você pode ajustar este número!
        
        # 2. Filtra o dataframe para pegar apenas as cidades acima do corte
        cidades_para_rotular = mapa_final[mapa_final['total_casos'] > ponto_de_corte]
        
        # 3. Adiciona os nomes ao mapa
        for idx, row in cidades_para_rotular.iterrows():
            # Pega o ponto central do município para posicionar o texto
            ponto = row['geometry'].representative_point()
            plt.text(
                ponto.x, 
                ponto.y, 
                row['municipio_nome'], 
                fontsize=9, 
                fontweight='bold',
                ha='center', # Alinhamento horizontal
                color='white', # Cor do texto
                bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.2', edgecolor='none') # Sombra para legibilidade
            )
        
        plt.figtext(
            0.5, # Posição horizontal (0.5 = centro)
            0.10, # Posição vertical (0.15 = perto da base)
            f'Nota: Municípios com mais de {ponto_de_corte} casos confirmados estão rotulados.',
            ha='center', # Alinhamento horizontal do texto
            fontsize=12,
            style='italic',
            bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.5', edgecolor='grey')
        )

        plt.savefig('mapa_distribuicao_casos_com_nomes.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
        print("Análise Espacial Concluída. Mapa aprimorado salvo como 'mapa_distribuicao_casos_com_nomes.png'")
        plt.show()

except FileNotFoundError:
    print(f"\nERRO CRÍTICO: O arquivo do mapa '{caminho_shapefile}' não foi encontrado.")
except Exception as e:
    print(f"\nOcorreu um erro inesperado na análise espacial: {e}")


