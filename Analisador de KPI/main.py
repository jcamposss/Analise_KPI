import tkinter as tk
from tkinter import messagebox
import pandas as pd
from gui_upload import iniciar_interface_upload
from analise_dados import analisar_dados_os
from gui_dashboard import exibir_painel_controle


def main():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal inicial

    caminho_arquivo = iniciar_interface_upload()

    if caminho_arquivo:
        try:
            dados_analisados = analisar_dados_os(caminho_arquivo)
            if dados_analisados is not None:
                exibir_painel_controle(dados_analisados)
            else:
                messagebox.showerror("Erro", "A análise dos dados falhou.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
    else:
        messagebox.showinfo("Informação", "Nenhum arquivo selecionado. A aplicação será encerrada.")

    root.destroy()  # Garante que a janela principal seja destruída


if __name__ == "__main__":
    main()