import pandas as pd
from datetime import datetime, timedelta


def analisar_dados_os(caminho_arquivo):
    """
    Analisa dados de OS de um arquivo Excel.

    Args:
        caminho_arquivo (str): Caminho para o arquivo Excel.

    Returns:
        pandas.DataFrame: DataFrame com os resultados da análise.
                        Retorna None em caso de erro.
    """
    try:
        df = pd.read_excel(caminho_arquivo)

        # Inicializar DataFrame vazio para armazenar os dados
        dados = []

        # Obter os nomes das colunas da segunda linha
        colunas = df.iloc[1].to_list()

        # Iterar pelas linhas a partir da terceira linha
        for i in range(2, len(df)):
            linha = df.iloc[i].to_list()
            # Criar um dicionário associando os nomes das colunas aos valores da linha
            dados_linha = dict(zip(colunas, linha))
            dados.append(dados_linha)

        # Converter a lista de dicionários em um DataFrame
        df_filtrado = pd.DataFrame(dados)

        # Converter colunas relevantes para numérico ou datetime
        df_filtrado['Tempo 1° Atend.'] = df_filtrado['Tempo 1° Atend.'].apply(
            lambda x: sum(int(t) * 60**i for i, t in enumerate(reversed(x.split(':'))))
        )
        df_filtrado['Data'] = pd.to_datetime(df_filtrado['Data'], format='%d/%m/%Y')
        df_filtrado['Última atualização'] = pd.to_datetime(
            df_filtrado['Última atualização'], format='%d/%m/%Y %H:%M:%S'
        )

        # --- Análise ---

        # 1. OS com maior quantidade
        contagem_os = df_filtrado['Tipo OS'].value_counts().reset_index()
        contagem_os.columns = ['Tipo OS', 'Quantidade']
        os_mais_comum = contagem_os.iloc[0].to_dict()

        # 2. OS mais antigas (Tempo em Aberto)
        df_filtrado['Tempo em Aberto'] = df_filtrado['Tempo em Aberto'].fillna(
            '0 days, 00:00:00'
        )  # Preencher NaN com '0 days, 00:00:00'

        def converter_para_segundos(tempo_str):
            partes = tempo_str.split(', ')
            dias = int(partes[0].split(' ')[0]) if len(partes) > 1 else 0
            partes_tempo = partes[-1].split(':')
            horas = int(partes_tempo[0])
            minutos = int(partes_tempo[1])
            segundos = int(partes_tempo[2])
            total_segundos = (
                dias * 24 * 3600
            ) + (
                horas * 3600
            ) + (
                minutos * 60
            ) + segundos
            return total_segundos

        df_filtrado['Tempo em Aberto (segundos)'] = df_filtrado[
            'Tempo em Aberto'
        ].apply(converter_para_segundos)
        os_mais_antigas = df_filtrado.sort_values(
            by='Tempo em Aberto (segundos)', ascending=False
        )[['OS', 'Tempo em Aberto']].to_dict(orient='records')

        # 3. Quantidade em corretiva
        quantidade_corretiva = len(df_filtrado[df_filtrado['Tipo OS'] == 'CORRETIVA'])

        # 4. Quantidade em transporte de ultrassom
        quantidade_ultrassom = len(
            df_filtrado[
                df_filtrado['Tipo OS'].str.contains(
                    'TRANSPORTE DE ULTRA-SOM', case=False, na=False
                )
            ]
        )
        codigos_os_ultrassom = df_filtrado[
            df_filtrado['Tipo OS'].str.contains(
                'TRANSPORTE DE ULTRA-SOM', case=False, na=False
            )
        ]['OS'].tolist()

        # 5. Quantidade em suporte ao usuário
        quantidade_suporte = len(
            df_filtrado[df_filtrado['Tipo OS'] == 'SUPORTE AO USUARIO']
        )

        # 6. Últimas atualizações fora do prazo
        uma_semana_atras = datetime.now() - timedelta(weeks=1)
        atualizacoes_atrasadas = df_filtrado[
            df_filtrado['Última atualização'] < uma_semana_atras
        ][['OS', 'Última atualização']].to_dict(orient='records')

        # 7. Tempo de 1º atendimento > 5 minutos
        os_acima_5_min = df_filtrado[df_filtrado['Tempo 1° Atend.'] > 300][
            ['OS', 'Tempo 1° Atend.']
        ].to_dict(orient='records')

        # Preparar dados para tabelas e visualizações
        tabela_contagem_os = contagem_os.to_dict(orient='records')

        resultados = {
            "os_mais_comum": os_mais_comum,
            "os_mais_antigas": os_mais_antigas,
            "quantidade_corretiva": quantidade_corretiva,
            "quantidade_ultrassom": quantidade_ultrassom,
            "codigos_os_ultrassom": codigos_os_ultrassom,
            "quantidade_suporte": quantidade_suporte,
            "atualizacoes_atrasadas": atualizacoes_atrasadas,
            "os_acima_5_min": os_acima_5_min,
            "tabela_contagem_os": tabela_contagem_os,
        }

        return resultados

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_arquivo}")
        return None
    except Exception as e:
        print(f"Erro durante a análise: {e}")
        return None


if __name__ == "__main__":
    # Código de teste (opcional)
    caminho_arquivo_teste = "Recebimento_de_Solicitacao_de_Servico___Eng__Clinica.json"  # Substitua pelo seu arquivo
    dados = analisar_dados_os(caminho_arquivo_teste)
    if dados is not None:
        print(dados)