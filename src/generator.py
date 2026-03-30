import os
import csv
import random
from datetime import datetime, timedelta

def gerar_lote(log_callback):
    os.makedirs("data/input", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)
    os.makedirs("data/archive", exist_ok=True)
    os.makedirs("data/errors", exist_ok=True)
    
    categorias_saida = ["Infraestrutura", "Marketing", "Folha de Pagamento", "Impostos", "Licencas de Software"]
    categorias_entrada = ["Venda de Licencas", "Consultoria", "Suporte Tecnico"]
    
    dados = []
    data_base = datetime.now()
    qtd_registros = random.randint(300, 800)
    
    log_callback(f"Iniciando geracao de {qtd_registros} registros sinteticos...")
    
    for i in range(1, qtd_registros + 1):
        tipo = random.choices(["Entrada", "Saida"], weights=[0.3, 0.7])
        categoria = random.choice(categorias_entrada) if tipo == "Entrada" else random.choice(categorias_saida)
        
        valor = round(random.uniform(1000.0, 15000.0) if tipo == "Entrada" else random.uniform(100.0, 3000.0), 2)
        
        if random.random() < 0.05:
            valor = "VALOR_INVALIDO"
            
        data_txn = (data_base - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d")
        status = random.choices(["Processado", "Rejeitado", "Pendente"], weights=[0.85, 0.10, 0.05])
        
        if random.random() < 0.02:
            dados.append({"id_transacao": f"TXN{i:05d}", "data": data_txn})
            continue
            
        dados.append({
            "id_transacao": f"TXN{i:05d}",
            "data": data_txn,
            "categoria": categoria,
            "tipo": tipo,
            "valor": valor,
            "status": status
        })
        
    nome_arquivo = f"data/input/batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id_transacao", "data", "categoria", "tipo", "valor", "status"])
        writer.writeheader()
        writer.writerows(dados)
        
    log_callback(f"Arquivo gerado com sucesso: {os.path.basename(nome_arquivo)}")
    return True