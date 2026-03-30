import os
import csv
import shutil
from src.html_builder import compilar_html

def executar_pipeline(log_callback):
    dir_in = "data/input"
    dir_out = "data/output"
    dir_arc = "data/archive"
    dir_err = "data/errors"
    
    arquivos = [f for f in os.listdir(dir_in) if f.endswith('.csv')]
    
    if not arquivos:
        log_callback("ERRO: Nenhum arquivo de dados encontrado na pasta input.")
        return False, None
        
    entradas = 0.0
    saidas = 0.0
    resumo_cat = {}
    reg_sucesso = 0
    reg_falha = 0
    
    for arquivo in arquivos:
        caminho_completo = os.path.join(dir_in, arquivo)
        log_callback(f"Processando arquivo: {arquivo}...")
        
        arquivo_tem_erro_critico = False
        
        with open(caminho_completo, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames or 'valor' not in reader.fieldnames:
                log_callback(f"AVISO: Estrutura invalida em {arquivo}.")
                arquivo_tem_erro_critico = True
                continue
                
            for row in reader:
                try:
                    if row.get('status') == 'Processado':
                        valor = float(row['valor'])
                        categoria = row.get('categoria', 'Desconhecida')
                        
                        if row.get('tipo') == 'Entrada':
                            entradas += valor
                        elif row.get('tipo') == 'Saida':
                            saidas += valor
                            resumo_cat[categoria] = resumo_cat.get(categoria, 0.0) + valor
                            
                        reg_sucesso += 1
                    else:
                        reg_falha += 1
                except (ValueError, TypeError):
                    reg_falha += 1
                    
        destino = dir_err if arquivo_tem_erro_critico else dir_arc
        shutil.move(caminho_completo, os.path.join(destino, arquivo))
        log_callback(f"Arquivo movido para: {destino}")
        
    saldo = entradas - saidas
    log_callback(f"Consolidacao concluida: {reg_sucesso} OK | {reg_falha} Falhas.")
    
    log_callback("Gerando dashboard interativo...")
    path_html = compilar_html(entradas, saidas, saldo, reg_sucesso, reg_falha, resumo_cat, dir_out)
    
    return True, path_html