import argparse

def parse_arguments():
    """
    Define e processa os argumentos de linha de comando usando argparse.
    """
    
    # 1. Instanciar o ArgumentParser

    parser = argparse.ArgumentParser(
        description="Ferramenta CLI para processamento de PDF e resumo com LLM local."
    )


    # 2. Adicionar Argumentos

    # Argumento Obrigatório: Arquivo PDF
    parser.add_argument(
        '-f','--file',
        type=str, # Espera uma string
        required=True, # Torna o argumento obrigatório
        help='Caminho para o arquivo PDF em português a ser processado.'
    )
    # Argumento Opcional: Diretório de Saída
    parser.add_argument(
        '-o', '--output', 
        type=str,
        default='output/', # Se não for passado, usa 'output/'
        help='Diretório de saída para salvar o resumo e as imagens. Padrão: "output/".'
    )
    # Flag Opcional: Gerar Resumo (LLM)
    parser.add_argument(
        '--summarize', 
        action='store_true', # Define o valor como True se a flag estiver presente
        help='Ativa a geração do resumo do conteúdo do PDF usando a LLM local.'
    )

    # 3. Retornar o Objeto de Argumentos Processados
    return parser.parse_args()