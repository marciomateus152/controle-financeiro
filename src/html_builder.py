import os
from datetime import datetime

def gerar_grafico_svg(categorias_dict, max_width=400):
    if not categorias_dict:
        return "<p>Sem dados para gerar gráfico.</p>"
        
    svg_lines = []
    svg_lines.append(f'<svg width="100%" height="{len(categorias_dict) * 45 + 20}" xmlns="http://www.w3.org/2000/svg">')
    
    max_val = max(categorias_dict.values()) if categorias_dict.values() else 1
    y_pos = 10
    
    for cat, val in categorias_dict.items():
        bar_width = (val / max_val) * max_width if max_val > 0 else 0
        
        svg_lines.append(f'<text x="0" y="{y_pos + 15}" fill="#94a3b8" font-family="sans-serif" font-size="12">{cat}</text>')
        svg_lines.append(f'<rect x="120" y="{y_pos}" width="{bar_width}" height="20" fill="#38bdf8" rx="4" />')
        svg_lines.append(f'<text x="{130 + bar_width}" y="{y_pos + 15}" fill="#f8fafc" font-family="sans-serif" font-size="12">R$ {val:,.2f}</text>')
        
        y_pos += 40
        
    svg_lines.append('</svg>')
    return "\n".join(svg_lines)

def compilar_html(entradas, saidas, saldo, reg_sucesso, reg_falha, categorias, output_dir):
    data_gen = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cor_saldo = "#10b981" if saldo >= 0 else "#ef4444"
    
    grafico_svg = gerar_grafico_svg(categorias)
    
    tabela = ""
    for cat, val in sorted(categorias.items(), key=lambda x: x, reverse=True):
        tabela += f"<tr><td>{cat}</td><td>R$ {val:,.2f}</td></tr>"

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>FinDash Pro - Relatório Analítico</title>
        <style>
            :root {{ --bg: #0f172a; --panel: #1e293b; --text: #f8fafc; --muted: #94a3b8; --accent: #38bdf8; --success: #10b981; --danger: #ef4444; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 1000px; margin: auto; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .header h1 {{ color: var(--accent); margin: 0 0 10px 0; font-size: 2.5em; letter-spacing: 1px; }}
            .header p {{ color: var(--muted); margin: 0; font-size: 1.1em; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }}
            .card {{ background: var(--panel); padding: 25px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); position: relative; overflow: hidden; }}
            .card::before {{ content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: var(--accent); }}
            .card.success::before {{ background: var(--success); }}
            .card.danger::before {{ background: var(--danger); }}
            .card h3 {{ margin: 0 0 15px 0; font-size: 0.9em; text-transform: uppercase; color: var(--muted); letter-spacing: 1px; }}
            .card .value {{ font-size: 2em; font-weight: bold; margin: 0; }}
            .content-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
            .panel {{ background: var(--panel); padding: 30px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }}
            .panel h2 {{ color: var(--accent); margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 15px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #334155; }}
            th {{ font-weight: 600; color: var(--muted); text-transform: uppercase; font-size: 0.85em; }}
            .stats {{ display: flex; justify-content: space-between; background: #0f172a; padding: 15px; border-radius: 8px; margin-top: 20px; }}
            .stats span {{ color: var(--muted); font-size: 0.9em; }}
            .stats strong {{ color: var(--text); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>FinDash Pro Analytics</h1>
                <p>Processamento Automático de Dados Financeiros</p>
                <p style="font-size: 0.9em; margin-top: 10px;">Gerado em: {data_gen}</p>
            </div>
            
            <div class="grid">
                <div class="card success">
                    <h3>Total de Entradas</h3>
                    <p class="value" style="color: var(--success);">R$ {entradas:,.2f}</p>
                </div>
                <div class="card danger">
                    <h3>Total de Saídas</h3>
                    <p class="value" style="color: var(--danger);">R$ {saidas:,.2f}</p>
                </div>
                <div class="card" style="border-top-color: {cor_saldo};">
                    <h3>Saldo Operacional</h3>
                    <p class="value" style="color: {cor_saldo};">R$ {saldo:,.2f}</p>
                </div>
            </div>

            <div class="content-grid">
                <div class="panel">
                    <h2>Distribuição de Despesas</h2>
                    {grafico_svg}
                    
                    <div class="stats">
                        <span>Registros Processados: <strong>{reg_sucesso}</strong></span>
                        <span>Falhas Ignoradas: <strong>{reg_falha}</strong></span>
                    </div>
                </div>
                
                <div class="panel">
                    <h2>Detalhamento por Categoria</h2>
                    <table>
                        <tr><th>Categoria</th><th>Volume Total</th></tr>
                        {tabela}
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    filename = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        
    return os.path.abspath(filepath)