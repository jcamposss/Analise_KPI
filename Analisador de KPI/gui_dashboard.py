import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime  # Importe o módulo datetime aqui


def exibir_painel_controle(dados_analisados):
    root = tk.Tk()
    root.title("Painel de Controle de OS")
    root.geometry("1000x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Aba para Contagem de OS
    aba_contagem_os = ttk.Frame(notebook)
    notebook.add(aba_contagem_os, text="Contagem de OS")
    exibir_contagem_os(aba_contagem_os, dados_analisados['tabela_contagem_os'])

    # Aba para OS Mais Antigas
    aba_os_mais_antigas = ttk.Frame(notebook)
    notebook.add(aba_os_mais_antigas, text="OS Mais Antigas")
    exibir_os_mais_antigas(aba_os_mais_antigas, dados_analisados['os_mais_antigas'])

    # Aba para Atualizações Atrasadas
    aba_atualizacoes_atrasadas = ttk.Frame(notebook)
    notebook.add(aba_atualizacoes_atrasadas, text="Atualizações Atrasadas")
    exibir_atualizacoes_atrasadas(
        aba_atualizacoes_atrasadas, dados_analisados['atualizacoes_atrasadas']
    )

    # Aba para Tempos de Resposta Lentos
    aba_tempos_resposta = ttk.Frame(notebook)
    notebook.add(aba_tempos_resposta, text="Tempos de Resposta Lentos")
    exibir_tempos_resposta_lentos(
        aba_tempos_resposta, dados_analisados['os_acima_5_min']
    )

    # Aba para Distribuição de Tipo de OS (Gráfico de Pizza)
    aba_distribuicao_os = ttk.Frame(notebook)
    notebook.add(aba_distribuicao_os, text="Distribuição de Tipo de OS")
    exibir_distribuicao_tipo_os(
        aba_distribuicao_os, dados_analisados['tabela_contagem_os']
    )

    root.mainloop()


def exibir_contagem_os(aba, tabela_contagem_os):
    """Exibe a contagem de OS em uma tabela."""

    tree = ttk.Treeview(aba, columns=('Tipo OS', 'Quantidade'), show='headings')
    tree.heading('Tipo OS', text='Tipo OS')
    tree.heading('Quantidade', text='Quantidade')
    for item in tabela_contagem_os:
        tree.insert('', 'end', values=(item['Tipo OS'], item['Quantidade']))
    tree.pack(fill=tk.BOTH, expand=True)


def exibir_os_mais_antigas(aba, os_mais_antigas_data):
    """Exibe as entradas de OS mais antigas."""

    tree = ttk.Treeview(aba, columns=('OS', 'Tempo em Aberto'), show='headings')
    tree.heading('OS', text='OS')
    tree.heading('Tempo em Aberto', text='Tempo em Aberto')
    for item in os_mais_antigas_data:
        tree.insert('', 'end', values=(item['OS'], item['Tempo em Aberto']))
    tree.pack(fill=tk.BOTH, expand=True)


def exibir_atualizacoes_atrasadas(aba, atualizacoes_atrasadas_data):
    """Exibe as entradas de OS com atualizações atrasadas."""

    tree = ttk.Treeview(aba, columns=('OS', 'Última atualização'), show='headings')
    tree.heading('OS', text='OS')
    tree.heading('Última atualização', text='Última atualização')
    for item in atualizacoes_atrasadas_data:
        tree.insert(
            '',
            'end',
            values=(
                item['OS'],
                item['Última atualização'].strftime('%Y-%m-%d %H:%M:%S'),
            ),
        )
    tree.pack(fill=tk.BOTH, expand=True)


def exibir_tempos_resposta_lentos(aba, tempos_resposta_lentos_data):
    """Exibe as entradas de OS com tempos de resposta lentos."""

    tree = ttk.Treeview(aba, columns=('OS', 'Tempo 1° Atend.'), show='headings')
    tree.heading('OS', text='OS')
    tree.heading('Tempo 1° Atend.', text='Tempo 1° Atend. (segundos)')
    for item in tempos_resposta_lentos_data:
        tree.insert('', 'end', values=(item['OS'], item['Tempo 1° Atend.']))
    tree.pack(fill=tk.BOTH, expand=True)


def exibir_distribuicao_tipo_os(aba, tabela_contagem_os):
    """Exibe a distribuição dos tipos de OS usando um gráfico de pizza."""

    labels = [item['Tipo OS'] for item in tabela_contagem_os]
    sizes = [item['Quantidade'] for item in tabela_contagem_os]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Proporção igual garante que a pizza seja desenhada como um círculo.

    canvas = FigureCanvasTkAgg(fig, master=aba)  # Um tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    # Dados de exemplo para teste
    dados_teste = {
        'tabela_contagem_os': [
            {'Tipo OS': 'A', 'Quantidade': 10},
            {'Tipo OS': 'B', 'Quantidade': 20},
            {'Tipo OS': 'C', 'Quantidade': 15},
        ],
        'os_mais_antigas': [
            {'OS': '1', 'Tempo em Aberto': '10 dias'},
            {'OS': '2', 'Tempo em Aberto': '20 dias'},
        ],
        'atualizacoes_atrasadas': [
            {'OS': '3', 'Última atualização': datetime(2025, 5, 1)},
            {'OS': '4', 'Última atualização': datetime(2025, 4, 25)},
        ],
        'os_acima_5_min': [
            {'OS': '5', 'Tempo 1° Atend.': 600},
            {'OS': '6', 'Tempo 1° Atend.': 700},
        ],
    }
    exibir_painel_controle(dados_teste)