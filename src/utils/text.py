from typing import List, Dict
from collections import Counter
import re

# Lista de stopwords em português
STOPWORDS_PT = {
    'a', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas',
    'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas',
    'por', 'para', 'com', 'sem', 'sob', 'sobre', 'e', 'ou', 'mas', 'mais',
    'que', 'qual', 'quando', 'como', 'se', 'este', 'esta', 'isto', 'esse',
    'essa', 'isso', 'aquele', 'aquela', 'aquilo', 'meu', 'minha', 'teu',
    'tua', 'seu', 'sua', 'nosso', 'nossa', 'eu', 'tu', 'ele', 'ela', 'nós',
    'vós', 'eles', 'elas', 'já', 'só', 'tão', 'muito', 'todo', 'toda', 'também',
    'ainda', 'assim', 'apenas', 'cerca', 'desde', 'entre', 'etc', 'mesmo', 'deste', 'neste',
    'é', 'ser', 'ter', 'foi', 'foram', 'era', 'eram', 'está', 'estava', 'estavam',
    'tem', 'tinha', 'tinham', 'vai', 'vou', 'ir', 'terão', 'seja', 'fosse', 'fôssemos',
    'seus', 'suas', 'meus', 'minhas', 'teus', 'tuas'
}

def clean_and_tokenize(text: str) -> List[str]:
    #Limpa o texto, remove pontuações, converte para minúsculas e tokeniza.
    if not text:
        return []
        
    # 1. Converte para minúsculas
    text = text.lower()
    
    # 2. Remove pontuações e caracteres especiais, mantendo apenas letras e números
    # e substituindo por espaço para não juntar palavras
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 3. Remove múltiplos espaços e quebras de linha
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 4. Tokeniza (divide em palavras)
    tokens = text.split()
    
    return tokens

def count_word_frequencies(tokens: List[str]) -> Dict[str, int]:
    """
    Conta a frequência das palavras, ignorando as stopwords.
    Esta função é usada para a 'Lista das 10 palavras mais comuns (que não sejam stopwords)'.
    """
    # 1. Filtra stopwords e palavras que são apenas números
    filtered_tokens = [
        token for token in tokens
        if token not in STOPWORDS_PT and not token.isdigit() and len(token) > 1
    ]
    
    # 2. Conta a frequência
    word_counts = Counter(filtered_tokens)
    
    return dict(word_counts)

# --- Funções Auxiliares de Análise ---

def calculate_vocabulary_size(tokens: List[str]) -> int:
    """
    Calcula o tamanho do vocabulário (número de palavras distintas após limpeza básica).
    """
    vocabulary = {token for token in tokens if len(token) > 1}
    return len(vocabulary)

def get_top_n_words(word_frequencies: Dict[str, int], n: int = 10) -> List[tuple[str, int]]:
    """
    Retorna as N palavras mais comuns.
    """
    # Converte o dicionário de volta para Counter para usar o método most_common
    counter = Counter(word_frequencies)
    
    # Retorna as 10 palavras mais comuns 
    return counter.most_common(n)