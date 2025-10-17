import pandas as pd
import numpy as np

# --- 1. CARREGAR E LIMPAR DADOS DE ZIKA (sem alterações) ---
print("Carregando e limpando dados de casos de Zika...")
try:
    caminho_zika = 'dados/sinannet_cnv_zikape144309150_161_2_202.csv'
    df_zika = pd.read_csv(
        caminho_zika, delimiter=';', encoding='latin1',
        skiprows=3, skipfooter=11, engine='python'
    )
    df_zika = df_zika.iloc[:-1].copy()
    temp_split = df_zika['Município de residência'].str.split(' ', n=1, expand=True)
    df_zika['codigo_ibge'] = temp_split[0]
    df_zika['municipio_nome'] = temp_split[1]
    df_zika.drop(columns=['Município de residência', 'Total'], inplace=True)
    colunas_anos = df_zika.columns.drop(['codigo_ibge', 'municipio_nome'])
    for coluna in colunas_anos:
        df_zika[coluna] = pd.to_numeric(df_zika[coluna], errors='coerce')
    df_zika.fillna(0, inplace=True)
    for coluna in colunas_anos:
        df_zika[coluna] = df_zika[coluna].astype(int)
except FileNotFoundError:
    print(f"ERRO: O arquivo de dados de Zika não foi encontrado. Verifique o caminho: '{caminho_zika}'")
    exit()

# --- 2. CARREGAR E LIMPAR DADOS DE POPULAÇÃO ---
print("Carregando e limpando dados de população do IBGE...")
try:
    caminho_populacao = 'dados/481e7096a0820255f086359f3ad45518.csv'
    df_pop = pd.read_csv(caminho_populacao, encoding='latin1', skiprows=1)

    df_pop = df_pop[['C&oacute;digo [-]', 'Popula&ccedil;&atilde;o no &uacute;ltimo censo - pessoas [2022]']].copy()
    df_pop.rename(columns={
        'C&oacute;digo [-]': 'codigo_ibge_7',
        'Popula&ccedil;&atilde;o no &uacute;ltimo censo - pessoas [2022]': 'populacao_2022'
    }, inplace=True)

    # --- CORREÇÃO APLICADA AQUI ---
    # 1. Tenta converter a coluna para numérico. Onde houver texto (rodapé), vira NaN.
    df_pop['populacao_2022'] = pd.to_numeric(df_pop['populacao_2022'], errors='coerce')

    # 2. Remove todas as linhas que agora contêm NaN (ou seja, o rodapé).
    df_pop.dropna(inplace=True)

    # 3. Agora que só temos números, podemos converter para inteiro com segurança.
    df_pop['populacao_2022'] = df_pop['populacao_2022'].astype(int)
    df_pop['codigo_ibge_7'] = df_pop['codigo_ibge_7'].astype(int)
    df_pop['codigo_ibge'] = df_pop['codigo_ibge_7'].astype(str).str[:6]

except FileNotFoundError:
    print(f"ERRO: O arquivo de dados de população não foi encontrado. Verifique o caminho: '{caminho_populacao}'")
    exit()

# --- O RESTO DO SCRIPT CONTINUA IGUAL ---
print("Juntando os dados de casos e população...")
df_completo = pd.merge(df_zika, df_pop[['codigo_ibge', 'populacao_2022']], on='codigo_ibge', how='left')
df_completo.dropna(subset=['populacao_2022'], inplace=True)

print("Calculando o total de casos no período 2015-2024...")
colunas_periodo = [col for col in colunas_anos if col.isdigit() and 2015 <= int(col) <= 2024]
df_completo['total_casos_periodo'] = df_completo[colunas_periodo].sum(axis=1)

print("Calculando a taxa proporcional por 10.000 habitantes...")
df_completo.loc[df_completo['populacao_2022'] > 0, 'taxa_por_10k_hab'] = \
    (df_completo['total_casos_periodo'] / df_completo['populacao_2022']) * 10000
df_completo['taxa_por_10k_hab'].fillna(0, inplace=True)

print("\nAnálise concluída! Amostra dos dados com a nova coluna:")
print(df_completo[['municipio_nome', 'populacao_2022', 'total_casos_periodo', 'taxa_por_10k_hab']].sort_values(by='taxa_por_10k_hab', ascending=False).head(10))

nome_arquivo_saida = 'dados_zika_proporcional_pe.csv'
df_completo.to_csv(nome_arquivo_saida, index=False, encoding='utf-8')
print(f"\nResultado completo salvo com sucesso em: '{nome_arquivo_saida}'")