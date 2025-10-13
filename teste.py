import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Carregar os dados ---
# Substitua 'nome_do_seu_arquivo.csv' pelo nome real do seu arquivo.
caminho_do_arquivo = 'dados/sinannet_cnv_zikape144309150_161_2_202.csv' 

# O engine='python' ajuda a lidar com o skipfooter.
# latin1 é a codificação comum para arquivos do governo brasileiro.
df = pd.read_csv(
    caminho_do_arquivo, 
    delimiter=';', 
    encoding='latin1', 
    skiprows=3,          # Pula as 3 primeiras linhas de cabeçalho
    skipfooter=11,         # Pula as 11 linhas de rodapé
    engine='python'
)

# --- 2. Limpar os dados ---
# O DATASUS coloca um código na frente do nome do município. Vamos remover.
# Também removemos a última linha que é o "Total" geral.
df = df.iloc[:-1].copy() # Pega todas as linhas, menos a última
df['Município'] = df['Município de Residência'].str.split(' ').str[1:].str.join(' ')

# Define a coluna de município como índice (facilita os cálculos)
df.set_index('Município', inplace=True)
df.drop(columns=['Município de Residência', 'Total'], inplace=True) # Remove colunas desnecessárias

# Substitui o hífen '-' por 0 e converte todas as colunas para número
df = df.replace('-', '0')
df = df.astype(int)

# --- 3. Calcular o total de casos por ano ---
casos_por_ano = df.sum()

# --- 4. Criar o gráfico ---
plt.figure(figsize=(12, 7)) # Define o tamanho do gráfico
sns.barplot(x=casos_por_ano.index, y=casos_por_ano.values, palette="viridis")

plt.title('Casos Confirmados de SCZ em Pernambuco (2016-2024)', fontsize=16)
plt.xlabel('Ano de Notificação', fontsize=12)
plt.ylabel('Número de Casos Confirmados', fontsize=12)
plt.xticks(rotation=45) # Gira os rótulos do eixo X para melhor visualização
plt.grid(axis='y', linestyle='--', alpha=0.7) # Adiciona uma grade para facilitar a leitura

# Mostra o gráfico
plt.show()

# Exibe a tabela de totais
print(casos_por_ano)