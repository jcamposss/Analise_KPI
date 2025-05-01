import tkinter as tk
from tkinter import filedialog


def iniciar_interface_upload():
    root = tk.Tk()
    root.title("Selecione o Arquivo Excel")

    caminho_arquivo = None

    def selecionar_arquivo():
        nonlocal caminho_arquivo
        caminho_arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos Excel", "*.xlsx;*.xls;*.csv")]
        )
        if caminho_arquivo:
            label_arquivo_selecionado.config(
                text=f"Arquivo selecionado: {caminho_arquivo.split('/')[-1]}"
            )
            botao_analisar.config(state=tk.NORMAL)  # Habilita o botão "Analisar"

    def analisar_arquivo():
        root.destroy()  # Fecha a janela de upload
        root.quit()  # Termina o loop principal
        return  # Retorna None para sinalizar que a análise deve prosseguir

    # Widgets
    frame_selecao = tk.Frame(root, padx=10, pady=10)
    frame_selecao.pack()

    botao_selecionar = tk.Button(
        frame_selecao, text="Selecionar Arquivo Excel", command=selecionar_arquivo
    )
    botao_selecionar.pack(pady=5)

    label_arquivo_selecionado = tk.Label(text="Nenhum arquivo selecionado")
    label_arquivo_selecionado.pack(pady=5)

    botao_analisar = tk.Button(
        frame_selecao, text="Analisar e Exibir Painel de Controle", command=analisar_arquivo, state=tk.DISABLED
    )
    botao_analisar.pack(pady=10)

    root.mainloop()

    return caminho_arquivo


if __name__ == "__main__":
    caminho = iniciar_interface_upload()
    if caminho:
        print(f"Arquivo selecionado: {caminho}")
    else:
        print("Nenhum arquivo selecionado.")