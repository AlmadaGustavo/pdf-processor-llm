import pathlib
from typing import Optional

def get_file_size_bytes(file_path: pathlib.Path) -> Optional[int]:
    """
    Retorna o tamanho do arquivo em bytes.
    
    Lança FileNotFoundError se o arquivo não existir.
    """
    if not isinstance(file_path, pathlib.Path):
        # Converte para Path se for uma string 
        file_path = pathlib.Path(file_path)
    try:
        # Usando o método .stat() para obter informações sobre o arquivo, incluindo o tamanho
        file_size = file_path.stat().st_size
        return file_size
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado no caminho: {file_path}")
        return None
    except Exception as e:
        # Captura outros erros, como permissão negada
        print(f"ERRO inesperado ao acessar o arquivo {file_path}: {e}")
        return None