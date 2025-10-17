import os
import shutil
import glob
from datetime import datetime

def organizar_projeto_definitivo():
    print("=== ORGANIZAÇÃO DEFINITIVA DO PROJETO ===\n")
    
    # --- 1. BACKUP DE SEGURANÇA ---
    print("📦 FAZENDO BACKUP DE SEGURANÇA...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_antes_organizar_{timestamp}"
    
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copiar apenas arquivos importantes para backup
    extensoes_backup = ['.py', '.csv', '.png', '.md', '.txt']
    for arquivo in os.listdir('.'):
        if os.path.isfile(arquivo) and any(arquivo.endswith(ext) for ext in extensoes_backup):
            shutil.copy2(arquivo, os.path.join(backup_dir, arquivo))
            print(f"   ✅ Backup: {arquivo}")
    
    print(f"   📁 Backup completo em: {backup_dir}/")
    
    # --- 2. CRIAR ESTRUTURA ORGANIZADA ---
    print("\n📂 CRIANDO ESTRUTURA DE PASTAS...")
    
    diretorios = [
        'scripts',
        'dados/brutos',
        'dados/processados',
        'resultados/graficos',
        'resultados/mapas', 
        'resultados/tabelas',
        'docs'
    ]
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
        print(f"   ✅ Criado: {diretorio}/")
    
    # --- 3. MAPEAMENTO INTELIGENTE DOS ARQUIVOS ---
    
    # SCRIPTS PYTHON - MOVER
    scripts_map = {
        'teste.py': 'scripts/01_coleta_dados.py',
        'analise_proporcional.py': 'scripts/02_calcular_taxas.py', 
        'analise_agua.py': 'scripts/03_analise_correlacao.py',
        'gerar_grafico_procional.py': 'scripts/04_gerar_graficos.py',
        'iterativo.py': 'scripts/05_analise_interativa.py'
    }
    
    # DADOS BRUTOS - MOVER para dados/brutos
    dados_brutos_map = {
        'sinannet_cnv_zikape144309150_161_2_202.csv': 'dados/brutos/casos_zika_pe.csv',
        '481e7096a0820255f086359f3ad45518.csv': 'dados/brutos/dados_ibge.csv',
        'Desagregado-20251017164220.csv': 'dados/brutos/snis_saneamento.csv',
        'PE_Municipios_2024.shp': 'dados/brutos/mapa_pe.shp'
    }
    
    # DADOS PROCESSADOS - MOVER
    dados_processados_map = {
        'dados_zika_proporcional_pe.csv': 'dados/processados/taxas_proporcionais.csv',
        'dados_completos_pernambuco.csv': 'dados/processados/dados_completos_analise.csv'
    }
    
    # GRÁFICOS - MOVER
    graficos_map = {
        'heatmap_correlacao_2015_2024.png': 'resultados/graficos/heatmap_correlacao_zika.png',
        'heatmap_correlacao_final.png': 'resultados/graficos/heatmap_correlacao_completo.png',
        'zika_vs_idhm_2015_2024.png': 'resultados/graficos/dispersao_zika_idhm.png',
        'zika_vs_idhm.png': 'resultados/graficos/dispersao_zika_idhm_original.png', 
        'zika_vs_pib.png': 'resultados/graficos/dispersao_zika_pib.png',
        'grafico_casos_por_ano.png': 'resultados/graficos/evolucao_temporal_casos.png',
        'grafico_taxa_proporcional_top20.png': 'resultados/graficos/top20_taxa_incidencia.png'
    }
    
    # MAPAS - MOVER
    mapas_map = {
        'mapa_distribuicao_casos_com_nomes.png': 'resultados/mapas/mapa_distribuicao_casos.png'
    }
    
    # --- 4. EXECUTAR A ORGANIZAÇÃO ---
    
    # Mover scripts
    print("\n🐍 ORGANIZANDO SCRIPTS PYTHON...")
    for orig, dest in scripts_map.items():
        if os.path.exists(orig):
            shutil.move(orig, dest)
            print(f"   ✅ {orig:.<25} → {dest}")
        else:
            print(f"   ⚠️  {orig:.<25} não encontrado")
    
    # Mover dados brutos (usando pattern matching)
    print("\n📁 ORGANIZANDO DADOS BRUTOS...")
    for orig_pattern, dest in dados_brutos_map.items():
        arquivos_encontrados = False
        
        # Primeiro tenta encontrar em subpastas
        for arquivo in glob.glob('**/' + orig_pattern, recursive=True):
            if os.path.isfile(arquivo):
                # Se está em subpasta, mover para dados/brutos mantendo nome original
                nome_arquivo = os.path.basename(arquivo)
                novo_dest = os.path.join('dados/brutos', nome_arquivo)
                shutil.move(arquivo, novo_dest)
                print(f"   ✅ {arquivo:.<25} → {novo_dest}")
                arquivos_encontrados = True
        
        # Se não encontrou em subpastas, tenta no diretório atual
        if not arquivos_encontrados and os.path.exists(orig_pattern):
            shutil.move(orig_pattern, os.path.join('dados/brutos', os.path.basename(orig_pattern)))
            print(f"   ✅ {orig_pattern:.<25} → dados/brutos/{os.path.basename(orig_pattern)}")
    
    # Mover dados processados
    print("\n📊 ORGANIZANDO DADOS PROCESSADOS...")
    for orig, dest in dados_processados_map.items():
        if os.path.exists(orig):
            shutil.move(orig, dest)
            print(f"   ✅ {orig:.<25} → {dest}")
    
    # Mover gráficos
    print("\n📈 ORGANIZANDO GRÁFICOS...")
    for orig, dest in graficos_map.items():
        if os.path.exists(orig):
            shutil.move(orig, dest)
            print(f"   ✅ {orig:.<25} → {dest}")
    
    # Mover mapas
    print("\n🗺️  ORGANIZANDO MAPAS...")
    for orig_pattern, dest in mapas_map.items():
        for arquivo in glob.glob(orig_pattern + '*'):
            if os.path.exists(arquivo):
                shutil.move(arquivo, dest)
                print(f"   ✅ {arquivo:.<25} → {dest}")
    
    # --- 5. ATUALIZAR README ---
    print("\n📝 ATUALIZANDO DOCUMENTAÇÃO...")
    
organizar_projeto_definitivo()