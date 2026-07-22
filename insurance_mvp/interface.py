"""
interface.py
------------
Mapeamento da Interface (GUI Tkinter).

  Formulário de Cliente (Inputs)
    - Único campo digitável: Idade
    - Campos selecionáveis: Faixa de Renda, Tipo de Vínculo, Tempo no Emprego,
      Possui Imóvel, Possui Veículo, Histórico de Crédito, Estado Civil,
      Qtd. Filhos, Faixa Etária dos Filhos, Possui Seguro, Qtd. de Seguros Ativos.

  Painel de Ações (Botões de Controle)
    - Gerar Base Sintética / Treinar Modelo / Analisar Cliente /
      Exibir Estatísticas / Limpar Dados
"""

import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gerador_base import (
    gerar_base,
    FAIXAS_RENDA,
    TIPOS_VINCULO,
    HISTORICOS_CREDITO,
    ESTADOS_CIVIS,
    FAIXAS_ETARIAS_FILHOS,
    SIM_NAO,
)
from modelo import ModeloPreditivoSeguros
import estatistica


COR_FUNDO = "#F4F6F8"
COR_TITULO = "#2E75B6"
COR_SECAO = "#E74C3C"
COR_OK = "#1A7A5E"


class AplicacaoSeguros(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MVP de Análise Preditiva para Seguros")
        self.geometry("980x680")
        self.configure(bg=COR_FUNDO)
        self.minsize(900, 620)

        # Estado da aplicação (em memória, sem banco de dados)
        self.base_clientes = []
        self.modelo = ModeloPreditivoSeguros()

        self._construir_layout()

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------
    def _construir_layout(self):
        titulo = tk.Label(
            self,
            text="MVP de Análise Preditiva para Seguros",
            font=("Arial", 16, "bold"),
            fg=COR_TITULO,
            bg=COR_FUNDO,
        )
        titulo.pack(pady=(12, 4))

        self.lbl_status = tk.Label(
            self,
            text="Status: base não gerada | modelo não treinado",
            font=("Arial", 10),
            fg="#555555",
            bg=COR_FUNDO,
        )
        self.lbl_status.pack(pady=(0, 8))

        container = tk.Frame(self, bg=COR_FUNDO)
        container.pack(fill="both", expand=True, padx=12, pady=6)

        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(0, weight=1)

        self._construir_formulario(container)
        self._construir_painel_acoes_e_resultado(container)

    def _secao_label(self, parent, texto):
        return tk.Label(
            parent, text=texto, font=("Arial", 11, "bold"), fg=COR_SECAO, bg=COR_FUNDO
        )

    def _construir_formulario(self, parent):
        frame = tk.LabelFrame(
            parent, text="Formulário de Cliente", font=("Arial", 11, "bold"),
            bg=COR_FUNDO, padx=10, pady=10,
        )
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        linha = 0

        # Único campo digitável: Idade
        tk.Label(frame, text="Idade:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_idade = tk.StringVar(value="35")
        tk.Entry(frame, textvariable=self.var_idade, width=10).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Faixa de Renda
        tk.Label(frame, text="Faixa de Renda:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_renda = tk.StringVar(value=FAIXAS_RENDA[1][0])
        ttk.Combobox(
            frame, textvariable=self.var_renda, state="readonly", width=25,
            values=[f[0] for f in FAIXAS_RENDA],
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Tipo de Vínculo
        tk.Label(frame, text="Tipo de Vínculo:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_vinculo = tk.StringVar(value="CLT")
        ttk.Combobox(
            frame, textvariable=self.var_vinculo, state="readonly", width=25,
            values=list(TIPOS_VINCULO.keys()),
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Tempo no Emprego (anos) — selecionável
        tk.Label(frame, text="Tempo no Emprego (anos):", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_tempo_emprego = tk.StringVar(value="5")
        ttk.Combobox(
            frame, textvariable=self.var_tempo_emprego, state="readonly", width=25,
            values=[str(i) for i in range(0, 41)],
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Possui Imóvel
        tk.Label(frame, text="Possui Imóvel:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_imovel = tk.StringVar(value="Não")
        ttk.Combobox(
            frame, textvariable=self.var_imovel, state="readonly", width=25, values=SIM_NAO
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Possui Veículo
        tk.Label(frame, text="Possui Veículo:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_veiculo = tk.StringVar(value="Não")
        ttk.Combobox(
            frame, textvariable=self.var_veiculo, state="readonly", width=25, values=SIM_NAO
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Histórico de Crédito
        tk.Label(frame, text="Histórico de Crédito:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_credito = tk.StringVar(value="Regular")
        ttk.Combobox(
            frame, textvariable=self.var_credito, state="readonly", width=25,
            values=list(HISTORICOS_CREDITO.keys()),
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Estado Civil
        tk.Label(frame, text="Estado Civil:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_estado_civil = tk.StringVar(value=ESTADOS_CIVIS[0])
        ttk.Combobox(
            frame, textvariable=self.var_estado_civil, state="readonly", width=25,
            values=ESTADOS_CIVIS,
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Qtd. Filhos
        tk.Label(frame, text="Qtd. Filhos:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_qtd_filhos = tk.StringVar(value="0")
        ttk.Combobox(
            frame, textvariable=self.var_qtd_filhos, state="readonly", width=25,
            values=["0", "1", "2", "3", "4", "5"],
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Faixa Etária dos Filhos
        tk.Label(frame, text="Faixa Etária dos Filhos:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_faixa_filhos = tk.StringVar(value=FAIXAS_ETARIAS_FILHOS[0])
        ttk.Combobox(
            frame, textvariable=self.var_faixa_filhos, state="readonly", width=25,
            values=FAIXAS_ETARIAS_FILHOS,
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Possui Seguro
        tk.Label(frame, text="Possui Seguro:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_possui_seguro = tk.StringVar(value="Não")
        ttk.Combobox(
            frame, textvariable=self.var_possui_seguro, state="readonly", width=25, values=SIM_NAO
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

        # Qtd. de Seguros Ativos
        tk.Label(frame, text="Qtd. de Seguros Ativos:", bg=COR_FUNDO).grid(row=linha, column=0, sticky="w", pady=3)
        self.var_qtd_seguros = tk.StringVar(value="0")
        ttk.Combobox(
            frame, textvariable=self.var_qtd_seguros, state="readonly", width=25,
            values=["0", "1", "2", "3", "4"],
        ).grid(row=linha, column=1, sticky="w")
        linha += 1

    def _construir_painel_acoes_e_resultado(self, parent):
        lado_direito = tk.Frame(parent, bg=COR_FUNDO)
        lado_direito.grid(row=0, column=1, sticky="nsew")
        lado_direito.rowconfigure(1, weight=1)
        lado_direito.columnconfigure(0, weight=1)

        # Painel de Ações (Botões de Controle)
        painel_botoes = tk.LabelFrame(
            lado_direito, text="Painel de Ações", font=("Arial", 11, "bold"),
            bg=COR_FUNDO, padx=10, pady=10,
        )
        painel_botoes.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        botoes = [
            ("Gerar Base Sintética", self.on_gerar_base),
            ("Treinar Modelo", self.on_treinar_modelo),
            ("Analisar Cliente", self.on_analisar_cliente),
            ("Exibir Estatísticas", self.on_exibir_estatisticas),
            ("Limpar Dados", self.on_limpar_dados),
        ]
        for i, (texto, comando) in enumerate(botoes):
            tk.Button(
                painel_botoes, text=texto, command=comando, width=22,
                bg="white", relief="groove",
            ).grid(row=i, column=0, pady=3, sticky="ew")

        # Área de resultado (abas: Predição / Estatísticas)
        self.notebook = ttk.Notebook(lado_direito)
        self.notebook.grid(row=1, column=0, sticky="nsew")

        # Aba 1: Painel de Predições Individuais
        self.aba_predicao = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.aba_predicao, text="Predição do Cliente")
        self.txt_predicao = tk.Text(self.aba_predicao, wrap="word", font=("Consolas", 10))
        self.txt_predicao.pack(fill="both", expand=True, padx=6, pady=6)
        self.txt_predicao.insert("1.0", "Gere a base, treine o modelo e clique em 'Analisar Cliente'.")
        self.txt_predicao.config(state="disabled")

        # Aba 2: Estatísticas Populacionais
        self.aba_estatisticas = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.aba_estatisticas, text="Estatísticas Populacionais")
        self.frame_grafico = tk.Frame(self.aba_estatisticas, bg="white")
        self.frame_grafico.pack(fill="both", expand=True)
        self.txt_estatisticas = tk.Text(self.aba_estatisticas, height=8, font=("Consolas", 9))
        self.txt_estatisticas.pack(fill="x", padx=6, pady=(0, 6))

    # ------------------------------------------------------------------
    # Callbacks dos botões (Painel de Ações)
    # ------------------------------------------------------------------
    def _atualizar_status(self):
        base_ok = "OK" if self.base_clientes else "não gerada"
        modelo_ok = "OK" if self.modelo.treinado else "não treinado"
        self.lbl_status.config(text=f"Status: base {base_ok} ({len(self.base_clientes)} clientes) | modelo {modelo_ok}")

    def on_gerar_base(self):
        self.base_clientes = gerar_base(100)
        self.modelo = ModeloPreditivoSeguros()  # reseta modelo, pois a base mudou
        self._atualizar_status()
        messagebox.showinfo("Base Sintética", "Base sintética com 100 clientes gerada com sucesso.")

    def on_treinar_modelo(self):
        if not self.base_clientes:
            messagebox.showwarning("Atenção", "Gere a base sintética antes de treinar o modelo.")
            return
        try:
            r2 = self.modelo.treinar(self.base_clientes)
        except Exception as e:
            messagebox.showerror("Erro ao treinar", str(e))
            return
        self._atualizar_status()
        resumo = "\n".join(f"  {k}: R² = {v:.3f}" for k, v in r2.items())
        messagebox.showinfo("Modelo Treinado", f"Regressão Linear Múltipla treinada com sucesso.\n\n{resumo}")

    def _ler_cliente_do_formulario(self):
        try:
            idade = int(self.var_idade.get())
        except ValueError:
            raise ValueError("Idade deve ser um número inteiro (ex.: 35).")
        if not (18 <= idade <= 100):
            raise ValueError("Idade deve estar entre 18 e 100 anos.")

        renda_label = self.var_renda.get()
        renda_num = dict(FAIXAS_RENDA)[renda_label]

        return {
            "idade": idade,
            "faixa_renda": renda_label,
            "renda_num": renda_num,
            "tipo_vinculo": self.var_vinculo.get(),
            "tempo_emprego": int(self.var_tempo_emprego.get()),
            "possui_imovel": self.var_imovel.get(),
            "possui_veiculo": self.var_veiculo.get(),
            "historico_credito": self.var_credito.get(),
            "estado_civil": self.var_estado_civil.get(),
            "qtd_filhos": int(self.var_qtd_filhos.get()),
            "faixa_etaria_filhos": self.var_faixa_filhos.get(),
            "possui_seguro": self.var_possui_seguro.get(),
            "qtd_seguros_ativos": int(self.var_qtd_seguros.get()),
        }

    def on_analisar_cliente(self):
        if not self.modelo.treinado:
            messagebox.showwarning("Atenção", "Treine o modelo antes de analisar um cliente.")
            return
        try:
            cliente = self._ler_cliente_do_formulario()
            resultado = self.modelo.analisar_cliente(cliente)
        except Exception as e:
            messagebox.showerror("Erro na análise", str(e))
            return

        ig = resultado["indicadores_globais"]
        pc = resultado["propensao_contratacao"]
        rr = resultado["risco_retencao"]

        linhas = [
            "===== PAINEL DE PREDIÇÕES INDIVIDUAIS =====",
            "",
            "-- Indicadores Globais --",
            f"Score Geral: {ig['score_geral']} / 100",
            f"Tendência: {ig['tendencia']}",
            "",
            "-- Propensão de Contratação (%) --",
        ]
        for produto, valor in pc.items():
            linhas.append(f"  {produto}: {valor}%")
        linhas += [
            "",
            "-- Risco e Retenção (Churn) --",
            f"Probabilidade de Cancelamento: {rr['probabilidade_churn']}%",
            f"Tempo Estimado de Permanência: {rr['tempo_estimado_permanencia']}",
        ]

        self.txt_predicao.config(state="normal")
        self.txt_predicao.delete("1.0", "end")
        self.txt_predicao.insert("1.0", "\n".join(linhas))
        self.txt_predicao.config(state="disabled")
        self.notebook.select(self.aba_predicao)

    def on_exibir_estatisticas(self):
        if not self.base_clientes:
            messagebox.showwarning("Atenção", "Gere a base sintética antes de exibir estatísticas.")
            return

        # Limpa gráfico anterior, se existir
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        fig = estatistica.plotar_estatisticas(self.base_clientes)
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        relatorio = estatistica.gerar_relatorio_texto(self.base_clientes)
        self.txt_estatisticas.delete("1.0", "end")
        self.txt_estatisticas.insert("1.0", relatorio)

        self.notebook.select(self.aba_estatisticas)

    def on_limpar_dados(self):
        if not messagebox.askyesno("Confirmar", "Deseja limpar a base de dados e o modelo treinado?"):
            return
        self.base_clientes = []
        self.modelo = ModeloPreditivoSeguros()

        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        self.txt_estatisticas.delete("1.0", "end")

        self.txt_predicao.config(state="normal")
        self.txt_predicao.delete("1.0", "end")
        self.txt_predicao.insert("1.0", "Gere a base, treine o modelo e clique em 'Analisar Cliente'.")
        self.txt_predicao.config(state="disabled")

        self._atualizar_status()
        messagebox.showinfo("Dados Limpos", "Base e modelo foram reiniciados.")


def iniciar_aplicacao():
    app = AplicacaoSeguros()
    app.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()
