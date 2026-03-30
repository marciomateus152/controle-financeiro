import tkinter as tk
from tkinter import scrolledtext
import webbrowser
import threading
from src.utils import setup_logger
from src.generator import gerar_lote
from src.etl_engine import executar_pipeline

class FinDashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FinDash Pro - ETL Engine")
        self.root.geometry("850x550")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)
        
        self.logger = setup_logger()
        self.ultimo_html = None
        
        self.construir_interface()
        self.log_gui("Sistema inicializado. Modulos carregados.")

    def construir_interface(self):
        left_panel = tk.Frame(self.root, bg="#1e293b", width=300)
        left_panel.pack(side="left", fill="y", padx=20, pady=20)
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(self.root, bg="#0f172a")
        right_panel.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)
        
        tk.Label(left_panel, text="FinDash Pro", font=("Segoe UI", 24, "bold"), bg="#1e293b", fg="#38bdf8").pack(pady=(20, 5))
        tk.Label(left_panel, text="Data Automation Tool", font=("Segoe UI", 10), bg="#1e293b", fg="#94a3b8").pack(pady=(0, 40))
        
        btn_style = {"font": ("Segoe UI", 11, "bold"), "fg": "#ffffff", "relief": "flat", "cursor": "hand2", "pady": 8}
        
        self.btn_gen = tk.Button(left_panel, text="Gerar Massa de Dados", bg="#3b82f6", activebackground="#2563eb", command=self.thread_gerar, **btn_style)
        self.btn_gen.pack(fill="x", padx=20, pady=10)
        
        self.btn_etl = tk.Button(left_panel, text="Processar Pipeline", bg="#10b981", activebackground="#059669", command=self.thread_etl, **btn_style)
        self.btn_etl.pack(fill="x", padx=20, pady=10)
        
        self.btn_view = tk.Button(left_panel, text="Visualizar Dashboard", bg="#475569", activebackground="#334155", state="disabled", command=self.abrir_relatorio, **btn_style)
        self.btn_view.pack(fill="x", padx=20, pady=10)
        
        tk.Label(right_panel, text="Console de Execução", font=("Segoe UI", 12, "bold"), bg="#0f172a", fg="#f8fafc", anchor="w").pack(fill="x", pady=(0, 10))
        
        self.console = scrolledtext.ScrolledText(right_panel, bg="#020617", fg="#10b981", font=("Consolas", 10), bd=0, padx=10, pady=10)
        self.console.pack(fill="both", expand=True)
        self.console.config(state="disabled")

    def log_gui(self, message):
        self.logger.info(message)
        self.console.config(state="normal")
        self.console.insert(tk.END, f"> {message}\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def thread_gerar(self):
        threading.Thread(target=self._exec_gerar, daemon=True).start()

    def _exec_gerar(self):
        self.mudar_estado_botoes("disabled")
        gerar_lote(self.log_gui)
        self.mudar_estado_botoes("normal")

    def thread_etl(self):
        threading.Thread(target=self._exec_etl, daemon=True).start()

    def _exec_etl(self):
        self.mudar_estado_botoes("disabled")
        self.log_gui("Iniciando rotina de extracao e transformacao...")
        
        sucesso, caminho = executar_pipeline(self.log_gui)
        
        if sucesso:
            self.ultimo_html = caminho
            self.log_gui("Pipeline finalizado. Relatorio disponivel.")
            self.btn_view.config(state="normal", bg="#38bdf8", activebackground="#0284c7")
        
        self.btn_gen.config(state="normal")
        self.btn_etl.config(state="normal")

    def mudar_estado_botoes(self, estado):
        self.btn_gen.config(state=estado)
        self.btn_etl.config(state=estado)

    def abrir_relatorio(self):
        if self.ultimo_html:
            self.log_gui("Abrindo relatorio no navegador padrao...")
            webbrowser.open(f"file://{self.ultimo_html}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinDashApp(root)
    root.mainloop()