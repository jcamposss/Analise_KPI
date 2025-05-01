import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime

def exibir_painel_controle(dados_analisados):
    root = ThemedTk(theme="equilux")  # Escolha um tema do ttkthemes
    root.title("Painel de Controle de OS")
    root.geometry("1000x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    aba_contagem_os = ttk.Frame(notebook)
    notebook.add(aba_contagem_os, text="Contagem de OS")
    exibir_contagem_os(aba_contagem_os, dados_analisados["tabela_contagem_os"])

    aba_os_mais_antigas = ttk.Frame(notebook)
    notebook.add(aba_os_mais_antigas, text="OS Mais Antigas")
    exibir_os_mais_antigas(aba_os_mais_antigas, dados_analisados["os_mais_antigas"])

    aba_atualizacoes_atrasadas = ttk.Frame(notebook)
    notebook.add(aba_atualizacoes_atrasadas, text="Atualizações Atrasadas")
    exibir_atualizacoes_atrasadas(
        aba_atualizacoes_atrasadas, dados_analisados["atualizacoes_atrasadas"]
    )

    aba_tempos_resposta = ttk.Frame(notebook)
    notebook.add(aba_tempos_resposta, text="Tempos de Resposta Lentos")
    exibir_tempos_resposta_lentos(
        aba_tempos_resposta, dados_analisados["os_acima_5_min"]
    )

    aba_distribuicao_os = ttk.Frame(notebook)
    notebook.add(aba_distribuicao_os, text="Distribuição de Tipo de OS")
    exibir_distribuicao_tipo_os(
        aba_distribuicao_os, dados_analisados["tabela_contagem_os"], aba_distribuicao_os
    )

    root.mainloop()

def exibir_contagem_os(aba, tabela_contagem_os):
    tree = ttk.Treeview(aba, columns=("Tipo OS", "Quantidade"), show="headings")
    tree.heading("Tipo OS", text="Tipo OS")
    tree.heading("Quantidade", text="Quantidade")
    for item in tabela_contagem_os:
        tree.insert("", "end", values=(item["Tipo OS"], item["Quantidade"]))
    tree.pack(fill=tk.BOTH, expand=True)

def exibir_os_mais_antigas(aba, os_mais_antigas_data):
    tree = ttk.Treeview(
        aba, columns=("OS", "Tempo em Aberto", "Equipamento", "Tag"), show="headings"
    )
    tree.heading("OS", text="OS")
    tree.heading("Tempo em Aberto", text="Tempo em Aberto")
    tree.heading("Equipamento", text="Equipamento")
    tree.heading("Tag", text="Tag")
    for item in os_mais_antigas_data:
        tree.insert(
            "",
            "end",
            values=(
                item["OS"],
                item["Tempo em Aberto"],
                item.get("Equipamento", "N/A"),
                item.get("Tag", "N/A"),
            ),
        )
    tree.pack(fill=tk.BOTH, expand=True)

def exibir_atualizacoes_atrasadas(aba, atualizacoes_atrasadas_data):
    tree = ttk.Treeview(
        aba, columns=("OS", "Última atualização", "Equipamento", "Tag"), show="headings"
    )
    tree.heading("OS", text="OS")
    tree.heading("Última atualização", text="Última atualização")
    tree.heading("Equipamento", text="Equipamento")
    tree.heading("Tag", text="Tag")
    for item in atualizacoes_atrasadas_data:
        tree.insert(
            "",
            "end",
            values=(
                item["OS"],
                item["Última atualização"].strftime("%Y-%m-%d %H:%M:%S"),
                item.get("Equipamento", "N/A"),
                item.get("Tag", "N/A"),
            ),
        )
    tree.pack(fill=tk.BOTH, expand=True)

def exibir_tempos_resposta_lentos(aba, tempos_resposta_lentos_data):
    tree = ttk.Treeview(aba, columns=("OS", "Tempo 1° Atend."), show="headings")
    tree.heading("OS", text="OS")
    tree.heading("Tempo 1° Atend.", text="Tempo 1° Atend. (HH:MM:SS)")
    for item in tempos_resposta_lentos_data:
        tempo_atendimento = item["Tempo 1° Atend."]
        horas, resto = divmod(tempo_atendimento, 3600)
        minutos, segundos = divmod(resto, 60)
        tempo_formatado = f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"
        tree.insert("", "end", values=(item["OS"], tempo_formatado))
    tree.pack(fill=tk.BOTH, expand=True)

def exibir_distribuicao_tipo_os(aba, tabela_contagem_os, frame):
    labels = [item["Tipo OS"] for item in tabela_contagem_os]
    sizes = [item["Quantidade"] for item in tabela_contagem_os]

    fig, ax = plt.subplots()
    ax.bar(labels, sizes)
    ax.set_xlabel("Tipo OS")
    ax.set_ylabel("Quantidade")
    ax.set_title("Distribuição de Tipo de OS")
    plt.xticks(rotation=45, ha="right")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    dados_teste = {
        "tabela_contagem_os": [
            {"Tipo OS": "A", "Quantidade": 10},
            {"Tipo OS": "B", "Quantidade": 20},
            {"Tipo OS": "C", "Quantidade": 15},
        ],
        "os_mais_antigas": [
            {"OS": "1", "Tempo em Aberto": "10 dias", "Equipamento": "Equip1", "Tag": "Tag1"},
            {"OS": "2", "Tempo em Aberto": "20 dias", "Equipamento": "Equip2", "Tag": "Tag2"},
        ],
        "atualizacoes_atrasadas": [
            {"OS": "3", "Última atualização": datetime(2025, 5, 1), "Equipamento": "Equip3", "Tag": "Tag3"},
            {"OS": "4", "Última atualização": datetime(2025, 4, 25), "Equipamento": "Equip4", "Tag": "Tag4"},
        ],
        "os_acima_5_min": [
            {"OS": "5", "Tempo 1° Atend.": 600},
            {"OS": "6", "Tempo 1° Atend.": 700},
        ],
    }
    exibir_painel_controle(dados_teste)