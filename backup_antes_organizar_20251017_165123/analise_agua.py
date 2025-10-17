import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("=== ANÁLISE DE DADOS - VERSÃO DEFINITIVA ===\n")

# --- 1. CARREGAR OS DADOS EXISTENTES ---
print("1. Carregando dados proporcionais e do IBGE...")
try:
    df_proporcional = pd.read_csv('dados_zika_proporcional_pe.csv')
    df_ibge_raw = pd.read_csv('dados/481e7096a0820255f086359f3ad45518.csv', encoding='latin1', skiprows=1)
    print(f"   ✅ Dados proporcionais: {df_proporcional.shape}")
    print(f"   ✅ Dados IBGE: {df_ibge_raw.shape}")
    
    # Mostrar colunas do IBGE para debug
    print(f"   Colunas IBGE: {df_ibge_raw.columns.tolist()}")
    
except FileNotFoundError as e:
    print(f"❌ ERRO: {e}")
    exit()



# --- 2. PREPARAR DADOS SOCIOECONÔMICOS (IBGE) - VERSÃO SIMPLIFICADA ---
print("\n2. Preparando dados socioeconômicos do IBGE...")

# VERDADEIRA SOLUÇÃO: Usar os nomes exatos das colunas que apareceram no debug
df_socio = df_ibge_raw[[
    'C&oacute;digo [-]', 
    'IDHM &lt;span&gt;&Iacute;ndice de desenvolvimento humano municipal&lt;/span&gt; [2010]',
    'PIB per capita - R$ [2021]'
]].copy()

# Renomear para nomes simples
df_socio.rename(columns={
    'C&oacute;digo [-]': 'codigo_ibge_7',
    'IDHM &lt;span&gt;&Iacute;ndice de desenvolvimento humano municipal&lt;/span&gt; [2010]': 'idhm_2010',
    'PIB per capita - R$ [2021]': 'pib_per_capita'
}, inplace=True)

print(f"   Dados socioeconômicos brutos: {df_socio.shape}")

# Converter para numérico
df_socio['idhm_2010'] = pd.to_numeric(df_socio['idhm_2010'], errors='coerce')
df_socio['pib_per_capita'] = pd.to_numeric(df_socio['pib_per_capita'], errors='coerce')

# Criar código IBGE de 6 dígitos
df_socio['codigo_ibge'] = df_socio['codigo_ibge_7'].astype(str).str[:6]

# Remover linhas com valores nulos
df_socio = df_socio.dropna(subset=['idhm_2010', 'pib_per_capita'])
print(f"   ✅ Dados socioeconômicos válidos: {df_socio.shape[0]} municípios")

# --- CORREÇÃO DO MERGE --- 
print("\n📋 Verificando e corrigindo tipos de dados para o merge...")

# Verificar tipos atuais
print(f"   Tipo de 'codigo_ibge' em df_proporcional: {df_proporcional['codigo_ibge'].dtype}")
print(f"   Tipo de 'codigo_ibge' em df_socio: {df_socio['codigo_ibge'].dtype}")

# Converter AMBOS para string para garantir compatibilidade
df_proporcional['codigo_ibge'] = df_proporcional['codigo_ibge'].astype(str)
df_socio['codigo_ibge'] = df_socio['codigo_ibge'].astype(str)

print("   ✅ Ambos convertidos para string")

# Verificar alguns valores para debug
print(f"   Exemplo de códigos em df_proporcional: {df_proporcional['codigo_ibge'].head(3).tolist()}")
print(f"   Exemplo de códigos em df_socio: {df_socio['codigo_ibge'].head(3).tolist()}")

# --- 3. JUNTAR DADOS PROPORCIONAIS COM SOCIOECONÔMICOS ---
print("\n3. Unindo dados de Zika com dados socioeconômicos...")

# Fazer o merge
df_final = pd.merge(
    df_proporcional, 
    df_socio[['codigo_ibge', 'idhm_2010', 'pib_per_capita']], 
    on='codigo_ibge', 
    how='inner'  # Usar apenas municípios que existem em ambos
)

print(f"   ✅ Merge concluído: {df_final.shape[0]} municípios")

# --- 4. TENTAR ADICIONAR DADOS DE SANEAMENTO (OPCIONAL) ---
print("\n4. Tentando adicionar dados de saneamento...")

try:
    caminho_snis = 'dados/Desagregado-20251017164220.csv'
    
    if os.path.exists(caminho_snis):
        # Carregar SNIS
        df_snis_raw = pd.read_csv(caminho_snis, delimiter=';', encoding='utf-16-le')
        print(f"   ✅ SNIS carregado: {df_snis_raw.shape}")
        
        # Verificar estrutura do SNIS
        print(f"   Colunas SNIS: {df_snis_raw.columns.tolist()[:5]}...")  # Primeiras 5 colunas
        
        # Tentar encontrar dados úteis - usar uma abordagem diferente
        # Vamos pegar todos os dados disponíveis e depois filtrar
        colunas_interesse = ['Código do Município', 'IN015 - Índice de coleta de esgoto', 'IN016 - Índice de tratamento de esgoto']
        
        if all(col in df_snis_raw.columns for col in colunas_interesse):
            # Selecionar colunas de interesse
            df_snis = df_snis_raw[colunas_interesse].copy()
            
            # Renomear
            df_snis.rename(columns={
                'Código do Município': 'codigo_ibge',
                'IN015 - Índice de coleta de esgoto': 'indice_coleta_esgoto',
                'IN016 - Índice de tratamento de esgoto': 'indice_tratamento_esgoto'
            }, inplace=True)
            
            # Converter dados
            for col in ['indice_coleta_esgoto', 'indice_tratamento_esgoto']:
                if df_snis[col].dtype == 'object':
                    df_snis[col] = df_snis[col].str.replace(',', '.', regex=False)
                df_snis[col] = pd.to_numeric(df_snis[col], errors='coerce')
            
            # Converter código IBGE
            df_snis['codigo_ibge'] = df_snis['codigo_ibge'].astype(str)
            
            # Remover totalmente nulos
            df_snis = df_snis.dropna(subset=['indice_coleta_esgoto', 'indice_tratamento_esgoto'], how='all')
            
            print(f"   📊 Dados de saneamento disponíveis: {df_snis.shape[0]} registros")
            
            # Fazer merge com dados finais
            if df_snis.shape[0] > 0:
                df_final = pd.merge(df_final, df_snis, on='codigo_ibge', how='left')
                print(f"   ✅ Dados de saneamento adicionados: {df_final['indice_coleta_esgoto'].notna().sum()} municípios")
            else:
                print("   ⚠️  Nenhum dado de saneamento válido encontrado")
                df_final['indice_coleta_esgoto'] = None
                df_final['indice_tratamento_esgoto'] = None
        else:
            print("   ⚠️  Colunas de saneamento não encontradas no SNIS")
            df_final['indice_coleta_esgoto'] = None
            df_final['indice_tratamento_esgoto'] = None
            
except Exception as e:
    print(f"   ⚠️  Erro ao processar saneamento: {e}")
    df_final['indice_coleta_esgoto'] = None
    df_final['indice_tratamento_esgoto'] = None

# --- 5. ANÁLISE ESTATÍSTICA ---
print(f"\n5. ANÁLISE FINAL - {df_final.shape[0]} MUNICÍPIOS DE PERNAMBUCO")

# Estatísticas básicas
print("\n📊 ESTATÍSTICAS BÁSICAS:")
print(f"   - Taxa média de Zika: {df_final['taxa_por_10k_hab'].mean():.2f} por 10k hab")
print(f"   - IDHM médio: {df_final['idhm_2010'].mean():.3f}")
print(f"   - PIB per capita médio: R$ {df_final['pib_per_capita'].mean():.2f}")

if 'indice_coleta_esgoto' in df_final.columns and df_final['indice_coleta_esgoto'].notna().sum() > 0:
    print(f"   - Coleta de esgoto (média): {df_final['indice_coleta_esgoto'].mean():.1f}%")
if 'indice_tratamento_esgoto' in df_final.columns and df_final['indice_tratamento_esgoto'].notna().sum() > 0:
    print(f"   - Tratamento de esgoto (média): {df_final['indice_tratamento_esgoto'].mean():.1f}%")

# --- 6. CORRELAÇÕES ---
print("\n6. CALCULANDO CORRELAÇÕES...")

# Selecionar colunas para correlação
colunas_corr = ['taxa_por_10k_hab', 'idhm_2010', 'pib_per_capita']

# Adicionar saneamento se tiver dados
if 'indice_coleta_esgoto' in df_final.columns and df_final['indice_coleta_esgoto'].notna().sum() >= 5:
    colunas_corr.append('indice_coleta_esgoto')
if 'indice_tratamento_esgoto' in df_final.columns and df_final['indice_tratamento_esgoto'].notna().sum() >= 5:
    colunas_corr.append('indice_tratamento_esgoto')

print(f"   Variáveis analisadas: {colunas_corr}")

# Calcular correlação
df_corr = df_final[colunas_corr].dropna()

if df_corr.shape[0] >= 5:
    matriz_corr = df_corr.corr()
    
    print(f"\n📈 MATRIZ DE CORRELAÇÃO:")
    print(matriz_corr.round(3))
    
    # --- GERAR HEATMAP ---
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz_corr, 
                annot=True, 
                cmap='coolwarm', 
                fmt=".2f", 
                linewidths=.5,
                center=0,
                square=True,
                cbar_kws={"shrink": .8})
    
    plt.title('Correlação entre Zika, Desenvolvimento e Saneamento em PE', 
              fontsize=14, pad=20, weight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # Salvar
    plt.savefig('heatmap_correlacao_final.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Heatmap salvo: 'heatmap_correlacao_final.png'")
    
else:
    print("   ❌ Dados insuficientes para correlação")

# --- 7. SALVAR DADOS COMPLETOS ---
print("\n7. Salvando dados completos...")
df_final.to_csv('dados_completos_pernambuco.csv', index=False)
print(f"✅ Dados salvos: 'dados_completos_pernambuco.csv'")

# --- 8. GRÁFICOS ADICIONAIS ---
print("\n8. Gerando gráficos adicionais...")

# Gráfico 1: Zika vs IDHM
plt.figure(figsize=(10, 6))
plt.scatter(df_final['idhm_2010'], df_final['taxa_por_10k_hab'], alpha=0.6, s=50)
plt.xlabel('IDHM 2010')
plt.ylabel('Taxa de Zika (por 10k hab)')
plt.title('Relação entre Desenvolvimento Humano e Zika em PE')
plt.grid(True, alpha=0.3)
plt.savefig('zika_vs_idhm.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: 'zika_vs_idhm.png'")

# Gráfico 2: Zika vs PIB
plt.figure(figsize=(10, 6))
plt.scatter(df_final['pib_per_capita'], df_final['taxa_por_10k_hab'], alpha=0.6, s=50, color='green')
plt.xlabel('PIB per Capita (R$) anual')
plt.ylabel('Taxa de Zika (por 10k hab)')
plt.title('Relação entre Renda e Zika em PE')
plt.grid(True, alpha=0.3)
plt.savefig('zika_vs_pib.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: 'zika_vs_pib.png'")

print(f"\n🎉 ANÁLISE CONCLUÍDA COM SUCESSO!")
print(f"📊 {df_final.shape[0]} municípios de Pernambuco analisados")
print(f"📁 Arquivos gerados:")
print(f"   - heatmap_correlacao_final.png")
print(f"   - zika_vs_idhm.png") 
print(f"   - zika_vs_pib.png")
print(f"   - dados_completos_pernambuco.csv")

if pib_stats['mean'] > 100000:
    print("   ⚠️  VALORES SUSPEITOS: PIB per capita muito alto!")
    print("   💡 Possível problema: Dados em milhares/milhões")
    print("   🔧 Aplicando correção: dividindo por 1000...")
    df_final['pib_per_capita_corrigido'] = df_final['pib_per_capita'] / 1000
    usar_pib_corrigido = True
elif pib_stats['mean'] < 5000:
    print("   ⚠️  VALORES SUSPEITOS: PIB per capita muito baixo!")
    print("   💡 Possível problema: Dados incompletos ou errados")
    usar_pib_corrigido = False
else:
    print("   ✅ Valores dentro do esperado para PIB per capita municipal")
    usar_pib_corrigido = False

# Verificar outliers
Q1 = df_final['pib_per_capita'].quantile(0.25)
Q3 = df_final['pib_per_capita'].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR

outliers = df_final[df_final['pib_per_capita'] > limite_superior]
if not outliers.empty:
    print(f"   ⚠️  Encontrados {len(outliers)} outliers no PIB per capita")
    print(f"      Limite superior: R$ {limite_superior:,.2f}")
    
    # Mostrar municípios com outliers
    print("      Municípios com PIB muito alto:")
    for _, municipio in outliers.iterrows():
        print(f"        - {municipio['codigo_ibge']}: R$ {municipio['pib_per_capita']:,.2f}")

# --- 6. CORRELAÇÕES (USANDO PIB CORRIGIDO SE NECESSÁRIO) ---
print("\n6. CALCULANDO CORRELAÇÕES (2015-2024)...")

# Decidir qual coluna de PIB usar
if usar_pib_corrigido:
    coluna_pib = 'pib_per_capita_corrigido'
    print("   💡 Usando PIB per capita corrigido (dividido por 1000)")
else:
    coluna_pib = 'pib_per_capita'
    print("   💡 Usando PIB per capita original")

colunas_corr = ['taxa_por_10k_hab', 'idhm_2010', coluna_pib]
df_corr = df_final[colunas_corr].dropna()

if df_corr.shape[0] >= 5:
    matriz_corr = df_corr.corr()
    
    print(f"\n📈 MATRIZ DE CORRELAÇÃO:")
    print(matriz_corr.round(3))
    
    # GERAR HEATMAP
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz_corr, 
                annot=True, 
                cmap='coolwarm', 
                fmt=".2f", 
                linewidths=.5,
                center=0,
                square=True,
                cbar_kws={"shrink": .8})
    
    titulo = 'Correlação: Zika vs Desenvolvimento em PE (2015-2024)'
    if usar_pib_corrigido:
        titulo += ' - PIB corrigido'
    
    plt.title(titulo, fontsize=14, pad=20, weight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    nome_heatmap = 'heatmap_correlacao_2015_2024.png'
    if usar_pib_corrigido:
        nome_heatmap = 'heatmap_correlacao_2015_2024_pib_corrigido.png'
    
    plt.savefig(nome_heatmap, dpi=300, bbox_inches='tight')
    print(f"\n✅ Heatmap salvo: '{nome_heatmap}'")
    
else:
    print("   ❌ Dados insuficientes para correlação")

# --- 7. GRÁFICOS ADICIONAIS ---
print("\n7. Gerando gráficos adicionais...")

# Gráfico 1: Zika vs IDHM
plt.figure(figsize=(10, 6))
plt.scatter(df_final['idhm_2010'], df_final['taxa_por_10k_hab'], alpha=0.6, s=50)
plt.xlabel('IDHM 2010')
plt.ylabel('Taxa de Zika (por 10k hab) - 2015-2024')
plt.title('Relação entre Desenvolvimento Humano e Zika em PE (2015-2024)')
plt.grid(True, alpha=0.3)
plt.savefig('zika_vs_idhm_2015_2024.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: 'zika_vs_idhm_2015_2024.png'")

# Gráfico 2: Zika vs PIB (usando versão corrigida se necessário)
plt.figure(figsize=(10, 6))

if usar_pib_corrigido:
    plt.scatter(df_final[coluna_pib], df_final['taxa_por_10k_hab'], alpha=0.6, s=50, color='green')
    plt.xlabel('PIB per Capita (R$ mil) - CORRIGIDO')
    titulo_pib = 'Relação entre Renda e Zika em PE (2015-2024) - PIB Corrigido'
else:
    plt.scatter(df_final[coluna_pib], df_final['taxa_por_10k_hab'], alpha=0.6, s=50, color='green')
    plt.xlabel('PIB per Capita (R$)')
    titulo_pib = 'Relação entre Renda e Zika em PE (2015-2024)'

plt.ylabel('Taxa de Zika (por 10k hab) - 2015-2024')
plt.title(titulo_pib)
plt.grid(True, alpha=0.3)

nome_pib = 'zika_vs_pib_2015_2024.png'
if usar_pib_corrigido:
    nome_pib = 'zika_vs_pib_2015_2024_corrigido.png'

plt.savefig(nome_pib, dpi=300, bbox_inches='tight')
print(f"✅ Gráfico salvo: '{nome_pib}'")